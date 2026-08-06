# BM4088 ICA2 Marking Bot

A Streamlit app that helps markers assess specific rubric lines of the BM4088 ICA2 group
assignment, backed by the Claude API. Markers paste, describe, or upload the pieces of a
group's submission — problem statement, DAX formulas, Python/notebook code, chart
screenshots — and the bot returns a recommended band and mark with reasoning, grounded in
the course's marking rubric, for the marker to accept or override. It never assigns a final
grade.

Deployed on Streamlit Community Cloud, built from this repo, logging to Google Sheets.

## What it does

- **Staff login** — gated by staff ID against a roster kept in a Google Sheet. No password;
  a match against the roster is the only check.
- **One scenario per submission** — the marker picks the business scenario (1–6) once per
  session; it locks for the rest of that submission.
- **Automatic model routing** — every marker message is pre-classified by a cheap Haiku call
  into a component type (DAX formula, Python code, problem statement, hypotheses, etc.).
  DAX and Python checks route to Opus; everything else routes to Sonnet. There's no
  marker-facing model selector.
- **Attachments** — a Power BI chart screenshot (PNG/JPEG) for chart-effectiveness and
  formatting checks, or a full `.ipynb` notebook for predictive-analytics checks. At most
  one attachment per message; a `.ipynb` upload is parsed into plain text (cell source +
  saved text output) and skips the classification call entirely, since the file extension
  is already a certain signal for `python_code`.
- **Running scorecard** — a compact, always-visible sidebar table (Criterion / Grade /
  Status) parsed automatically from each response's summary table, so a marker can see
  cumulative progress across a session without asking for it.
- **Prompt caching** — the system instructions, the reference-material bundle, and the
  growing conversation are each their own cache breakpoint, so a long marking session isn't
  repeatedly billed for its own history.
- **Google Sheets logging** — one row per turn (timestamp, staff ID, session ID, scenario,
  component type, model used, token/cache usage, a short summary, and a pattern-matched
  issue flag/type), for health monitoring — not a transcript of student work.
- **Start New Submission** — clears session state and starts a genuinely new conversation,
  which is what actually resets the prompt-cache lifecycle, not just an in-chat reset.

## Project structure

```
app.py                     — Streamlit entry point: login, scenario lock, chat, sidebar
src/
  api_client.py             — Claude Messages API calls, request building, prompt caching
  auth.py                   — staff ID check against the roster Google Sheet
  help_content.py           — the "How to use this bot" copy
  model_routing.py          — Haiku classification + Opus/Sonnet routing
  notebook_parser.py        — .ipynb → plain text for a marker's notebook upload
  scorecard_tracker.py      — parses each response's table into the sidebar scorecard
  sheets_logger.py          — Google Sheets client + per-turn logging
prompts/system_instructions.md   — the full behavioural spec sent to the model
reference/*.md              — marking reference data (rubric, scenarios, schema, etc.)
docs/implementation_notes.md      — architecture rationale
docs/IMPLEMENTATION_GUIDE.md      — the staged build plan this repo was built from
scripts/                    — one-off setup/test scripts, not part of the running app
```

## Setup

Requires Python 3.11+ and a Google Cloud service account with the Sheets and Drive APIs
enabled.

```bash
pip install -r requirements.txt
```

Create `.streamlit/secrets.toml` (never commit this file):

```toml
ANTHROPIC_API_KEY  = "..."
GOOGLE_SHEET_ID     = "..."   # per-turn logging sheet
GOOGLE_SHEET_NAME   = "..."   # worksheet/tab name within it
ROSTER_SHEET_ID     = "..."   # staff roster sheet
ROSTER_SHEET_NAME   = "..."   # worksheet/tab name within it

[gcp_service_account]
type = "service_account"
project_id = "..."
private_key_id = "..."
private_key = "..."
client_email = "..."
client_id = "..."
token_uri = "https://oauth2.googleapis.com/token"
# auth_uri, auth_provider_x509_cert_url, client_x509_cert_url, universe_domain
# are also expected — copy the full JSON key your service account download gives you.
```

Both the logging sheet and the roster sheet must be shared (Viewer is enough for the
roster; the logging sheet needs Editor) with the service account's `client_email`. The
roster sheet needs a `staff_id` column, one authorized ID per row.

Run locally:

```bash
streamlit run app.py
```

## Deployment

Deployed on [Streamlit Community Cloud](https://streamlit.io/cloud) directly from this
repo's `master` branch. Add the same keys as above to the app's **Secrets** panel there —
`app.py` validates all of them at startup and fails fast with a clear message listing
anything missing, rather than surfacing a raw exception later.

## Architecture notes

See `CLAUDE.md` for the locked-in architecture decisions (model routing, prompt caching
breakpoints, login flow, logging schema) and `docs/implementation_notes.md` for the
reasoning behind them.
