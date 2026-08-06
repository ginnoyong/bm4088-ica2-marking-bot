"""Parses the per-response scorecard table out of assistant responses and
maintains the cumulative three-column (Criterion, Grade, Status) sidebar
tracker described in system_instructions.md's Running scorecard section.

Parsing approach is deliberately simple row-splitting on "|" matched
against the exact expected header — not a general markdown parser — the
same philosophy as the app's issue_flag/issue_type detection: pattern-match
against response text the model reliably produces in a consistent format.
"""

import re

# The model's own header cell varies between "Criterion" (the literal table
# example in system_instructions.md) and "Criterion/Component" (what it
# actually produces live — the "Criterion/Component X.Y" row-labelling
# instruction generalises to the column header itself) — both accepted,
# still an exact-set match, not a fuzzy one.
_HEADER_FIRST_CELL_OPTIONS = ("Criterion", "Criterion/Component")
_TRAILING_HEADER_CELLS = ("Grade", "Status", "Comments")

# "3.1", "4.2", or "3.1 (EDA #2)" — the disambiguated form system_instructions.md
# requires for Criterion 3's per-EDA-entry lines (3.1/3.2/3.3).
_CRITERION_PATTERN = re.compile(r"^(\d+)\.(\d+)(?:\s*\(EDA\s*#(\d+)\))?$")


def _split_row(line: str) -> list[str] | None:
    """Split one markdown table row on "|" into its cell values, or None
    if the line isn't a table row at all."""
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return None
    return [cell.strip() for cell in stripped[1:-1].split("|")]


def _is_separator_row(cells: list[str]) -> bool:
    """The "|---|---|---|---|" row under the header."""
    return all(re.fullmatch(r":?-+:?", cell) for cell in cells)


def parse_scorecard_rows(response_text: str) -> list[dict[str, str]]:
    """Find the "| Criterion | Grade | Status | Comments |" table (or its
    "Criterion/Component" header variant — see _HEADER_FIRST_CELL_OPTIONS)
    in a response and return its data rows as {"criterion", "grade",
    "status"} dicts (Comments dropped). Returns [] if no such table is
    present.
    """
    rows: list[dict[str, str]] = []
    in_table = False

    for line in response_text.splitlines():
        cells = _split_row(line)
        if cells is None:
            if in_table:
                break  # table block ended
            continue

        if not in_table:
            if len(cells) == 4 and cells[0] in _HEADER_FIRST_CELL_OPTIONS and tuple(cells[1:]) == _TRAILING_HEADER_CELLS:
                in_table = True
            continue

        if _is_separator_row(cells):
            continue
        if len(cells) != 4:
            break  # malformed row — stop rather than misparse

        criterion, grade, status, _comments = cells
        if criterion:
            rows.append({"criterion": criterion, "grade": grade, "status": status})

    return rows


def update_scorecard(scorecard: dict[str, dict[str, str]], response_text: str) -> None:
    """Upsert `scorecard` (keyed by exact Criterion cell text) in place
    from the scorecard table in `response_text`, if any — a new key adds
    an entry, an existing key overwrites its Grade/Status. A response
    with no table leaves `scorecard` unchanged."""
    for row in parse_scorecard_rows(response_text):
        scorecard[row["criterion"]] = {"grade": row["grade"], "status": row["status"]}


def _sort_key(criterion: str) -> tuple:
    match = _CRITERION_PATTERN.match(criterion)
    if not match:
        return (99, 0, 0, criterion)  # unrecognised form — keep, sort to the end

    major, minor, eda = match.groups()
    major, minor = int(major), int(minor)
    eda_group = int(eda) if eda is not None else 0
    # Criterion 3 groups by EDA entry first, then by subline (3.1/3.2/3.3)
    # within that entry — every other criterion has no EDA grouping.
    group = eda_group if major == 3 else 0
    return (major, group, minor, "")


def _status_word(status: str) -> str:
    """Just the leading state word for the sidebar — "Provisional —
    pending filter confirmation" becomes "Provisional"; a bare "Complete"
    (no dash) passes through unchanged. The full text (with reason clause)
    stays in the scorecard dict itself — only this sidebar-facing view
    is shortened."""
    return status.split(" — ", 1)[0].strip()


def sorted_scorecard_rows(scorecard: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    """Scorecard entries in rubric order — 1.1, 1.2, 2.1, 2.2, then
    3.1/3.2/3.3 per EDA entry in order, 4.1, 4.2, 4.3, 5.1, 5.2, 5.3 —
    not insertion order. Each item includes its own Criterion label."""
    return [
        {"Criterion": criterion, "Grade": values["grade"], "Status": _status_word(values["status"])}
        for criterion, values in sorted(scorecard.items(), key=lambda item: _sort_key(item[0]))
    ]
