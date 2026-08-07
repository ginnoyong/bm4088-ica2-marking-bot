# Project: BM4088 ICA2 Marking Bot

A Streamlit app that helps markers assess specific rubric lines of the ICA2
group assignment, via the Claude API. Deployed on Streamlit Community Cloud,
built from a GitHub repo, logging to Google Sheets.

## What already exists — do not rewrite or duplicate

```
prompts/system_instructions.md   — full behavioural spec for the model
reference/*.md                   — marking reference data the model reads
docs/implementation_notes.md     — architecture rationale for everything
                                    below; read this for the "why" behind
                                    any decision that seems arbitrary
docs/IMPLEMENTATION_GUIDE.md     — the staged /goal build plan this repo
                                    is being built from
```

All of the above are finished deliverables from a separate design process — the app's job is to load and send them, never to rewrite, paraphrase, or regenerate their content.

## What you're building

Everything under `app.py`, `src/`, `.streamlit/`, and `requirements.txt` — per the staged `/goal` commands in `docs/IMPLEMENTATION_GUIDE.md`. Build in that order; each stage has an explicit, checkable completion condition.

## Architecture decisions already made — do not deviate without asking

- **Model routing**: DAX and Python code checks go to `claude-opus-4-8`, everything else goes to `claude-sonnet-5`. Routed per API call, automatically, via a cheap `claude-haiku-4-5-20251001` pre-classification call on each marker message — no marker-facing selector. `component_type` in the log comes from this classification, not user input.
- **Temperature**: all API calls, including the Haiku classification, use `temperature=0` — deterministic marking matters more than response variety here.
- **Prompt caching**: `system_instructions.md` and the concatenated `reference/` `.md` bundle are each their own `cache_control` breakpoint; the growing conversation is a third breakpoint, set on the last content block of the last prior message — never on the message object itself, that's not valid per the API.
- **Screenshots**: 3.1 optionally accepts an attached chart screenshot as an image content block on the current message only — never part of the cached prefix, doesn't change the cache breakpoint placement above. Supporting evidence for chart type/axis labels, never a replacement for the marker's typed configuration (aggregation, filters still need to be stated).
- **Notebook uploads**: a full `.ipynb` is only ever expected for Requirement 4 (4.1–4.3), never EDA or cleansing. When one's attached, skip the Haiku classification call and set `component_type = "python_code"` directly — the file extension is a certain signal. `system_instructions.md` restricts the model's analysis to Requirement-4-relevant cells even if cleansing/EDA cells are present in the same file; the app's job is just to extract and pass through the full content, not to pre-filter cells itself.
- **Reference bundle**: only `.md` files from `reference/` are concatenated into what's sent to Claude. There's no roster file in `reference/` to worry about excluding — the roster lives entirely in a separate Google Sheet (see Login gate below), structurally outside anything the reference-bundle loader ever touches.
- **Login gate**: staff ID checked live against a Google Sheet named "roster" (single `staff_id` column), on every login attempt — not a local file, not cached. No access code, no password, no OIDC or external identity provider. Happens entirely before the chat renders, never inside the conversation; the model has no role in authentication. This is a live external API call, so it needs its own error handling — see Access control in docs/implementation_notes.md for the failure-mode this introduces that a local-file check never had.
- **Sidebar scorecard**: a compact three-column (Criterion, Grade, Status) session-state tracker, parsed from the four-column summary table `system_instructions.md` requires in every substantive response — the app parses, the model just produces the table it was already going to produce. Keyed by exact Criterion cell text, which is why EDA entries must be disambiguated ("3.1 (EDA #1)," not bare "3.1") — otherwise four EDA entries' rows would collide on the same key.
- **Submission lifecycle**: a "Start New Submission" button clears conversation state entirely (new session, fresh cache lifecycle) — not just an in-conversation reset message. Scenario number (1–6) is selected once per session via a UI selector, then locked read-only for the rest of that session.
- **Logging**: one row per turn to Google Sheets via a service account, columns are `timestamp, staff_id, session_id, scenario_number, component_type, model_used, input_tokens, output_tokens, cache_read_tokens, cache_write_tokens, summary, issue_flag, issue_type`. `issue_flag`/`issue_type` are derived by simple pattern-matching against the response text — including `possible_prompt_injection` and `marker_override_declined`, per `system_instructions.md`'s Marking Principles 6 and 7 — plus one check comparing the marker's input against Haiku's classification (`possible_component_mismatch`). Never derived by asking the model to self-report a status; see `docs/implementation_notes.md` for the full detection table.

If a `/goal` seems to conflict with something above, the decision above wins — flag the conflict rather than silently picking one.
