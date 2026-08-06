"""Staff login gate: staff ID matched against a roster maintained in a
Google Sheet (see ROSTER_SHEET_ID / ROSTER_SHEET_NAME in secrets).

Runs entirely at the app layer, before the chat interface is reachable.
The model plays no role in authentication.
"""

import gspread


def load_roster(worksheet: gspread.Worksheet) -> set[str]:
    """Read the staff_id column from the roster worksheet into a set of
    valid IDs."""
    header = worksheet.row_values(1)
    if "staff_id" not in header:
        raise ValueError(
            f"Roster sheet '{worksheet.title}' is missing required 'staff_id' column"
        )
    records = worksheet.get_all_records()
    return {
        str(row["staff_id"]).strip()
        for row in records
        if row.get("staff_id") and str(row["staff_id"]).strip()
    }


def is_authorized(staff_id: str, worksheet: gspread.Worksheet) -> bool:
    """Check a staff ID against the roster. Case-sensitive, whitespace-trimmed."""
    staff_id = (staff_id or "").strip()
    if not staff_id:
        return False
    return staff_id in load_roster(worksheet)
