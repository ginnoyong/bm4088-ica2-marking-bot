"""Claude Messages API client: content loading, prompt caching, and the
classify-then-call flow.
"""

import base64
import os
from pathlib import Path
from typing import Callable

import anthropic

from src.model_routing import classify_component_type, select_model

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SYSTEM_INSTRUCTIONS_PATH = PROJECT_ROOT / "prompts" / "system_instructions.md"
REFERENCE_DIR = PROJECT_ROOT / "reference"


def load_system_instructions(path: Path = SYSTEM_INSTRUCTIONS_PATH) -> str:
    return path.read_text(encoding="utf-8")


def load_reference_bundle(reference_dir: Path = REFERENCE_DIR) -> str:
    """Concatenate every .md file under reference/, explicitly excluding
    roster.csv (and any other non-.md file) — filtered by extension, not
    a directory glob, so auth data never ends up in what's sent to Claude.
    """
    md_files = sorted(reference_dir.glob("*.md"))
    sections = [f.read_text(encoding="utf-8") for f in md_files]
    return "\n\n".join(sections)


def get_api_key() -> str:
    try:
        import streamlit as st

        if "ANTHROPIC_API_KEY" in st.secrets:
            return st.secrets["ANTHROPIC_API_KEY"]
    except Exception:
        pass

    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY not found in st.secrets or the environment"
        )
    return key


def get_client() -> anthropic.Anthropic:
    return anthropic.Anthropic(api_key=get_api_key())


def as_blocks(content):
    """cache_control can only be set on a content block, never on the
    message object itself — so plain string content needs wrapping into
    a block before a breakpoint can be attached to it.

    Multimodal content (e.g. an image block plus a text block, built via
    image_block() below) is already a list of blocks and passes through
    unchanged — this is what lets a new message carry an attached image.
    """
    if isinstance(content, str):
        return [{"type": "text", "text": content}]
    return content


def image_block(data: bytes, media_type: str) -> dict:
    """Base64-encoded image content block for the Messages API."""
    return {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": media_type,
            "data": base64.standard_b64encode(data).decode("utf-8"),
        },
    }


def build_request(
    instructions: str,
    reference_bundle: str,
    history: list[dict],
    new_message: str,
    component_type: str,
    max_tokens: int = 8192,
) -> dict:
    """Assemble Messages API kwargs with three cache_control breakpoints:
    end of instructions, end of reference bundle, end of prior conversation.

    No `temperature` param here: claude-opus-4-8 and claude-sonnet-5 reject it
    outright (400 "temperature is deprecated for this model") rather than just
    ignoring a non-default value. The Haiku classification call in
    model_routing.py still sets temperature=0, which that model still accepts.

    max_tokens defaults well above 1024: both models run adaptive thinking by
    default when `thinking` is omitted, and thinking tokens count against
    max_tokens — a tight budget can be consumed entirely by thinking, leaving
    no room for the visible reply (observed directly: stop_reason="max_tokens"
    with an empty text block, first at max_tokens=1024, then again at 4096
    once conversation history grew further — raised to 8192 for the same
    reason; there's no way to cap thinking specifically since budget_tokens
    is rejected on these models when thinking is adaptive, so the only lever
    is giving the combined thinking+text budget more headroom).
    """
    model = select_model(component_type)

    system_blocks = [
        {
            "type": "text",
            "text": instructions,
            "cache_control": {"type": "ephemeral"},
        },
        {
            "type": "text",
            "text": reference_bundle,
            "cache_control": {"type": "ephemeral"},
        },
    ]

    messages = [
        {"role": m["role"], "content": as_blocks(m["content"])} for m in history
    ] + [{"role": "user", "content": as_blocks(new_message)}]

    # Breakpoint on everything up to (not including) the newest message —
    # set on the last content block of the last *prior* message, not on
    # the message dict itself.
    if len(messages) > 1:
        messages[-2]["content"][-1]["cache_control"] = {"type": "ephemeral"}

    return {
        "model": model,
        "max_tokens": max_tokens,
        "system": system_blocks,
        "messages": messages,
    }


def send_marker_message(
    client: anthropic.Anthropic,
    instructions: str,
    reference_bundle: str,
    history: list[dict],
    new_message: str,
    max_tokens: int = 8192,
    classify_text: str | None = None,
) -> dict:
    """Classify the marker's message, route to the right model, and call
    the Messages API. Returns the component_type, model used, and the raw
    API response (for callers to pull usage/content from).

    `classify_text` lets a caller send a different (always plain-text)
    string to the Haiku classification call than what's actually sent as
    the message content — needed when `new_message` is a multimodal block
    list (e.g. an attached image) rather than a plain string, since
    classification only ever looks at text. Defaults to `new_message`.
    """
    component_type = classify_component_type(client, classify_text if classify_text is not None else new_message)
    request = build_request(
        instructions, reference_bundle, history, new_message, component_type, max_tokens
    )
    response = client.messages.create(**request)
    return {
        "component_type": component_type,
        "model": request["model"],
        "response": response,
    }


def stream_marker_message(
    client: anthropic.Anthropic,
    instructions: str,
    reference_bundle: str,
    history: list[dict],
    new_message: str,
    on_delta: Callable[[str], None],
    should_stop: Callable[[], bool],
    max_tokens: int = 8192,
    classify_text: str | None = None,
    forced_component_type: str | None = None,
) -> dict:
    """Classify + route, then stream the main call so a caller can show
    incremental text and cooperatively cancel mid-generation (a "Stop"
    button in the UI).

    `on_delta(accumulated_text)` is called after every streamed text chunk.
    `should_stop()` is checked before streaming starts and after every raw
    stream event — not just text ones — when it returns True, the stream is
    closed early rather than read to completion.

    `classify_text` — see send_marker_message() above; same purpose here.

    `forced_component_type` skips the Haiku classification call entirely
    and uses this value directly — for callers that already have a certain
    signal of what the content is (e.g. an uploaded .ipynb's extension is
    a certain signal for "python_code", per docs/implementation_notes.md).

    Checking on every raw event (not just text deltas) matters: both
    models run adaptive thinking by default, and the thinking phase can
    run many seconds before the first *text* delta arrives — a should_stop
    check placed only inside the text loop would silently not fire for the
    entire thinking phase, leaving a Stop button unresponsive for however
    long the model spent thinking (observed directly: 20+ seconds).
    Thinking deltas arrive as their own stream events well before that, so
    checking per-event closes that gap.

    Returns component_type, model, the text accumulated so far, whether
    generation was stopped early, and usage (None if stopped, since a
    partially-consumed stream has no final usage total to read).
    """
    if forced_component_type is not None:
        component_type = forced_component_type
    else:
        component_type = classify_component_type(client, classify_text if classify_text is not None else new_message)
    request = build_request(instructions, reference_bundle, history, new_message, component_type, max_tokens)
    model = request["model"]

    text_parts: list[str] = []
    stopped = should_stop()
    usage = None
    stop_reason = None

    if not stopped:
        with client.messages.stream(**request) as stream:
            for event in stream:
                if should_stop():
                    stopped = True
                    break
                if event.type == "content_block_delta" and event.delta.type == "text_delta":
                    text_parts.append(event.delta.text)
                    on_delta("".join(text_parts))
            if not stopped:
                final_message = stream.get_final_message()
                usage = final_message.usage
                stop_reason = final_message.stop_reason

    return {
        "component_type": component_type,
        "model": model,
        "text": "".join(text_parts),
        "stopped": stopped,
        "stop_reason": stop_reason,
        "usage": usage,
    }
