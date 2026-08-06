"""Stage 2 smoke test: classify -> route -> call, run against the real
Claude API. Not part of the app; run manually with:

    python scripts/test_stage2_api_flow.py

Sends an obvious DAX-formula message twice (same content, no history) and
checks:
  - it classifies as "dax_formula" and routes to Opus
  - the second call, within 5 minutes of the first, shows a nonzero
    cache_read_input_tokens (the system prompt / reference bundle blocks
    cached from the first call)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.api_client import get_client, load_reference_bundle, load_system_instructions, send_marker_message
from src.model_routing import OPUS_MODEL

DAX_MESSAGE = (
    "Can you check this DAX formula for the Total Sales measure?\n\n"
    "Total Sales = SUMX(RELATEDTABLE(Sales), Sales[Quantity] * Sales[UnitPrice])\n\n"
    "I used CALCULATE and RELATED elsewhere in the model too. Does this look right "
    "for the scenario's fact/dimension structure?"
)


def run_once(client, instructions, reference_bundle, label):
    result = send_marker_message(client, instructions, reference_bundle, history=[], new_message=DAX_MESSAGE)
    response = result["response"]
    usage = response.usage

    print(f"\n--- {label} ---")
    print(f"component_type:            {result['component_type']}")
    print(f"model_used:                 {result['model']}")
    print(f"response (first 300 chars): {response.content[0].text[:300]!r}")
    print(f"input_tokens:               {usage.input_tokens}")
    print(f"output_tokens:              {usage.output_tokens}")
    print(f"cache_creation_input_tokens: {usage.cache_creation_input_tokens}")
    print(f"cache_read_input_tokens:    {usage.cache_read_input_tokens}")
    return result, usage


def main():
    client = get_client()
    instructions = load_system_instructions()
    reference_bundle = load_reference_bundle()

    print(f"Loaded system_instructions.md: {len(instructions)} chars")
    print(f"Loaded reference bundle:       {len(reference_bundle)} chars")
    assert "staff_id" not in reference_bundle, "roster.csv content leaked into reference bundle!"

    first_result, first_usage = run_once(client, instructions, reference_bundle, "Call 1 (cold cache)")
    assert first_result["component_type"] == "dax_formula", (
        f"expected dax_formula, got {first_result['component_type']!r}"
    )
    assert first_result["model"] == OPUS_MODEL, (
        f"expected {OPUS_MODEL}, got {first_result['model']!r}"
    )
    print("\nPASS: DAX formula input classified as dax_formula and routed to Opus")

    second_result, second_usage = run_once(client, instructions, reference_bundle, "Call 2 (should hit cache)")
    assert second_usage.cache_read_input_tokens > 0, (
        "expected nonzero cache_read_input_tokens on the second call within 5 minutes"
    )
    print(f"\nPASS: second call shows cache_read_input_tokens = {second_usage.cache_read_input_tokens}")

    print("\nALL STAGE 2 CHECKS PASSED")


if __name__ == "__main__":
    main()
