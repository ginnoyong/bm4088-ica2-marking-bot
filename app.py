"""BM4088 ICA2 Marking Bot — Streamlit entry point.

Stage 5: startup secrets validation, Claude API retry handling, and
resilient Google Sheets logging.
"""

import base64
import threading
import uuid

import anthropic
import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError
from streamlit.runtime.scriptrunner import add_script_run_ctx

from src.api_client import (
    get_client,
    image_block,
    load_reference_bundle,
    load_system_instructions,
    stream_marker_message,
)
from src.auth import is_authorized
from src.help_content import HELP_TEXT
from src.notebook_parser import parse_notebook
from src.scorecard_tracker import sorted_scorecard_rows, update_scorecard
from src.sheets_logger import get_client as get_sheets_client
from src.sheets_logger import get_worksheet, log_turn

st.set_page_config(
    page_title="BM4088 ICA2 Marking Bot",
    page_icon=":material/school:",
    # An int here sets the sidebar's initial pixel width (still "auto" show/hide
    # behaviour) — native as of this Streamlit version, so no CSS injection
    # needed for width specifically. 420px (vs. the ~244px default): the
    # scorecard's three st.dataframe columns (small+medium+small = 75+200+75
    # = 350px, per column_config below) need that plus room for the
    # sidebar's own padding/border, or the dataframe gets its own internal
    # horizontal scrollbar despite already being narrower than before.
    initial_sidebar_state=420,
)

SCENARIO_NUMBERS = [1, 2, 3, 4, 5, 6]

REQUIRED_TOP_LEVEL_SECRETS = [
    "ANTHROPIC_API_KEY",
    "GOOGLE_SHEET_ID",
    "GOOGLE_SHEET_NAME",
    "ROSTER_SHEET_ID",
    "ROSTER_SHEET_NAME",
]
REQUIRED_SERVICE_ACCOUNT_FIELDS = [
    "type",
    "project_id",
    "private_key_id",
    "private_key",
    "client_email",
    "client_id",
    "token_uri",
]


def _media_type_for_upload(uploaded_file) -> str:
    """Only called for an upload that isn't a .ipynb (see render_chat), so
    it's always png/jpg/jpeg here. The browser-reported MIME type is
    trusted first; the extension is only a fallback for the rare case a
    browser reports something unexpected."""
    if uploaded_file.type in ("image/png", "image/jpeg"):
        return uploaded_file.type
    ext = uploaded_file.name.rsplit(".", 1)[-1].lower()
    return "image/png" if ext == "png" else "image/jpeg"


def _render_message_content(content) -> None:
    """Chat message content is either a plain string (the common case) or a
    list of Messages API content blocks (image + text) for a turn with an
    attached screenshot — render each block appropriately."""
    if isinstance(content, str):
        st.markdown(content)
        return
    for block in content:
        if block.get("type") == "image":
            st.image(base64.standard_b64decode(block["source"]["data"]))
        elif block.get("type") == "text":
            st.markdown(block["text"])


def _extract_text(content) -> str:
    """Plain-text view of message content, for Sheets logging and for
    building the Haiku classification input — image blocks contribute
    nothing here (classification gets a separate note instead, see
    _classify_text_for_content)."""
    if isinstance(content, str):
        return content
    return " ".join(block["text"] for block in content if block.get("type") == "text").strip()


def _classify_text_for_content(content) -> str:
    """Text sent to Stage 2's classify_component_type() call. When an image
    is attached, prepend a short note so classification still routes
    correctly even when the accompanying text alone is minimal."""
    text = _extract_text(content)
    has_image = not isinstance(content, str) and any(block.get("type") == "image" for block in content)
    if has_image:
        return f"[Image attached: chart screenshot] {text}".strip()
    return text


def _validate_secrets() -> list[str]:
    """Return the names of any missing or empty required secrets.

    Returns a single-item list naming the secrets file itself if it can't be
    found or parsed at all, rather than letting that surface as a raw
    FileNotFoundError deep inside a cached function later.
    """
    try:
        missing = [key for key in REQUIRED_TOP_LEVEL_SECRETS if not st.secrets.get(key)]

        if "gcp_service_account" not in st.secrets:
            missing.append("gcp_service_account")
        else:
            service_account = st.secrets["gcp_service_account"]
            missing.extend(
                f"gcp_service_account.{field}"
                for field in REQUIRED_SERVICE_ACCOUNT_FIELDS
                if not service_account.get(field)
            )
        return missing
    except StreamlitSecretNotFoundError:
        return ["(no secrets.toml found — see .streamlit/secrets.toml)"]


@st.cache_resource
def _get_client():
    return get_client()


@st.cache_data
def _load_static_content():
    return load_system_instructions(), load_reference_bundle()


@st.cache_resource
def _get_sheets_worksheet():
    client = get_sheets_client(dict(st.secrets["gcp_service_account"]))
    return get_worksheet(client, st.secrets["GOOGLE_SHEET_ID"], st.secrets["GOOGLE_SHEET_NAME"])


@st.cache_resource
def _get_roster_worksheet():
    client = get_sheets_client(dict(st.secrets["gcp_service_account"]))
    return get_worksheet(client, st.secrets["ROSTER_SHEET_ID"], st.secrets["ROSTER_SHEET_NAME"])


@st.dialog("How to use this bot")
def _show_help_dialog() -> None:
    """Pure UI overlay — reads only the static HELP_TEXT, touches no
    session state, and makes no API calls. Safe to open/close from
    anywhere without affecting login input, chat history, or the
    locked scenario number."""
    st.markdown(HELP_TEXT)
    if st.button("Close"):
        st.rerun()


def _start_new_submission() -> None:
    """Fresh session, fresh cache lifecycle — not an in-conversation reset."""
    st.session_state.session_id = uuid.uuid4().hex
    st.session_state.scenario_number = None
    st.session_state.messages = []
    st.session_state.scorecard = {}
    st.session_state.last_error = None
    st.session_state.generating = False
    st.session_state.gen_thread = None
    st.session_state.stop_event = None
    st.session_state.partial_response = ""
    st.session_state.gen_result = None
    st.session_state.gen_error = None
    st.session_state.pending_user_message = None


def render_login() -> None:
    st.title("BM4088 ICA2 Marking Bot")
    st.subheader("Staff Login")

    with st.form("login_form"):
        staff_id = st.text_input("Staff ID")
        submitted = st.form_submit_button("Log in")

    st.divider()
    with st.container(border=True):
        st.subheader("How to use this bot")
        st.markdown(HELP_TEXT)

    if submitted:
        try:
            authorized = is_authorized(staff_id, _get_roster_worksheet())
        except Exception as e:
            # Broad catch: gspread/Google API calls can fail in more ways than
            # the old CSV read did (auth, permissions, network, rate limits) —
            # the roster is now a live dependency, not a bundled file.
            st.error(f"Login is currently unavailable: {e}")
            return

        if authorized:
            st.session_state.authenticated = True
            st.session_state.staff_id = staff_id.strip()
            _start_new_submission()
            st.rerun()
        else:
            st.error("Staff ID not recognized. Please check your ID and try again.")


def render_scenario_selector() -> None:
    st.title("BM4088 ICA2 Marking Bot")
    st.caption(f"Logged in as **{st.session_state.staff_id}**")

    if st.button("Log out"):
        st.session_state.authenticated = False
        st.session_state.staff_id = None
        st.rerun()

    st.divider()
    st.subheader("Select Scenario")
    st.write(
        "Choose the business scenario (1–6) for this submission. "
        "This locks for the rest of the session."
    )

    with st.form("scenario_form"):
        scenario = st.selectbox("Scenario number", SCENARIO_NUMBERS)
        submitted = st.form_submit_button("Confirm scenario")

    if submitted:
        st.session_state.scenario_number = scenario
        st.rerun()


def _log_turn_safely(
    component_type: str, model_used: str, usage, marker_input: str, response_text: str, stop_reason: str | None
) -> None:
    """Google Sheets write failures must never block the already-rendered
    chat response — log the failure to console and move on."""
    try:
        worksheet = _get_sheets_worksheet()
        log_turn(
            worksheet,
            st.session_state.staff_id,
            st.session_state.session_id,
            st.session_state.scenario_number,
            component_type,
            model_used,
            usage,
            marker_input,
            response_text,
            stop_reason,
        )
    except Exception as e:
        print(f"[sheets_logger] failed to log turn: {e}")


def _generation_worker(
    client, instructions, reference_bundle, history, user_message, stop_event, classify_text, forced_component_type
) -> None:
    """Runs on a background thread so the main script stays free to render
    a Stop button and poll for progress. Writes results into session_state
    keys the fragment below reads — never touches `generating` itself, so
    there's no race between the worker finishing and the poller noticing:
    completion is detected purely from `gen_thread.is_alive()`.
    """

    def on_delta(text: str) -> None:
        st.session_state.partial_response = text

    try:
        result = stream_marker_message(
            client, instructions, reference_bundle, history, user_message,
            on_delta=on_delta, should_stop=stop_event.is_set, classify_text=classify_text,
            forced_component_type=forced_component_type,
        )
        st.session_state.gen_result = result
        st.session_state.gen_error = None
    except anthropic.RateLimitError:
        st.session_state.gen_result = None
        st.session_state.gen_error = "Claude is rate-limiting requests right now. Wait a moment and retry."
    except anthropic.APIConnectionError:
        st.session_state.gen_result = None
        st.session_state.gen_error = "Could not reach the Claude API — check your network connection and retry."
    except anthropic.APIStatusError as e:
        st.session_state.gen_result = None
        st.session_state.gen_error = f"Claude API error ({e.status_code}): {e.message}"
    except Exception as e:
        st.session_state.gen_result = None
        st.session_state.gen_error = f"Unexpected error calling Claude: {e}"


def _start_generation(user_message, forced_component_type: str | None = None) -> None:
    """Kick off streaming generation for `user_message` on a background
    thread. Used for both a fresh chat_input submission and Retry.

    `user_message` is either a plain string or a list of Messages API
    content blocks (image + text) when a screenshot was attached — the
    classification text sent to Stage 2 is derived from it here so both
    the fresh-submission and Retry paths get the same "image attached"
    note behaviour for free.

    `forced_component_type` skips Stage 2's classification call entirely
    (set when a .ipynb was attached — see render_chat) — passed through
    as-is so Retry preserves the same certain signal on a re-attempt.
    """
    # The UI-selected scenario number is app-side state the model never
    # otherwise sees — inject it as the earliest context on every call, so
    # the marker isn't asked to re-supply what they already picked in the
    # scenario selector.
    scenario_context = {
        "role": "user",
        "content": f"For this session, the scenario number is {st.session_state.scenario_number}.",
    }
    history = [scenario_context] + [
        {"role": m["role"], "content": m["content"]} for m in st.session_state.messages[:-1]
    ]
    instructions, reference_bundle = _load_static_content()
    client = _get_client()
    classify_text = _classify_text_for_content(user_message)

    st.session_state.stop_event = threading.Event()
    st.session_state.partial_response = ""
    st.session_state.gen_result = None
    st.session_state.gen_error = None
    st.session_state.pending_user_message = user_message
    st.session_state.generating = True

    thread = threading.Thread(
        target=_generation_worker,
        args=(
            client, instructions, reference_bundle, history, user_message,
            st.session_state.stop_event, classify_text, forced_component_type,
        ),
        daemon=True,
    )
    add_script_run_ctx(thread)
    thread.start()
    st.session_state.gen_thread = thread


def _finalize_generation() -> None:
    """Runs on the main thread once the background worker has finished
    (naturally or via Stop). Moves the result into permanent chat history
    and logs it — the only place `generating` is cleared."""
    result = st.session_state.get("gen_result")
    error = st.session_state.get("gen_error")
    user_message = st.session_state.get("pending_user_message")

    if error:
        st.session_state.last_error = error
    elif result["stopped"]:
        st.session_state.last_error = None
        response_text = result["text"]
        if response_text:
            st.session_state.messages.append(
                {"role": "assistant", "content": response_text, "debug": "⏹ generation stopped by marker"}
            )
            update_scorecard(st.session_state.scorecard, response_text)
        # No Sheets row for a stopped turn — it produced no real verdict to log.
    elif not result["text"]:
        # An empty completion can't be appended to history: as_blocks() would wrap it
        # into an empty text block, and the Messages API rejects cache_control on an
        # empty text block — which is exactly where that block would land once this
        # turn is no longer the newest message. Surface it as a retryable error instead.
        if result.get("stop_reason") == "max_tokens":
            st.session_state.last_error = (
                "Claude spent its entire token budget thinking about that message and had "
                "no room left to write a reply — try Retry (adaptive thinking is variable, "
                "so a retry often succeeds even without changing anything)."
            )
        else:
            st.session_state.last_error = (
                f"Claude returned an empty response for that message "
                f"(stop_reason: {result.get('stop_reason')}) — try Retry."
            )
    else:
        st.session_state.last_error = None
        response_text = result["text"]
        debug_line = f"component_type: `{result['component_type']}` · model: `{result['model']}`"
        st.session_state.messages.append(
            {"role": "assistant", "content": response_text, "debug": debug_line}
        )
        update_scorecard(st.session_state.scorecard, response_text)
        _log_turn_safely(
            result["component_type"], result["model"], result["usage"], _extract_text(user_message), response_text,
            result["stop_reason"],
        )

    st.session_state.generating = False
    st.session_state.gen_thread = None
    st.session_state.stop_event = None
    st.session_state.partial_response = ""
    st.session_state.gen_result = None
    st.session_state.gen_error = None
    st.session_state.pending_user_message = None


@st.fragment(run_every="0.3s")
def _render_generation_progress() -> None:
    """Auto-refreshing fragment: shows the streaming reply so far and a
    Stop button while the background worker runs, then hands off to
    _finalize_generation() the moment it detects the worker has finished."""
    thread = st.session_state.get("gen_thread")
    if thread is None:
        return

    if thread.is_alive():
        with st.chat_message("assistant"):
            st.markdown(st.session_state.get("partial_response") or "Thinking…")
            if st.button("Stop", key="stop_generation_button"):
                st.session_state.stop_event.set()
    else:
        _finalize_generation()
        st.rerun()


def render_chat() -> None:
    with st.sidebar:
        if st.button("How to use this bot", key="help_button_chat"):
            _show_help_dialog()

        rows = sorted_scorecard_rows(st.session_state.scorecard)
        if rows:
            st.caption("Running scorecard")
            # st.dataframe (not st.table) to keep its native hover toolbar
            # (download/search/fullscreen). Wrapping is enabled by row_height
            # alone — a taller-than-one-line row_height is what turns on
            # cell wrapping in the underlying grid; there's no separate wrap
            # flag on the column types. Explicit widths keep Criterion
            # compact and give Grade/Status room without either column
            # eating the whole sidebar.
            st.dataframe(
                rows,
                hide_index=True,
                row_height=52,
                column_config={
                    "Criterion": st.column_config.TextColumn(width="small"),
                    "Grade": st.column_config.TextColumn(width="medium"),
                    "Status": st.column_config.TextColumn(width="small"),
                },
            )

    st.title("BM4088 ICA2 Marking Bot")
    st.caption(f"Logged in as **{st.session_state.staff_id}**")

    top_left, top_right = st.columns([3, 1])
    with top_left:
        st.info(f"Scenario: **{st.session_state.scenario_number}** (locked for this submission)")
    with top_right:
        if not st.session_state.get("generating"):
            if st.button("Start New Submission"):
                _start_new_submission()
                st.rerun()

    with st.container(height=650, autoscroll=True):
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                _render_message_content(msg["content"])
                if msg.get("debug"):
                    st.caption(msg["debug"])

    if st.session_state.get("generating"):
        _render_generation_progress()
        return

    st.caption(
        "📎 Optionally attach a PNG/JPEG screenshot of a Power BI chart (e.g. for a 3.1 check), "
        "or a .ipynb notebook (Requirement 4 checks) — at most one per message."
    )
    chat_value = st.chat_input(
        "Type your message to the marking bot...",
        accept_file=True,
        file_type=["png", "jpg", "jpeg", "ipynb"],
    )
    if chat_value:
        text = chat_value.text.strip()
        uploaded = chat_value.files[0] if chat_value.files else None
        if uploaded is None and not text:
            # accept_file=True means the widget can submit with a blank/whitespace-only
            # text box and no file (e.g. an attachment removed after being added) —
            # nothing to send; as_blocks() would otherwise wrap "" into an empty text
            # block, which the Messages API rejects a cache_control breakpoint on.
            st.rerun()
            return

        forced_component_type = None
        if uploaded is not None and uploaded.name.lower().endswith(".ipynb"):
            try:
                notebook_text = parse_notebook(uploaded.getvalue())
            except Exception as e:
                st.error(f"Couldn't parse that notebook: {e}")
                st.rerun()
                return
            if not text:
                text = "(no additional text — see attached notebook)"
            content = f"{notebook_text}\n\n{text}"
            # The .ipynb extension is a certain signal for python_code — skip Stage 2's
            # Haiku classification call entirely, per docs/implementation_notes.md.
            forced_component_type = "python_code"
        elif uploaded is not None:
            if not text:
                text = "(no additional text — see attached screenshot)"
            content = [image_block(uploaded.getvalue(), _media_type_for_upload(uploaded)), {"type": "text", "text": text}]
        else:
            content = text

        st.session_state.messages.append(
            {"role": "user", "content": content, "forced_component_type": forced_component_type}
        )
        with st.chat_message("user"):
            _render_message_content(content)
        _start_generation(content, forced_component_type=forced_component_type)
        st.rerun()
        return

    if st.session_state.get("last_error"):
        if st.button("Retry"):
            last_message = st.session_state.messages[-1]
            st.session_state.last_error = None
            _start_generation(last_message["content"], forced_component_type=last_message.get("forced_component_type"))
            st.rerun()
        else:
            st.error(st.session_state.last_error)


def main() -> None:
    missing_secrets = _validate_secrets()
    if missing_secrets:
        st.title("BM4088 ICA2 Marking Bot")
        st.error(
            "The app is missing required configuration and cannot start.\n\n"
            "Missing secret(s):\n" + "\n".join(f"- `{name}`" for name in missing_secrets) + "\n\n"
            "Add these to `.streamlit/secrets.toml` locally, or in the app's "
            "**Secrets** panel on Streamlit Community Cloud, then reload."
        )
        st.stop()

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "scorecard" not in st.session_state:
        st.session_state.scorecard = {}

    if not st.session_state.authenticated:
        render_login()
        return

    if st.session_state.get("scenario_number") is None:
        render_scenario_selector()
    else:
        render_chat()


if __name__ == "__main__":
    main()
