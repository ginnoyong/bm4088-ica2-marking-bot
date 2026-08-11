# Implementation Guide — BM4088 ICA2 Marking Bot

Builds the bot designed across the rest of this project: Claude API (Sonnet/Opus routing, prompt caching), Streamlit front end hosted via GitHub on Streamlit Community Cloud, staff login gate, Google Sheets logging. Built using Claude Code's `/goal` feature to do the actual engineering, with you supplying accounts, credentials, and verification.

## 0. What you need before starting

| Item | Where to get it | Used for |
|---|---|---|
| Anthropic API key | console.anthropic.com → API Keys | Calling Claude |
| GitHub account | github.com | Hosting the repo Streamlit deploys from |
| Streamlit Community Cloud account | share.streamlit.io, sign in with GitHub | Hosting the app |
| Google Cloud project | console.cloud.google.com | Sheets API service account only — no OAuth client needed |
| A Google Sheet, created and empty | sheets.google.com | The log destination |
| Claude Code installed locally | see docs.claude.com for current install instructions | Building the app |

**On the login gate.** Staff ID matched against a roster — no access code, no OIDC, no external identity provider. Just a username check.

## 1. Repository structure

Create a new GitHub repo, then this structure locally:

```
bm4088-ica2-marking-bot/
├── app.py
├── requirements.txt
├── CLAUDE.md
├── .gitignore
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml          # local only — never commit this
├── src/
│   ├── model_routing.py
│   ├── api_client.py
│   ├── sheets_logger.py
│   ├── auth.py
│   ├── help_content.py
│   ├── notebook_parser.py
│   └── scorecard_tracker.py
├── prompts/
│   └── system_instructions.md
└── reference/
    ├── rubric_descriptors.md
    ├── scenario_descriptions.md
    ├── table_relationships.md
    ├── data_dictionary.md
    ├── tutor_guide_data_issues.md
    ├── tutor_guide_scenario_analytics_ref.md
    └── marking_notes.md
```

Copy the files already built in this project into `prompts/` and `reference/`, and `CLAUDE.md` into the repo root — those are the deliverables from earlier in this conversation, not something Claude Code needs to (re)write. `reference/marking_notes.md` is included in the download too, so nothing needs to be manually copied in from the project files separately. There's no roster file in the repo at all — the roster lives in a Google Sheet, set up in Section 2 below.

`.gitignore` should contain at minimum:
```
.streamlit/secrets.toml
__pycache__/
*.pyc
.venv/
```

## 2. Google Cloud: Sheets API + Drive API + service account

1. In console.cloud.google.com, create a new project (or use an existing one).
2. APIs & Services → Library → enable **Google Sheets API**.
3. APIs & Services → Library → also enable **Google Drive API**. This is easy to miss — if you're using `gspread` (the standard Python library for this, and the likely default Claude Code reaches for), it needs both APIs enabled even though you're only writing to a spreadsheet, not touching Drive files directly. Skipping this produces a "Google Drive API has not been enabled" error the first time the app tries to open the sheet, even with correct Sheets-only credentials otherwise.
4. APIs & Services → Credentials → Create Credentials → **Service Account**. Give it a name (e.g. `ica2-bot-logger`), no special roles needed at the project level.
5. Open the new service account → Keys → Add Key → **Create new key** → JSON. Download it — this is the credential the app uses to write to Sheets. Keep it out of the repo entirely.
6. Open your Google Sheet (the logging one). In the sheet header row, add exactly these columns (matching the schema from earlier in this project):
   `timestamp | staff_id | session_id | scenario_number | component_type | model_used | input_tokens | output_tokens | cache_read_tokens | cache_write_tokens | stop_reason | summary | issue_flag | issue_type`
7. Share the logging Sheet with the service account's email address (found in the JSON key file, field `client_email`) — give it **Editor** access, the same way you'd share with a person.
8. Create a **second, separate Google Sheet** for the staff roster, named exactly `roster`. In row 1, add a single header: `staff_id`. Add your actual authorized staff IDs in the rows below, one per row.
9. Share this roster Sheet with the same service account email — **Viewer** access is enough, since the app only ever reads it.

## 3. Login gate: staff ID checked live against the roster Sheet

No access code, no password — just a staff ID checked against the roster Sheet from Section 2. Simplest option, appropriate for an internal tool with a non-public URL; the trade-off is that anyone who knows or guesses a valid staff ID string can get in, since there's no secret involved.

1. The roster lives entirely in the Google Sheet set up in Section 2 — nothing in the repo itself. `src/auth.py` queries it live via the Sheets API on every login attempt, using the same service account credentials already set up for logging. There's no local file to keep in sync, and no risk of ever committing real staff IDs to git history, since they're never in the repo at all.
2. The app's login screen asks for a staff ID; it must appear in the "roster" Sheet's `staff_id` column, checked fresh on each attempt (not cached), before the chat loads. Adding or removing a staff member in the Sheet takes effect immediately — no redeploy needed.
3. Because this is now a live network call rather than a local file read, handle failure explicitly: a Sheets API timeout, rate limit, or misconfigured sharing permission should surface as a clear, retryable error ("couldn't verify access, try again") — never a raw exception, and never something that looks identical to a genuine "not on the roster" denial.

The actual check happens in `src/auth.py`, before the chat interface renders — never inside the conversation itself, per the design decided earlier.

## 4. Anthropic API key

console.anthropic.com → API Keys → Create Key. This goes into secrets, never into code or the repo.

## 5. Build the app with Claude Code

Install Claude Code per current instructions at docs.claude.com (this changes over time, so check there rather than relying on a fixed command here). Then, in your repo directory:

```
cd bm4088-ica2-marking-bot
claude
```

**First, give Claude Code project context.** `CLAUDE.md` is included in the project bundle at the repo root — place it there as-is, no editing needed. It covers what already exists in the repo, what Claude Code is building, and the architecture decisions from `docs/implementation_notes.md` condensed into a form Claude Code should treat as fixed unless you say otherwise.

Then run the build in stages — one `/goal` per stage, verifying each before moving to the next. Long, vague goals are exactly what tends to produce plausible-looking but wrong output; keep each one narrow and objectively checkable.

**Stage 1 — scaffold and login gate**
```
/goal Create app.py, requirements.txt, .streamlit/config.toml, and
src/auth.py. The app must show a login screen first — a single staff
ID field, checked live via the Sheets API against a Google Sheet named
"roster" (column header staff_id, one ID per row, credentials and
sheet ID from st.secrets), not cached, a fresh check on every login
attempt — and only render a placeholder chat area after a successful
match. Handle Sheets API failures (timeout, rate limit, permission
error) with a clear retryable error message, distinct from a genuine
"not on the roster" denial — never a raw exception. Running
`python -m streamlit run app.py` locally must show the login screen, reject an
unlisted staff ID with a clear message, and show the placeholder chat
area after a listed one. Do not build the Claude API integration yet.
```

**Stage 2 — Claude API client, routing, caching**
```
/goal Create src/model_routing.py and src/api_client.py. Load
prompts/system_instructions.md and every .md file under reference/ at
startup, concatenate the reference files into
one bundle. Implement
classify_component_type(marker_input) using one cheap
claude-haiku-4-5-20251001 call (max_tokens=20, temperature=0) that
returns exactly one of: problem_statement, hypotheses,
schema_description, cleansing, dax_formula, eda_chart_config,
python_code, predictive_analytics_text, report_structure, conclusion,
other. Implement select_model(component_type) returning
claude-opus-4-8 for "dax_formula" and "python_code",
claude-sonnet-5 otherwise. Implement a function that classifies the
marker's message first, then builds a Messages API request with
max_tokens=8192 (this bot's required output format — dependencies,
relationship assumptions, verdict, mandatory justification, scorecard
updates — genuinely needs headroom; a lower ceiling risks truncating
mid-response on richer turns), temperature=0, and three cache_control
breakpoints: end of
system_instructions.md, end of the reference bundle, and end of the
conversation so far (set on the last content block of the last prior
message, not on the message object). Write a small script or test
that sends one real message through the full flow (classify → route →
call) and prints the classification, the model used, the response, and
usage including cache_read_input_tokens and cache_creation_input_tokens,
confirming the second identical call within 5 minutes shows a cache
read. Test with an obvious DAX formula input and confirm it classifies
as dax_formula and routes to Opus.
```

**Stage 3 — chat UI**
```
/goal Wire the placeholder chat area from Stage 1 into a real
conversation using the api_client from Stage 2. At the start of a new
session (after login, before the first message), require a scenario
number selection (1-6) — once set, lock it for the rest of the session
and display it read-only, since it doesn't change mid-submission. No
component type selector — that's now handled automatically by
classify_component_type() from Stage 2 on every message, not chosen by
the marker. Add a "Start New Submission" button that clears all
conversation state, including the locked scenario number, and returns
to the scenario selector. Running the app locally: log in → select a
scenario (now locked) → send a DAX-formula message and confirm the
model actually used (visible in logs or a debug indicator) is Opus →
send a plain problem-statement message in the same session and confirm
it routes to Sonnet, scenario number unchanged → click "Start New
Submission" → scenario selector reappears and must be set again.
```

**Stage 4 — Google Sheets logging**
```
/goal Create src/sheets_logger.py using gspread with a service account
(credentials from st.secrets), authorized with both the
https://www.googleapis.com/auth/spreadsheets and
https://www.googleapis.com/auth/drive scopes (both are required even
though the app only writes to a spreadsheet, not Drive directly — see
docs/IMPLEMENTATION_GUIDE.md Section 2). Open the sheet by ID
(GOOGLE_SHEET_ID from secrets), not by name, and append one row per
turn to the configured Google Sheet, matching exactly this column
order:
timestamp, staff_id, session_id, scenario_number, component_type,
model_used, input_tokens, output_tokens, cache_read_tokens,
cache_write_tokens, stop_reason, summary, issue_flag, issue_type.
stop_reason is the literal value from the API response object
(e.g. "end_turn", "max_tokens") — log it directly, don't derive or
interpret it; a value of "max_tokens" means the response was
genuinely cut off, distinct from a response that happened to be long
but finished naturally. component_type
comes from Stage 2's classify_component_type() output, not a marker
selection. Derive summary as a short truncation or simple description
of the turn. Derive issue_flag/issue_type via plain pattern matching
against the response text and, for one case, the marker's input:
missing-context or dependency requests -> unresolved_dependency or
missing_context; a route-to-human-marker decline -> out_of_scope_request;
a flagged relationship needing marker verification -> relationship_ambiguity;
the response noting embedded text in the submission tried to direct the
assessment -> possible_prompt_injection; the response stating an
assessment that differs from what the marker explicitly asked for ->
marker_override_declined; a response flagging a discrepancy between an
uploaded chart screenshot and the marker's typed description ->
screenshot_description_mismatch; a response noting the formula's
accuracy verdict and a screenshot's visual cross-check disagree with
each other -> insight_visual_mismatch; a response noting 3.1's
implementation verdict and 3.2's accuracy verdict (from the same DAX
formula) point in different directions -> implementation_accuracy_divergence;
a response noting a notebook's embedded
saved output disagrees with what the Written Report claims ->
notebook_output_report_mismatch; a regex check (DAX/Python syntax
patterns) on the marker's input disagreeing with what Haiku classified
it as -> possible_component_mismatch, log only, never block or alter
routing. Wire this logger into the Stage 3 chat flow so every turn
appends a row. Running the app and sending two messages must result in
two new rows appearing in the actual Google Sheet.
```

**Stage 5 — polish**
```
/goal Add error handling for: Claude API failures (show a retry
option, don't crash), Google Sheets write failures (log to console,
don't block the chat response from displaying), and missing/invalid
secrets on startup (clear error message naming which secret is
missing, not a raw traceback). Add a requirements.txt covering every
import actually used in the repo. Confirm `python -m streamlit run app.py` still
works end to end after these changes.
```

**Stage 6 — help popup**
```
/goal Create src/help_content.py with a single HELP_TEXT constant
(markdown string) containing this content, written as scannable
bullets for a popup, not conversational prose:

Title: How to use this bot

What this bot can help you mark:
- Problem statement and hypotheses (1.1, 1.2)
- Schema and table relationships (2.1)
- The two cleansing activities (2.2)
- DAX formulas behind EDA charts and insights (3.1, 3.2)
- Chart formatting — colour, hierarchy, preattentive attributes (3.3, needs a screenshot)
- Predictive analytics: variables, target, evaluation (4.1-4.3)
- Required report structure - which elements are present or missing (5.1)
- Narrative sequencing to the conclusion and recommendations (5.2)
- Dashboard design and data storytelling principles (5.3)

How to get the best results:
- If unsure where to start, go through the requirements in order
  (1 -> 5) - it naturally covers the problem statement before later
  checks need it. Not required, though - jump around freely, and skip
  ahead if something's missing for one part, come back later
- Share the group's problem statement early - several later checks
  depend on it
- Paste exact/verbatim text for anything being judged on wording
  (report excerpts, DAX formulas, code) - not your own summary of it
- For chart checks, describe the configuration: chart type, what's on
  axis, values, filters
- Some recommendations come back Provisional rather than final - that
  means what's been checked from the report is solid, but it hasn't
  yet been verified against the actual file. Supplying that (a
  formula, code, a screenshot) moves it to a confirmed grade

What this bot can't do:
- Roleplay Presentation and Team Feedback - not part of the Written
  Report
- Open the Power BI file, notebook, or presentation itself - it works
  from what you paste, describe, or upload, never by accessing files
  directly
- It gives a recommended band and mark with reasoning, never a final
  grade - that's always your call

Using this content, implement a @st.dialog modal (a single shared
dialog function, imported and called from both places below, not
duplicated) titled "How to use this bot" that renders HELP_TEXT and
includes an explicit "Close" button in addition to the dialog's
default dismiss behaviour (X, Esc, click-outside). Add a button
labelled "How to use this bot" that opens this dialog: once near the
login form on the login screen, and once always-visible (e.g. in the
sidebar) on the chat screen regardless of scroll position or
conversation state. Opening and closing the dialog must never trigger
an API call and must never clear or affect login form input, chat
history, the locked scenario number, or any other session state.
Running the app locally: the button is visible on the login screen
before logging in, clicking it shows the modal with the content above,
closing it (via the Close button, X, Esc, or clicking outside) returns
to the login screen with anything already typed still in the field;
after logging in and starting a conversation, the same button is
visible in the chat view and behaves the same way without disrupting
the conversation.
```

**Stage 7 — optional chart screenshot for 3.1**
```
/goal Add an optional image attachment to the chat input, for
supplying a screenshot of a Power BI chart alongside a 3.1 check.
Use st.chat_input's file-attachment support if available in the
installed Streamlit version, otherwise a small st.file_uploader shown
near the input, clearly labelled optional. When an image is attached,
include it as an image content block (base64-encoded) in the Messages
API request alongside the text message — Anthropic's Python SDK
supports this natively, encode as base64 with the correct media_type
for the uploaded file type (png/jpeg). The image is part of the new
message only, never part of the cached prefix — don't disturb the
existing cache_control placement from Stage 2 (the breakpoint stays on
the last prior message, not on this new one). If an image is attached,
prepend a short note like "[Image attached: chart screenshot]" to what
gets passed into Stage 2's classify_component_type() call, so
classification still routes correctly even if the accompanying text is
minimal. Running the app locally: attach a chart screenshot with
minimal accompanying text (e.g. just the hypothesis) and confirm the
response reads chart type and axis labels from the image rather than
asking for them, while still asking for aggregation/filters unless
those are visibly labelled in the image; attach a screenshot that
clearly shows a different chart type than what's stated in the
accompanying text and confirm the response flags the discrepancy
rather than silently picking one.
```

**Stage 8 — full .ipynb upload for Requirement 4**
```
/goal Add an optional .ipynb upload to the chat input, alongside the
Stage 7 image attachment (both optional, either or neither may be
present on a given turn). Create src/notebook_parser.py to parse the
uploaded notebook's JSON structure and extract: cell source text (code and markdown cells), and any saved
output already embedded in code cells (text/stream output, printed
values) — image outputs (plots) can be skipped for now. Concatenate
the extracted content into plain text and include it as the message
content sent to Claude, clearly delimited so cell boundaries and
embedded outputs are distinguishable from each other. If a .ipynb is
attached on a turn, skip Stage 2's classify_component_type() call
entirely and set component_type = "python_code" directly — the file
extension is a certain signal, per docs/implementation_notes.md. This
still routes to Opus per the existing model_routing rules, no changes
needed there. Running the app locally: upload a sample .ipynb
containing a mix of cleansing, EDA, and a predictive-analytics section
with a saved output, with minimal accompanying text, and confirm the
response only discusses the predictive-analytics cells (per
system_instructions.md's scoping rule), references the saved output
where relevant, and explicitly does not comment on the cleansing/EDA
cells beyond noting they were out of scope.
```

**Stage 9 — sidebar scorecard**
```
/goal Create src/scorecard_tracker.py implementing a session-state
dict tracking the running scorecard, keyed by the exact Criterion cell
text (e.g. "3.1 (EDA #1)", "4.2"). After every assistant response,
parse the response text for a markdown table with header
"| Criterion | Grade | Status | Comments |" (simple row-splitting on
"|", matching the header — don't build a general markdown parser, just
match this specific table shape). For each row found, extract
Criterion and Grade as-is, and Status reduced to just its leading
state word — split on the em dash separator (" — ") and keep only what
comes before it, so "Provisional — pending filter confirmation"
becomes "Provisional"; a plain "Complete" with no dash stays as-is.
Drop Comments entirely. Upsert into the session-state dict — a new
key adds an entry, an existing key overwrites its Grade/Status with
the latest values. If a response has no such table, leave the dict
unchanged. Render this using st.dataframe specifically, not st.table
or a raw markdown/HTML table — st.dataframe's built-in hover toolbar
(download as CSV, search, fullscreen expand) is a feature worth
keeping, and it's the reason to use this widget over the alternatives.
Use st.column_config to control column width and enable text wrapping
within cells (rather than switching away from st.dataframe to solve
wrapping) — this keeps the toolbar while still fitting content within
the sidebar's width. Show Criterion, Grade, and the bare Status word
in the sidebar, directly below the "How to use this bot" button from
Stage 6, sorted in rubric order (1.1, 1.2, 2.1, 2.2, then 3.1/3.2/3.3
per EDA entry in order, 4.1, 4.2, 4.3, 5.1, 5.2, 5.3) rather than
insertion order. Wire the "Start New Submission" button to also clear
this session-state dict, alongside everything else it already resets.
Running the app locally: confirm hovering over the sidebar table shows
the native st.dataframe toolbar (download/search/fullscreen); get a
response that includes a summary table for at least two different
lines (e.g. ask about 3.1 for one EDA entry, then 4.2) and confirm
both appear correctly in the sidebar, in rubric order, not just chat
order, with Status shown as a bare word (no reason clause) even when
the chat table's Status cell had one, and with long content wrapping
within the sidebar's width rather than overflowing or being cut off;
get a second response updating one of those same lines (e.g. 4.2
moving from On-hold to a real band) and confirm the sidebar row
updates in place rather than duplicating; click "Start New
Submission" and confirm the sidebar scorecard clears along with the
conversation.
```

After each stage, actually run the app and check the goal's stated condition yourself before starting the next one — `/goal`'s own completion check is useful but isn't a substitute for you confirming it does what you intended, especially for the parts (cache breakpoints, routing) that are easy to get subtly wrong in a way that still runs without erroring.

## 6. `secrets.toml` — local development

Create `.streamlit/secrets.toml` (this file is git-ignored, never pushed):

```toml
ANTHROPIC_API_KEY = "sk-ant-..."

[gcp_service_account]
type = "service_account"
project_id = "..."
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "ica2-bot-logger@your-project.iam.gserviceaccount.com"
client_id = "..."
token_uri = "https://oauth2.googleapis.com/token"

# fill in the rest of the fields from the downloaded JSON key —
# copy them across, don't retype

GOOGLE_SHEET_ID = "the-id-from-your-logging-sheet-url"
ROSTER_SHEET_ID = "the-id-from-your-roster-sheet-url"
```

## 7. Test locally

```
python -m streamlit run app.py
```

On Windows, use this form rather than calling `streamlit.exe` directly — some organization-managed devices block the separate `streamlit.exe` launcher under Device Guard / Windows Defender Application Control, since it's an unsigned executable generated by `pip install`. Routing through `python -m` runs it via the trusted Python interpreter instead and avoids the block.

Walk through: login screen appears → correct credentials get you into the chat → wrong credentials are rejected → the scenario selector is required before sending, no component type selector to fill in → a real Claude response appears, from the correct model for a DAX-formula vs. a problem-statement message → a row appears in the Google Sheet after each turn, `component_type` populated from Haiku's classification → "Start New Submission" clears everything and shows the scenario selector again.

## 8. Deploy

1. `git add . && git commit -m "Initial build" && git push` to GitHub (secrets.toml stays local, per `.gitignore` — verify it's not in the commit).
2. In share.streamlit.io, "New app" → point at your GitHub repo, branch, and `app.py`.
3. In the app's settings on Streamlit Cloud, **Secrets** — paste in the same content as your local `secrets.toml` (API key, service account, both sheet IDs). There's no roster file to worry about deploying with the repo — it's entirely in the Google Sheet, already live and shared with the service account from Section 2.
4. Deploy. Repeat the same walkthrough from Step 7 against the live URL.

## 9. Final checklist against the design

- [ ] Login blocks access before any API call is made — confirm by checking the Sheet has zero rows from a rejected login attempt
- [ ] DAX formula and Python code messages route to Opus; everything else to Sonnet — confirm via the `model_used` column
- [ ] The Haiku classification call itself uses `temperature=0` and completes before the main call, not in parallel with it (routing depends on its result)
- [ ] A second identical-ish message within 5 minutes shows nonzero `cache_read_tokens`
- [ ] Every API call is sent with `temperature=0`
- [ ] "Start New Submission" produces a genuinely new `session_id`, not a continuation
- [ ] The Sheet never contains full verbatim student text, bands, or scores — only the lightweight columns
- [ ] Editing any file under `reference/` and restarting the app changes the bot's behaviour without touching `prompts/system_instructions.md` or any app code
- [ ] Adding a staff ID to the roster Sheet and immediately trying to log in with it works without a redeploy or restart, confirming the check is genuinely live, not cached; removing one denies access on the next login attempt just as quickly
- [ ] Login fails gracefully with a retryable message if the roster Sheet is temporarily unreachable (e.g. test by briefly revoking the service account's share access to the roster Sheet) — never a raw exception, never indistinguishable from a genuine "not on the roster" denial
- [ ] The "How to use this bot" help dialog opens from both the login screen and the chat screen, closes cleanly, and never triggers an API call or clears session state
- [ ] An attached chart screenshot doesn't disturb the cache breakpoint on prior turns — check `cache_read_tokens` is still nonzero on the message right after one containing an image
- [ ] An uploaded `.ipynb` skips the Haiku classification call (check the log — no extra token cost for that call on notebook-upload turns) and the response only discusses Requirement-4-relevant cells, explicitly declining to comment on any cleansing/EDA cells present in the same file
- [ ] The sidebar scorecard updates correctly across at least two different lines, sorts in rubric order not chat order, updates a row in place rather than duplicating it when a line's grade changes, clears on "Start New Submission," shows Status as a bare word (Complete/Provisional/On-hold) even when the chat table's version had a reason clause attached, and shows the native `st.dataframe` hover toolbar (download/search/fullscreen) on mouseover
