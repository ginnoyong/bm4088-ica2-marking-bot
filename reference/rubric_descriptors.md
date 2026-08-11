# Rubric Descriptors — BM4088 ICA2 Marking Sheet

Source: `2026S1_BM4088ICA2_Markers_Sheet___CASEX__MARKERNAME.xlsx`, sheet "Data Analysis & Written Report". Verbatim text, one line item per row, in the marking sheet's own order. `#` is the subcomponent index used throughout the system instructions (e.g. 4.2). Total possible marks: 60.

Update this file whenever the marking sheet changes — it's the single source of truth for weights and band text. The system instructions reference these by index number rather than repeating the text, so a rubric change only needs to be made here.

## 1. Business & Data Understanding (10 marks)

### 1.1 — Problem statement (weight 6)
Components expected: business problem/challenge; objectives and business impact; success metrics; scope and constraints.

| Band | Range | Descriptor |
|---|---|---|
| A | 80–100% | The problem statement clearly and completely addresses all components, demonstrating a strong and accurate understanding of the business scenario. |
| B | 70–79% | The problem statement adequately addresses the business scenario, demonstrating a good understanding, though some components may lack clarity or depth. |
| C | 60–69% | The problem statement demonstrates a basic understanding of the business scenario, with 1 to 2 components unclear or incomplete. |
| D | 50–59% | The problem statement demonstrates a weak understanding of the business scenario, with 3 to 4 components unclear or incomplete. |
| F | 0–49% | The problem statement demonstrates little or no understanding of the business scenario. |

### 1.2 — Hypotheses alignment (weight 4)

| Band | Range | Descriptor |
|---|---|---|
| A | 80–100% | All FOUR (4) hypotheses are well-aligned to the problem statement and testable with the available data. |
| B | 70–79% | Most hypotheses are aligned to the problem statement and testable. |
| C | 60–69% | Some hypotheses are aligned, but 1 to 2 may be loosely connected or difficult to test. |
| D | 50–59% | Hypotheses are present but show limited alignment or are mostly not testable. |
| F | 0–49% | Hypotheses are absent, irrelevant, or entirely misaligned. |

## 2. Data Modelling and Cleansing (5 marks)

### 2.1 — Schema & table relationships (weight 3) — IN SCOPE

| Band | Range | Descriptor |
|---|---|---|
| A | 80–100% | The schema and table relationships are correctly implemented and completely described (e.g. keys, cardinality, filter direction). |
| B | 70–79% | The schema and table relationships are correctly implemented and adequately described, with most connection details covered. |
| C | 60–69% | The schema and table relationships are implemented with minor errors and partially described. |
| D | 50–59% | The schema and table relationships are implemented with minor errors but the description is absent or too weak to be credited. |
| F | 0–49% | The schema is incorrectly implemented or missing. |

### 2.2 — Cleansing justification, 2 activities (weight 2) — IN SCOPE

| Band | Range | Descriptor |
|---|---|---|
| A | 80–100% | TWO (2) data cleansing activities are correctly implemented, well-identified, appropriate, and clearly explained. |
| B | 70–79% | TWO (2) data cleansing activities are implemented as described and appropriate, with a reasonable explanation, though some may lack depth. |
| C | 60–69% | Data cleansing activities are performed with minor errors or minor discrepancies from the written description, with explanations that are present but limited. |
| D | 50–59% | Data cleansing is superficial or contains significant discrepancies from the written description — only trivial or generic activities are identified, with little or no explanation. |
| F | 0–49% | Data cleansing activities are largely absent, inappropriate, or not implemented as described. |

## 3. Exploratory Data Analysis (5 marks × 4 EDA entries = 20 marks)

Repeats identically for EDA #1, #2, #3, #4 — one hypothesis each. Data communication techniques referenced in the rubric: chart selection principles, colour theory, visual hierarchy, preattentive attributes.

### 3.1 — Visualization effectiveness + calculated measure/column (weight 2 per entry) — IN SCOPE, conditional on chart config supplied (and DAX where a calculated field is involved)

| Band | Range | Descriptor |
|---|---|---|
| A | 80–100% | The visualization is effective — chart type, fields, and aggregation combine to test the hypothesis clearly and convincingly. Where applicable, the calculated measure or column is correctly implemented and clearly described. |
| B | 70–79% | The visualization uses acceptable chart type, fields, and aggregation to test the hypothesis, though some choices may not be optimal. Where applicable, the calculated measure or column is correctly implemented and adequately described. |
| C | 60–69% | The visualization partially tests the hypothesis, with minor issues in chart type, fields, or aggregation. Where applicable, the calculated measure or column is present but may contain minor errors or is limited in description. |
| D | 50–59% | The visualization is unable to test the hypothesis, with significant errors or misalignments in chart type, fields, or aggregation. Where applicable, the calculated measure or column contains significant errors or is absent when required. |
| F | 0–49% | The visualization, insight, and formatting are largely absent or entirely incorrect. |

### 3.2 — Insight accuracy (weight 2 per entry) — IN SCOPE, conditional on DAX supplied

| Band | Range | Descriptor |
|---|---|---|
| A | 80–100% | The insight is specific, accurate, and meaningfully connected to the business scenario. |
| B | 70–79% | The insight is accurate and connected to the business scenario, though it may lack depth. |
| C | 60–69% | The insight is present but generic, with a weak connection to the business scenario. |
| D | 50–59% | The insight does not relate to the business scenario or is too vague to be credited. |
| F | 0–49% | Marks within this band reflect the degree to which any meaningful attempt is present. |

### 3.3 — Formatting (weight 1 per entry) — IN SCOPE, screenshot mandatory

| Band | Range | Descriptor |
|---|---|---|
| A | 80–100% | Formatting effectively enhances communication through deliberate application of data communication techniques. |
| B | 70–79% | Formatting is present and appropriate, though not all techniques are optimally applied. |
| C | 60–69% | Formatting is applied but inconsistent or minimally effective. |
| D | 50–59% | Formatting does not enhance communication. |
| F | 0–49% | (no descriptor given) |

## 4. Predictive Analytics (15 marks)

### 4.1 — Training data construction & variable/cluster justification (weight 6) — IN SCOPE

| Band | Range | Descriptor |
|---|---|---|
| A | 80–100% | Training data construction (selection, aggregation, and any preparation steps) is well-justified, clearly appropriate, and correctly implemented in the code. Variable/cluster selection is well-justified and clearly appropriate to the business problem. |
| B | 70–79% | Training data construction is appropriate and implemented as described; justification is adequate but may lack depth. Variable/cluster selection is appropriate, similarly adequate. |
| C | 60–69% | Training data construction is mostly appropriate, with minor discrepancies between the code and the written description; justification is limited. Variable/cluster selection is mostly appropriate with limited justification. |
| D | 50–59% | Training data construction is weak, or contains significant discrepancies between the code and the written description, or justification is weak. Variable/cluster selection is weak or questionable. |
| F | 0–49% | Training data construction and/or variable/cluster selection is absent, too weak to be credited, or not implemented as described. |

### 4.2 — Target variable / clustering objective: purpose & relevance (weight 3) — IN SCOPE

| Band | Range | Descriptor |
|---|---|---|
| A | 80–100% | Purpose and relevance are clearly and convincingly explained, directly tied to the business challenge. |
| B | 70–79% | Purpose and relevance are adequately explained. |
| C | 60–69% | Purpose and relevance are explained but weakly connected to the business challenge. |
| D | 50–59% | Purpose and relevance are unclear or poorly connected. |
| F | 0–49% | Purpose and relevance are absent or too weak to be credited. |

### 4.3 — Model evaluation & business implications (weight 6) — IN SCOPE

| Band | Range | Descriptor |
|---|---|---|
| A | 80–100% | Appropriate metrics are used and correctly computed as reported; results are accurately interpreted with specific and meaningful implications for business decision-making. |
| B | 70–79% | Appropriate metrics are used and computed as reported; results are interpreted with reasonable business implications, though the discussion may lack specificity or depth. |
| C | 60–69% | Metrics are mostly appropriate, with minor discrepancies between the code and the reported figures; business interpretation is superficial or weakly connected to the scenario. |
| D | 50–59% | Metrics are weak, questionable, or contain significant discrepancies between the code and the reported figures; there is little meaningful business discussion. |
| F | 0–49% | Metrics and/or business discussion are absent, too weak to be credited, or the reported figures do not match the code. |

## 5. Data Storytelling (10 marks)

Dashboard best practices referenced: clean and compact layout; right chart type for the right message; suitable use of colour, hierarchy, and preattentive attributes.

### 5.1 — Required structure met (weight 2) — IN SCOPE

| Band | Range | Descriptor |
|---|---|---|
| A | 80–100% | The required structure is fully met. |
| B | 70–79% | The required structure is met. |
| C | 60–69% | The required structure is mostly met, though one structural element may be missing or incomplete, or not all EDA visualizations are included. |
| D | 50–59% | The required structure is partially met, with two or more structural elements missing or incomplete, or several EDA visualizations missing. |
| F | 0–49% | The required structure is largely not met or the report is largely absent. Narrative sequencing and data storytelling principles are largely absent or entirely ineffective. |

**Required structure checklist**, per the assignment guide's Requirement 5 — this is the fixed reference to check the marker's description against, the same way `table_relationships.md` grounds 2.1:

- First Page present — introduces the business context and objectives, framing why the analysis matters to the decision-maker. This is a presence check only — whether the framing's content actually matches the Written Report's problem statement is 1.1's job, not this line's; see the 1.1 guidance in `system_instructions.md`.
- All FOUR (4) EDA visualizations from Requirement 3 present somewhere in the Middle Pages
- Outcomes of predictive analytics presented (screenshots of Python output where appropriate)
- Conclusion and Recommendations page present, with exactly TWO (2) actionable recommendations. This is a presence and count check only — whether the content actually matches the Written Report's Conclusion and Recommendations section is 5.2's job, not this line's; see the 5.2 guidance in `system_instructions.md`.
- No more than FIVE (5) visible pages total
- Page navigation applied, guiding the decision-maker through the narrative in sequence — **and actually tested by clicking through it**, not just visually present. A navigation button or bookmark can look correct while still being broken (pointing to the wrong page, not responding at all) — that's only detectable by actually using it, not by looking at it, so a marker's confirmation needs to be about having clicked through, not just having seen a navigation element on the page.
- Any unused pages set to hidden

This checklist is about presence/absence and count only — not about how well insights are sequenced (that's 5.2's job) or how well the schema is described (not relevant here). C and D bands are literally counts against this list: one missing/incomplete item is C, two or more is D.

### 5.2 — Narrative sequencing to conclusion & recommendations (weight 4) — IN SCOPE

| Band | Range | Descriptor |
|---|---|---|
| A | 80–100% | Insights are purposefully sequenced to build a coherent narrative toward the conclusion and recommendations. The conclusion is clear, and the two recommendations are specific and genuinely actionable. |
| B | 70–79% | Insights are mostly sequenced toward the conclusion and recommendations, though narrative flow may lack coherence in some areas. The conclusion and recommendations are clear, though the recommendations may lack some specificity. |
| C | 60–69% | Insights are present but loosely sequenced, with limited narrative flow. The conclusion and/or recommendations are present but generic, vague, or only partially actionable. |
| D | 50–59% | Insights are listed without meaningful sequencing. The conclusion and/or recommendations are unclear or not genuinely actionable. |
| F | 0–49% | Marks within this band reflect the degree to which any meaningful attempt is present. |

### 5.3 — Design principles applied (weight 4) — IN SCOPE

| Band | Range | Descriptor |
|---|---|---|
| A | 80–100% | Data storytelling and dashboard design principles are effectively and deliberately applied. |
| B | 70–79% | Data storytelling and dashboard design principles are adequately applied. |
| C | 60–69% | Data storytelling and dashboard design principles are partially applied. |
| D | 50–59% | Data storytelling and dashboard design principles are minimally applied. |
| F | 0–49% | (no descriptor given) |

Two distinct halves, per the descriptor's own wording — both grounded in `data_viz_principles.md`:
- **Dashboard design principles** (visual/layout): clean/compact layout, right chart type per page, consistent colour theme across pages, simplicity (decoration is fine if it serves understanding, not automatically a violation). Checked via a marker-supplied checklist description, screenshot optional. Do not re-check accuracy here — already covered under 3.3's Tufte grounding, would be redundant.
- **Data storytelling principles** (content/framing): whether insights and the conclusion use Context and Benchmarking (a reference point — vs Target, vs Last period, vs Same period last year, vs Benchmark/Competitor) rather than presenting raw isolated numbers, and whether they pass the "So What?" test (so what / now what / for whom) rather than remaining observations. This reuses text already supplied for 3.2 and 5.2 — no new input needed for this half.

## Scope summary (for quick lookup)

**In scope (60 of 60 marks):** 1.1 (6), 1.2 (4), 2.1 (3), 2.2 (2), 3.1×4 (8), 3.2×4 (8), 3.3×4 (4), 4.1 (6), 4.2 (3), 4.3 (6), 5.1 (2), 5.2 (4), 5.3 (4)

**Out of scope, route to human marker (0 of 60 marks from the Criteria table):** none remaining. Roleplay Presentation and Team Feedback stay out of scope, since they were never part of the Written Report to begin with — see the Scope section in `system_instructions.md`.
