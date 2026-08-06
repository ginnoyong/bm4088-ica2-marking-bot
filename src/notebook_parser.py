"""Parses an uploaded .ipynb file into plain text for the Messages API.

Extracts cell source (code and markdown) and any saved text-based output
already embedded in code cells (stream output, printed/returned values).
Image outputs (plots) are skipped for now — out of scope per the goal this
was built against.
"""

import json


def _source_text(cell: dict) -> str:
    source = cell.get("source", "")
    if isinstance(source, list):
        return "".join(source)
    return source


def _output_text(output: dict) -> str | None:
    """Text for one saved output entry, or None if it's not one of the two
    text-based output types this parser handles (stream, execute_result) —
    e.g. a display_data image/plot output is left out entirely."""
    output_type = output.get("output_type")
    if output_type == "stream":
        text = output.get("text", "")
    elif output_type == "execute_result":
        text = output.get("data", {}).get("text/plain")
    else:
        return None
    if text is None:
        return None
    return "".join(text) if isinstance(text, list) else text


def parse_notebook(raw_bytes: bytes) -> str:
    """Parse a .ipynb file's JSON structure into plain text, with clear
    delimiters so cell boundaries and embedded outputs are distinguishable
    from each other and from the marker's own accompanying message.
    """
    notebook = json.loads(raw_bytes.decode("utf-8"))
    cells = notebook.get("cells", [])
    total = len(cells)

    parts = [f"=== NOTEBOOK ({total} cells) ==="]
    for i, cell in enumerate(cells, start=1):
        cell_type = cell.get("cell_type", "unknown")
        source = _source_text(cell).strip()
        parts.append(f"--- Cell {i}/{total} [{cell_type}] ---\n{source or '(empty cell)'}")

        if cell_type == "code":
            for output in cell.get("outputs", []):
                output_text = _output_text(output)
                if output_text and output_text.strip():
                    parts.append(f"--- Output (Cell {i}/{total}) ---\n{output_text.strip()}")

    parts.append("=== END NOTEBOOK ===")
    return "\n\n".join(parts)
