# Implementation Notes (Developer / Architecture)

Not sent to the model — this is for whoever builds the custom API-backed tool.

## File structure

```
/prompts/system_instructions.md      — process, principles, modules (changes rarely)
/reference/rubric_descriptors.md     — full verbatim A–F descriptor text + weights, per line index
/reference/scenario_descriptions.md  — Appendix E scenario text, ground truth for 1.1
/reference/table_relationships.md    — the static relationship reference
/reference/data_dictionary.md        — column definitions, converted from the xlsx
/reference/tutor_guide_data_issues.md      — Part 1, authoritative for 2.2 cleansing
/reference/tutor_guide_scenario_analytics_ref.md   — Part 2, plausibility-only
/reference/data_viz_principles.md    — taught framework grounding 3.3
/reference/marking_notes.md          — copied in, included in the bundle
```

Reference files change on their own cycle (e.g. the mid-project Requirement 5 weight tweak) — separating them from `system_instructions.md` means a rubric edit doesn't require touching or re-reviewing the instructions file, and vice versa. It also means a rubric-only edit only invalidates the reference-block cache breakpoint, not the larger, more stable instructions block ahead of it (see Prompt caching below).

## Deployment shape

Custom front end calling the Anthropic Messages API directly, one persistent UI element and two models in rotation.

## UI: submission-complete control

Not achievable inside a standard Claude.ai Project chat — this requires the custom front end. Suggested copy, kept to the shorter version:

> Finished this submission? **Start New Submission**

Behaviour: clicking it starts a genuinely new conversation (fresh message array, not just a case-file reset instruction sent to the model) — this is what actually reclaims the token/context cost, not the in-conversation reset behaviour described in `system_instructions.md`'s Session Handling section. Keep the in-conversation reset logic as a fallback for markers who don't click the button and instead just start describing a new group mid-thread.

## Model routing

| Trigger | Model |
|---|---|
| Classified as DAX formula content | Opus (`claude-opus-4-8`) |
| Classified as Python code content | Opus (`claude-opus-4-8`) |
| Everything else (problem statement, hypotheses, schema description, cleansing narrative, chart config without DAX, chart formatting, predictive analytics text, report structure, dashboard design, conclusion, general Q&A, the opening orientation) | Sonnet (`claude-sonnet-5`) |

**Routing is automatic, via a cheap Haiku pre-classification call — no marker-facing selector.** An earlier version of this design had the marker pick a component type before each message; that turned out to create its own failure mode (mis-selection, requiring a pre-send warning and a log flag to catch it). Since the bot already recognises what kind of input it's looking at from content alone once a model is processing it, the natural fix is to make that recognition happen *before* the real call too, using a fast, cheap model purely for classification — the same shape as Claude Code's own `/goal` evaluator: a lightweight model makes the judgment call, a stronger model does the work.

```python
def classify_component_type(client: anthropic.Anthropic, marker_input: str) -> str:
    """One cheap Haiku call to decide routing before the real request.
    Returns one of the category strings below."""
    categories = (
        "problem_statement, hypotheses, schema_description, cleansing, "
        "dax_formula, eda_chart_config, python_code, "
        "predictive_analytics_text, report_structure, conclusion, other"
    )
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=20,
        temperature=0,
        system=(
            "Classify the following marker input into exactly one of these "
            f"categories: {categories}. Respond with only the category "
            "string, nothing else."
        ),
        messages=[{"role": "user", "content": marker_input}],
    )
    return response.content[0].text.strip()

def select_model(component_type: str) -> str:
    if component_type in ("dax_formula", "python_code"):
        return "claude-opus-4-8"
    return "claude-sonnet-5"
```

**Deterministic shortcut for `.ipynb` uploads.** If the marker's message includes an uploaded `.ipynb` file, skip `classify_component_type()` entirely and set `component_type = "python_code"` directly — the file extension alone is a certain signal, per `system_instructions.md`'s note that a full notebook is only ever expected for Requirement 4. This saves a Haiku call on every notebook-upload turn and removes any chance of a misclassification on what's already unambiguous.

Since a single conversation touches multiple modules across turns (a marker might check a DAX formula, then the problem statement, then some Python code), classify and route per API call, not once per conversation. Model IDs above are current at time of writing — confirm against docs.claude.com before deploying, since the catalog changes.

**QA visibility, not a marker-facing warning.** Because classification now happens automatically, there's no marker action to double-check before sending. What's still worth keeping is a cheap secondary signal for auditing classifier accuracy over time: run the same simple regex patterns (`CALCULATE(`, `RELATED(`, `SUMX(` for DAX; `import pandas`, `sklearn`, a ```` ```python ```` fence for Python) against the input, and if they disagree with what Haiku classified it as, log `issue_type = possible_component_mismatch`. This never blocks or overrides anything — Haiku's classification is what actually drove routing — it's purely a way to notice if the classifier is drifting or getting specific patterns wrong often enough to warrant a closer look.

## Prompt caching

Three cache breakpoints are worth setting now that instructions and reference data are split, using the standard `cache_control: {"type": "ephemeral"}` marker (up to 4 breakpoints are allowed per request):

1. **End of `system_instructions.md`.** The most stable block — changes rarely, so this cache stays valid across rubric or reference-data edits.
2. **End of the concatenated `/reference/*.md` bundle.** Identical across all 140 groups, but on its own cycle — a rubric weight tweak (like the one just made to Requirement 5) invalidates this breakpoint without touching the instructions cache above it.
3. **End of the conversation so far, on each turn.** This caches the growing per-group transcript incrementally — each new API call only pays full price for the newest message, and everything before it in that conversation is a cache read rather than a full resend. This is what solves the "whole prior transcript gets resent every turn" problem — it's a bigger lever within a single group's session than trimming the static content further would be.

```python
import anthropic

client = anthropic.Anthropic()

# select_model() and classify_component_type() are defined in the Model
# routing section above — combine all three into the same module. Call
# classify_component_type() first on the marker's new_message, then pass
# its result in here as component_type.

def as_blocks(content):
    """cache_control can only be set on a content block, never on the
    message object itself — so plain string content needs wrapping
    into a block before a breakpoint can be attached to it."""
    if isinstance(content, str):
        return [{"type": "text", "text": content}]
    return content

def build_request(instructions: str, reference_bundle: str, history: list[dict], new_message: str, component_type: str):
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

    # Cache breakpoint: everything up to (not including) the newest message —
    # set on the last content block of the last *prior* message, not on the
    # message dict itself.
    if len(messages) > 1:
        messages[-2]["content"][-1]["cache_control"] = {"type": "ephemeral"}

    # max_tokens=8192 — the required output format (object/
    # dependencies, relationship assumptions, visual context, verdict,
    # screenshot cross-check, mandatory justification, scorecard update)
    # is genuinely long for a full 3.1+3.2 check, and scope has roughly
    # doubled since 4096 was set (13 line-types now, several combined-
    # verdict, e.g. 5.3). Since Stage 9 parses this table for the
    # sidebar, a truncated response now corrupts two things, not one —
    # worth the extra headroom. max_tokens is a ceiling, not a target,
    # so this costs nothing on shorter turns.
    return client.messages.create(
        model=model,
        max_tokens=8192,
        temperature=0,
        system=system_blocks,
        messages=messages,
    )
```

`temperature=0` is deliberate, not a default left in place — for a marking assistant, minimizing run-to-run variance in band/score recommendations matters more than response variety. Two markers (or the same marker twice) checking the same formula against the same insight should get materially the same verdict, not a different one depending on sampling. This doesn't guarantee bit-for-bit identical output, but it removes the biggest source of avoidable inconsistency.

`reference_bundle` is the concatenation of every `.md` file under `/reference/` at app startup (or on a file-change trigger) — read files from disk as separate files per the structure above, don't hardcode their content into the application code, so an edit to any one reference file doesn't require a code change or redeploy. There's no roster or other auth data under `/reference/` to accidentally sweep in here — the roster lives in a separate Google Sheet entirely, structurally outside anything this loader ever touches (see Access control below).

Default cache TTL is 5 minutes, refreshed on each read — fine for normal back-and-forth marking pace. If a marker's turns are regularly slower than that (e.g. they step away mid-assessment), the 1-hour cache option is available at a higher one-time write cost, worth it only if cache misses from the 5-minute TTL turn out to be common in practice.

## Sidebar scorecard

A compact, always-visible tracker rendered in the sidebar below the "How to use this bot" button from Stage 6, showing the cumulative state of every line touched so far in the current session. **This is deliberately not identical to the chat's summary table** — it's a minimal glance-view, reduced to only what fits comfortably in a narrow sidebar: Grade (band and score) and a bare Status word. No Criterion-column reasons, no Comments, none of the Status reason clause ("pending filter confirmation," etc.) — for any of that detail, the marker goes to the chat, where the full four-column table with everything already lives. Widening the sidebar and wrapping cell text were tried first and didn't fully solve the space problem; reducing what's shown is the more robust fix.

**Rendered via `st.dataframe`, not `st.table` or raw markdown.** `st.dataframe`'s built-in hover toolbar (download as CSV, search, fullscreen expand) is worth keeping — use `st.column_config` to control column width and enable cell text wrapping rather than switching to a different widget to solve layout problems, which would silently sacrifice the toolbar.

**How it's populated:** after every assistant response, parse the response text for the markdown summary table `system_instructions.md` requires (header `| Criterion | Grade | Status | Comments |`). For each row found, extract Criterion and Grade as-is, and Status reduced to just its leading state word — split on the em dash separator (` — `) and keep only what's before it, so `"Provisional — pending filter confirmation"` becomes `"Provisional"` for the sidebar; a plain `"Complete"` with no dash stays as-is. Comments is dropped entirely, same as before. Upsert into a session-state dict keyed by the Criterion cell's exact text (e.g. `"3.1 (EDA #1)"`, `"4.2"`) — a new key adds a row, an existing key overwrites its Grade/Status with the latest values. This is why the EDA-entry disambiguation in `system_instructions.md`'s Output format section matters mechanically, not just for readability: without it, all four EDA entries' 3.1 rows would collide on the same key and silently overwrite each other.

**Parsing approach:** simple markdown-table parsing (split rows on `|`, match against the expected header), the same philosophy as the `issue_flag`/`issue_type` detection in the Logging section below — pattern-matching against response text that the model reliably produces in a consistent format, not a separate structured/hidden output channel. If a response has no table (a purely conversational reply), leave the sidebar state unchanged.

**Display order:** sort rows in rubric order (1.1, 1.2, 2.1, 2.2, 3.1/3.2/3.3 per EDA entry in order, 4.1, 4.2, 4.3, 5.1, 5.2, 5.3), not insertion order — a marker scanning the sidebar should see something that reads like the marking sheet, not a log of whatever order they happened to check things in.

**Reset behaviour:** cleared on "Start New Submission," same as every other piece of per-submission state (per New-submission reset below) — never carries a previous group's rows into a new one.

## Access control (staff roster) and logging

Staff ID is real access control, not just a logging label — entered staff ID must be matched against a Google Sheet named "roster" (single `staff_id` column, one authorized ID per row) to determine whether access is granted at all. No access code or password layered on top — a match against this sheet is the only check. This changes the recommended architecture:

**Authentication must happen at the app layer, before the chat session is reachable — not inside the conversation.** The model has no way to verify a staff ID against anything and shouldn't be asked to gate access via conversation; a determined user could simply type past a conversational check. The correct flow:

1. Marker enters staff ID in a login-style UI field (not the chat itself).
2. App queries the "roster" Google Sheet live, via the Sheets API, checking whether the entered ID appears in the `staff_id` column — not cached, not read once at startup, a fresh check on every login attempt. This means adding or removing a staff member takes effect immediately, no redeploy needed.
3. On no match: access denied, chat interface never loads, no API call is made (and no tokens spent on an unauthorized attempt).
4. On match: a session token is issued, the chat interface becomes reachable, and the validated staff ID is attached to every subsequent API call's logging metadata automatically.

**Live checking introduces a failure mode a local file never had: the Sheets API itself can fail or be slow.** A local CSV read essentially never errors; a network call to Google Sheets can time out, hit a rate limit, or fail if the service account's access to the sheet is misconfigured. Handle this explicitly — a failed roster check should show a clear, retryable error to the marker ("couldn't verify access, try again"), never a raw exception, and never silently deny access in a way that looks identical to "your ID isn't on the roster" when the actual cause was a transient API failure. This uses the same service account and Sheets API access already set up for logging (see below) — no new Google Cloud setup beyond creating the sheet itself and sharing it with the service account, but it does mean login now depends on that service account's credentials being valid, same as logging does.

`system_instructions.md`'s Opening Message no longer asks for staff ID conversationally — if the tool is deployed this way, the model never needs to know staff ID wasn't yet established, because it always will be by the time a conversation starts.

### Identifiers

- `scenario_number` (1–6) — the business scenario type. Shared across roughly 23 groups each. Drives the cleansing table, relationship reference, and Appendix E lookups. Required before 1.1 can be assessed at all — capture via the app's UI selector.
- `session_id` — one specific conversation, generated by the app. Within a single session, "which submission" is already structurally guaranteed by Session Handling's reset behaviour (one conversation = one submission at a time) — no separate submission identifier is tracked. A submission split or reassessed across multiple sessions shows up in the log as unrelated sessions; that's an accepted tradeoff, not a gap to solve, since it only costs some manual reconstruction in the rare case it's needed, and nothing in the bot's actual marking logic depends on cross-session linkage.

### Suggested Google Sheet columns (lightweight)

Per-turn logging, kept to a summary/health-monitoring level rather than a full audit trail of every recommendation — no need to store detailed bands, scores, or verbatim excerpts of student work in the log.

| Column | Purpose |
|---|---|
| `timestamp` | ISO 8601 |
| `staff_id` | Validated against the roster at login, per above |
| `session_id` | Unique per conversation |
| `scenario_number` | 1–6, the business scenario type |
| `component_type` | `dax_formula` / `python_code` / `problem_statement` / etc. |
| `model_used` | `claude-opus-4-8` or `claude-sonnet-5` |
| `input_tokens`, `output_tokens` | From the API response's `usage` object |
| `cache_read_tokens`, `cache_write_tokens` | From `usage.cache_read_input_tokens` / `usage.cache_creation_input_tokens` |
| `stop_reason` | The literal value from the API response object (`end_turn`, `max_tokens`, etc.) — log directly, don't derive or interpret it. This is the only reliable way to distinguish a response that was genuinely cut off (`max_tokens`) from one that just happened to be long but finished naturally (`end_turn`) — token count alone can't tell those apart, since a response that used all of `max_tokens` and one that used most of it and then finished are indistinguishable by output length. |
| `summary` | One-line abstract of what the turn covered, e.g. "Assessed 3.2 EDA#2 insight vs DAX formula" |
| `issue_flag` | Yes/no — was there a problem with this turn |
| `issue_type` | Short category, only populated when `issue_flag` is yes — see below |

### Detecting `issue_flag` / `issue_type` cheaply

No need to add a special structured tag to the model's output for this — `system_instructions.md` already has the bot use consistent, recognisable language for exactly the situations worth flagging (the "Requesting missing input" rule, the stop-and-ask behaviour in both verification modules, the "route to human marker" phrasing for out-of-scope requests, the "Reading this as..." misread-correction pattern). The app can apply simple pattern matching — most rows below against the response text, one against the marker's own input compared to Haiku's classification — rather than asking the model to self-report a status:

| Pattern in response | `issue_type` |
|---|---|
| Asks for a missing formula/code/config/context | `unresolved_dependency` or `missing_context` |
| "route to human marker" / declines to assess | `out_of_scope_request` |
| Flags a relationship for marker verification | `relationship_ambiguity` |
| Says a dependency chain couldn't be fully resolved | `unresolved_dependency` |
| Notes that submitted content contained embedded text attempting to direct the assessment (per Marking Principle 6) | `possible_prompt_injection` |
| States a rubric-grounded assessment that differs from what the marker explicitly asked for (per Marking Principle 7) | `marker_override_declined` |
| Flags a discrepancy between an uploaded chart screenshot and the marker's typed description (per 3.1 guidance) | `screenshot_description_mismatch` |
| The formula's Accuracy verdict and the screenshot's visual cross-check disagree with each other (per 3.2 guidance, DAX module step 8) | `insight_visual_mismatch` |
| 3.1's Implementation verdict and 3.2's Accuracy verdict, from the same DAX formula, point in genuinely different directions (per Marking Principle 4 and the 3.1/3.2 guidance — expected on occasion, not a bug, but worth reviewing) | `implementation_accuracy_divergence` |
| A notebook's embedded saved output disagrees with what the Written Report itself claims (per Python module step 8) | `notebook_output_report_mismatch` |
| Message content pattern-matches a different component type than what Haiku classified it as (e.g. contains `CALCULATE(`/`RELATED(` but classified as something other than `dax_formula`; contains `import pandas`/`` ```python `` but classified as something other than `python_code`) | `possible_component_mismatch` |
| None of the above | `issue_flag = no` |

This costs nothing extra in tokens and needs no change to how the bot writes its responses — it already produces this language naturally per the existing spec. If this heuristic turns out to be unreliable in practice, the fallback is having the model append one short structured line at the end of its turn for the app to parse — worth revisiting only if the lightweight approach misses too much.

## New-submission reset

Wiring the button to a genuinely new conversation (empty `history`, fresh cache lifecycle) rather than an in-band reset message is what delivers the actual savings at 140-group scale — the instructions and reference-bundle cache breakpoints stay warm across submissions (same content, same cache), while the growing per-group transcript is what gets discarded and restarted cleanly. This also clears the sidebar scorecard's session-state dict — a new submission starts that tracker empty, same as the conversation itself.
