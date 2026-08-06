"""Staff login gate: staff ID matched against reference/roster.csv.

Runs entirely at the app layer, before the chat interface is reachable.
The model plays no role in authentication.
"""

import csv
from pathlib import Path

ROSTER_PATH = Path(__file__).resolve().parent.parent / "reference" / "roster.csv"


def load_roster(roster_path: Path = ROSTER_PATH) -> set[str]:
    """Read the staff_id column from roster.csv into a set of valid IDs."""
    if not roster_path.exists():
        raise FileNotFoundError(f"Roster file not found at {roster_path}")

    with roster_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None or "staff_id" not in reader.fieldnames:
            raise ValueError(
                f"Roster file at {roster_path} is missing required 'staff_id' column"
            )
        return {
            row["staff_id"].strip()
            for row in reader
            if row.get("staff_id") and row["staff_id"].strip()
        }


def is_authorized(staff_id: str, roster_path: Path = ROSTER_PATH) -> bool:
    """Check a staff ID against the roster. Case-sensitive, whitespace-trimmed."""
    staff_id = (staff_id or "").strip()
    if not staff_id:
        return False
    return staff_id in load_roster(roster_path)
