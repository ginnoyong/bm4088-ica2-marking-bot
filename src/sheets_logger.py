"""Per-turn Google Sheets logging via a service account.

One row per turn, lightweight (no verbatim student text, bands, or scores)
— see docs/implementation_notes.md "Suggested Google Sheet columns".
"""

import re
from datetime import datetime, timezone

import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
]

WORKSHEET_TITLE = "Log"

COLUMNS = [
    "timestamp",
    "staff_id",
    "session_id",
    "scenario_number",
    "component_type",
    "model_used",
    "input_tokens",
    "output_tokens",
    "cache_read_tokens",
    "cache_write_tokens",
    "summary",
    "issue_flag",
    "issue_type",
]

# Grounded in the actual recurring phrasing in prompts/system_instructions.md
# ("Requesting missing input", the DAX/Python module's stop-and-ask behaviour,
# the "route to the human marker" out-of-scope phrasing, and the Manage
# Relationships flag-for-verification language) — matched loosely since this
# is model-generated prose, not a fixed string.
_RESPONSE_PATTERNS = [
    (
        "out_of_scope_request",
        re.compile(r"rout(?:e|es|ed|ing)\s+(?:this\s+)?to\s+the\s+human\s+marker|out\s+of\s+scope", re.I),
    ),
    (
        # Marking Principle 6: submitted content containing embedded
        # instructions to the model, flagged rather than complied with.
        "possible_prompt_injection",
        re.compile(
            r"embedded\s+(?:text|instructions?)\s+attempt(?:ing|ed)?\s+to\s+direct"
            r"|attempt(?:ing|ed)?\s+to\s+(?:direct|instruct)\s+the\s+assessment"
            r"|contained\s+(?:text|an?\s+instruction)\s+attempting\s+to\s+direct",
            re.I,
        ),
    ),
    (
        # Marking Principle 7: marker asked for a specific band/score without
        # rubric support; bot states the rubric-grounded assessment instead.
        "marker_override_declined",
        re.compile(
            r"assessment\s+the\s+rubric\s+(?:actually\s+)?supports"
            r"|rubric\s+doesn'?t\s+support\s+that"
            r"|(?:can'?t|won'?t)\s+(?:award|give|mark\s+it\s+as)\s+(?:that|the\s+requested)\s+band",
            re.I,
        ),
    ),
    (
        # DAX module step 7: the marker's typed field-well description turns
        # out not to match what the supplied chart screenshot actually shows.
        "screenshot_description_mismatch",
        re.compile(
            r"screenshot\s+(?:doesn'?t\s+match|disagrees?\s+with|differs?\s+from|contradicts?)"
            r"\s+(?:the\s+)?(?:typed\s+|described\s+)?(?:configuration|description)"
            r"|(?:description|configuration)\s+(?:you\s+)?(?:typed|described|gave|supplied)"
            r".{0,60}?(?:doesn'?t\s+match|disagrees?\s+with|differs?\s+from|contradicts?)\s+(?:the\s+)?screenshot",
            re.I,
        ),
    ),
    (
        # DAX module step 7: the formula-logic verdict and the screenshot's
        # visual cross-check are reported as disagreeing with each other.
        "insight_visual_mismatch",
        re.compile(
            r"screenshot\s+cross-check\s+(?:disagrees?\s+with|contradicts?|differs?\s+from)\s+(?:the\s+)?formula"
            r"|formula(?:-based)?\s+verdict\s+.{0,60}?screenshot\s+(?:cross-check\s+)?"
            r"(?:disagrees?|shows?\s+something\s+(?:different|else)|contradicts?)"
            r"|formula\s+logic\s+is\s+correct\s+but\s+the\s+screenshot",
            re.I,
        ),
    ),
    (
        # DAX module steps 6-7 / Marking Principle 4: 3.1's implementation
        # verdict and 3.2's accuracy verdict, drawn from the same formula, are
        # reported as pointing in different directions — expected per the
        # module ("these two verdicts can genuinely disagree"), not an error.
        "implementation_accuracy_divergence",
        re.compile(
            r"implementation\s+verdict\s+.{0,60}?(?:diverges?\s+from|disagrees?\s+with|differs?\s+from|contradicts?)\s+.{0,10}?(?:the\s+)?accuracy\s+verdict"
            r"|accuracy\s+verdict\s+.{0,60}?(?:diverges?\s+from|disagrees?\s+with|differs?\s+from|contradicts?)\s+.{0,10}?(?:the\s+)?implementation\s+verdict"
            r"|correctly\s+implemented\s+but\s+(?:the\s+)?(?:insight\s+|report'?s\s+)?(?:doesn'?t\s+match|does\s+not\s+match|is\s+a\s+(?:partial\s+)?mismatch)"
            r"|implementation\s+(?:verdict\s+)?(?:is\s+)?(?:correct|sound)\s+but\s+(?:the\s+)?accuracy\s+verdict\s+is\s+a?\s*(?:partial\s+)?mismatch",
            re.I,
        ),
    ),
    (
        "relationship_ambiguity",
        re.compile(
            r"flagged?\s+for\s+the\s+marker\s+to\s+verify|verify\s+in\s+manage\s+relationships"
            r"|cross[- ]filter\s+direction",
            re.I,
        ),
    ),
    (
        "unresolved_dependency",
        re.compile(
            r"unresolved\s+dependency|resolve\s+(?:the\s+)?(?:full\s+)?dependency\s+chain"
            r"|dependency\s+chain\s+couldn'?t\s+be\s+fully\s+resolved",
            re.I,
        ),
    ),
    (
        "missing_context",
        re.compile(
            r"could\s+you\s+(?:paste|provide|describe|share|confirm|clarify)"
            r"|i\s+(?:still\s+)?need\s+the\b|before\s+i\s+can\s+(?:complete|assess|finish)"
            r"|i\s+have\s+to\s+stop\s+(?:here|before)",
            re.I,
        ),
    ),
]

_DAX_PATTERN = re.compile(r"\bCALCULATE\s*\(|\bRELATED\s*\(|\bRELATEDTABLE\s*\(|\bSUMX\s*\(|\bCALCULATETABLE\s*\(", re.I)
_PYTHON_PATTERN = re.compile(r"\bimport\s+pandas\b|\bimport\s+sklearn\b|\bfrom\s+sklearn\b|```python", re.I)


def get_client(service_account_info: dict) -> gspread.Client:
    creds = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
    return gspread.authorize(creds)


def get_worksheet(client: gspread.Client, sheet_id: str, worksheet_title: str = WORKSHEET_TITLE) -> gspread.Worksheet:
    spreadsheet = client.open_by_key(sheet_id)
    return spreadsheet.worksheet(worksheet_title)


def derive_summary(marker_input: str, component_type: str, max_len: int = 80) -> str:
    """Short description of the turn — a truncation of the marker's input,
    never the model's full response (keeps the log lightweight, per design)."""
    flattened = " ".join(marker_input.split())
    if len(flattened) > max_len:
        flattened = flattened[: max_len - 1].rstrip() + "…"
    return f"[{component_type}] {flattened}"


def classify_issue(response_text: str, marker_input: str, component_type: str) -> tuple[str, str]:
    """Plain pattern matching against the response text (most cases) plus one
    regex check of the marker's own input against Haiku's classification
    (possible_component_mismatch). Never blocks or alters routing — log-only.
    """
    for issue_type, pattern in _RESPONSE_PATTERNS:
        if pattern.search(response_text):
            return "yes", issue_type

    dax_like = bool(_DAX_PATTERN.search(marker_input))
    python_like = bool(_PYTHON_PATTERN.search(marker_input))
    if (dax_like and component_type != "dax_formula") or (
        python_like and component_type != "python_code"
    ):
        return "yes", "possible_component_mismatch"

    return "no", ""


def build_row(
    staff_id: str,
    session_id: str,
    scenario_number: int,
    component_type: str,
    model_used: str,
    usage,
    marker_input: str,
    response_text: str,
) -> list:
    issue_flag, issue_type = classify_issue(response_text, marker_input, component_type)
    return [
        datetime.now(timezone.utc).isoformat(),
        staff_id,
        session_id,
        scenario_number,
        component_type,
        model_used,
        usage.input_tokens,
        usage.output_tokens,
        usage.cache_read_input_tokens,
        usage.cache_creation_input_tokens,
        derive_summary(marker_input, component_type),
        issue_flag,
        issue_type,
    ]


def log_turn(
    worksheet: gspread.Worksheet,
    staff_id: str,
    session_id: str,
    scenario_number: int,
    component_type: str,
    model_used: str,
    usage,
    marker_input: str,
    response_text: str,
) -> None:
    row = build_row(
        staff_id, session_id, scenario_number, component_type, model_used, usage, marker_input, response_text
    )
    worksheet.append_row(row, value_input_option="RAW")
