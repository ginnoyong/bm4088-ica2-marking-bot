"""Haiku pre-classification and model routing.

Classification happens once per marker message, before the real (Sonnet
or Opus) call is made. No marker-facing component-type selector — the
component_type used for logging comes from classify_component_type(),
never from user input.
"""

import anthropic

HAIKU_MODEL = "claude-haiku-4-5-20251001"
OPUS_MODEL = "claude-opus-4-8"
SONNET_MODEL = "claude-sonnet-5"

COMPONENT_TYPES = (
    "problem_statement",
    "hypotheses",
    "cleansing",
    "dax_formula",
    "eda_chart_config",
    "python_code",
    "predictive_analytics_text",
    "conclusion",
    "other",
)

_CLASSIFY_SYSTEM_PROMPT = (
    "Classify the following marker input into exactly one of these "
    f"categories: {', '.join(COMPONENT_TYPES)}. Respond with only the "
    "category string, nothing else."
)


def classify_component_type(client: anthropic.Anthropic, marker_input: str) -> str:
    """One cheap Haiku call to decide routing before the real request.

    Returns one of the strings in COMPONENT_TYPES. Falls back to "other"
    if the model returns something unexpected, rather than raising.
    """
    response = client.messages.create(
        model=HAIKU_MODEL,
        max_tokens=20,
        temperature=0,
        system=_CLASSIFY_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": marker_input}],
    )
    classification = response.content[0].text.strip()
    if classification not in COMPONENT_TYPES:
        return "other"
    return classification


def select_model(component_type: str) -> str:
    """dax_formula and python_code go to Opus; everything else to Sonnet."""
    if component_type in ("dax_formula", "python_code"):
        return OPUS_MODEL
    return SONNET_MODEL
