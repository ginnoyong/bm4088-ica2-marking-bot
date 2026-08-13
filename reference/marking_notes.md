# BM4088 ICA2 — Marking Notes
## Companion to the Written Report Rubric (Appendix A)

**AY2026/2027 Semester 1 · For Internal Use Only**

> The rubric is the sole basis for assessing student work. These notes clarify how to apply it — they do not add new criteria.

---

## Overall Marking Principle

Award marks strictly according to the rubric descriptors in Appendix A. The suggested directions in the Tutor & Marker Reference Guide exist to help you assess whether a student's choices are reasonable — they are not a checklist or an answer key.

**A student who produces work that meets the A band descriptor receives A band marks** — regardless of whether their hypothesis angles, chart choices, or model selections match the suggested directions in the reference guide.

When in doubt, ask only: does the work meet the rubric descriptor? That is the only question that determines the mark.

---

## Section 1 — Marking Principles

*Judgment-level guidance that applies broadly across submissions.*

### Marking Workflow: The Written Report is the Primary Source

Marking begins with, and centres on, the Written Report. Use the Power BI file, Python Notebook, and other supporting files to **verify** what is reported — not to independently interpret or credit what a student may have intended if it is not reflected in the report.

Do not award marks based on effort or intent inferred solely from supporting files. **Exception:** partial effort visible in the supporting files may be taken into account when awarding marks within the F band, for a component that is otherwise unmet or too weak to credit from the Written Report alone.

If the Written Report's description of a component (e.g. schema design, model algorithm, variables used) does not match what is evident in the supporting files, treat this as a **technical error** and assess it within the existing "minor errors" / "significant errors" band language of the relevant criterion (Criterion 2.1/2.2, 3.1, or Criterion 4) — the severity of the mismatch determines which band applies. A mismatch does not require a separate penalty outside the rubric.

**Exception: Criterion 3's visualization and formatting components (chart type/fields/aggregation, and colour/hierarchy/preattentive attributes) do not follow this workflow.** These assess properties of the rendered Power BI visual itself. Nothing in the rubric requires students to write a justification of their chart or formatting choices — unlike, say, the cleansing activities — so there is no Written Report claim to treat as primary here. For these two components, mark directly from the actual Power BI file (or a marker's description/screenshot of it); the Written Report is not the starting point. Note the EDA section does embed a screenshot of each chart as part of its required structure, but this is documentation of the analysis, not a claim requiring verification — treat it as secondary. If a marker happens to notice the embedded screenshot doesn't match the live file (e.g. formatting was changed after the report was written), that is worth flagging, but it is a low-probability scenario and not something to actively check for.

**The general principle underneath this exception:** if something in the Written Report is a *reproduction* of content that also exists in the supporting files (a screenshot, an embedded copy), mark from the actual supporting file, not the reproduction — a reproduction can go stale if the underlying file changes after it was captured. This is different from Written Report content that is *independently required* by the report's own structure (e.g. the Problem Statement, the Conclusion and Recommendations) and happens to cover similar ground to something in the Power BI file — those sections are not copies of anything, so the Written Report version remains what is graded, and a divergence from the Power BI's own version is a cross-check finding worth noting, not a case of the Written Report being "out of date."

**Two further variations on this workflow, for completeness:**

- **Criterion 3.2 (insight text) follows the standard workflow, even when checked from the same formula used for 3.1's implementation check.** The report's insight claim is primary; the DAX formula and any screenshot verify it. This is a different question from 3.1's — whether the formula itself is correctly built — so the same formula can support two genuinely separate verdicts without contradiction.
- **Criterion 2.1 (schema) and 5.1 (required structure) sit outside the standard workflow too, but differently from 3.1/3.3.** Rather than one side being primary and the other verifying it, both are treated as a genuine two-way comparison — what the marker observes as actually built, checked against what the Written Report describes, with neither side automatically trusted over the other. A mismatch between the two is a finding worth surfacing, not a case of picking a winner.

### Criterion 3 — Exploratory Data Analysis

- A null hypothesis finding (no significant pattern found) is not an automatic fail, nor is it capped at a particular band. Assess the quality of analytical reasoning and relevance to the business scenario — a well-reasoned null finding can score as highly as any other finding, up to the A band.
- There is no single correct chart for any hypothesis. The key test is whether the visualization effectively investigates the stated hypothesis.

**Watch for majority null findings:** if 3 or 4 of the 4 hypotheses yield no meaningful pattern, this is likely to weaken downstream requirements —
- Insights become difficult to connect meaningfully to the business scenario (Criterion 3)
- Justification for training data selection becomes weaker without a clear understanding of relevant variables (Criterion 4)
- The data story becomes difficult to sequence into a coherent narrative (Criterion 5)

Do not penalise null findings in isolation — assess holistically whether the overall body of analysis demonstrates sufficient understanding of the business problem to support the downstream requirements.

### Criterion 4 — Predictive Analytics

- Reproducibility is not assessed. Even on the same platform, results may differ between runs due to package version differences, data preprocessing order, or environment state — a fixed random_state does not guarantee identical results. Do not penalise minor to moderate variation. Do penalise code that does not run, or where a rerun shows a large, qualitative divergence from the reported figures (e.g. accuracy 0.87 vs 0.25) suggesting the code does not do what it is claimed to do.
- **Assess model understanding and discussion based on the figures the student reports in their Written Report** — not on results a marker obtains by independently rerunning the code. Only investigate further if a rerun reveals a large, qualitative divergence as described above. **This describes the ceiling on what re-execution is ever appropriate — it does not mean report-only assessment should be treated as equally confident as code-verified assessment.** Where the code is available, checking the report's claims against it directly (a static read, not a rerun) is the expected default, not an optional extra; report-only assessment stands on its own as legitimate but should be treated as provisional pending that check, not as equivalent to a verified result.

**Model performance is not the goal.** A student who produces a poor-fitting model and correctly explains why — with clear business implications — should score higher than one who produces a good model with no meaningful discussion.

### Criterion 5 — Data Storytelling

- **Structure and narrative quality are two separate judgments, not one combined assessment.** The required Power BI report structure (First Page / Middle Pages / Conclusion and Recommendations) and the all-4-EDA requirement are fixed, presence-and-count facts, assessed entirely on their own — this is not weighed against or blended with storytelling quality. Narrative sequencing, conclusion support, and recommendation quality are a separate judgment, made independently of whether the structure itself is complete.
- Power BI reports exceeding 5 pages are acceptable, provided all pages beyond the required structure are set to hidden. The 5-page limit applies to visible pages only.

### Business Rule Interpretation

Some business rules in the dataset are open to interpretation and may affect the direction of a student's analysis — for example, whether the platform or the customer bears freight fees. Different reasonable interpretations can lead to materially different analyses.

Markers should watch for such variances and award marks according to the rubric descriptors, provided the student offers an acceptable explanation or justification for the interpretation taken in the Written Report. Do not penalise a student solely for choosing a different reasonable interpretation than expected — assess whether their reasoning is sound and consistently applied throughout their analysis.

### Curriculum Scope

Assessment should be scoped to what was actually taught in the module.

- **Students who go beyond the syllabus** (e.g. through self-directed learning or AI assistance) should be credited if they can correctly explain the logic and meaning behind their approach — even if the specific method was not taught in class.
- **Students should not be expected or penalised for not covering techniques or interpretations that were not taught**, even if such techniques would meaningfully enrich the analysis.

Five examples currently in scope for ICA2:

- **Categorical variable encoding for regression models:** LabelEncoder was taught, but for Multiple Linear Regression it produces coefficients that are difficult to interpret meaningfully (e.g. encoding customer segments as 0/1/2 implies an ordinal relationship that does not exist). Students who use alternative methods such as one-hot encoding (`get_dummies`) — even though not explicitly taught — should be credited, provided they can explain the logic and correctly interpret the resulting coefficients.
- **Decision Tree evaluation — feature importance:** Feature importance was not covered in this module. Do not expect or require students to discuss feature importance when interpreting Decision Tree results. For Decision Tree model evaluation, the focus should be on accuracy, precision, and recall — students are not expected to identify which feature is most deterministic given current course coverage.
- **Problem statement scope and limitations/constraints:** this component was not sufficiently covered in lessons and was omitted from ICA1 practice. Its absence alone should not cap a problem statement's band the way a missing business problem, objectives, or success metric would — weigh it as a plus when present, not a required element whose absence is penalised the same as the other three.
- **Schema enhancements beyond the standard structure:** the standard schema (customers/orders/order_items/products/sellers) is the baseline every submission starts from, not an exhaustive one. A student who builds additional correctly-implemented relationships beyond it — e.g. using Power Query's Merge Queries to add a direct foreign key so a table connects straight to a dimension it would otherwise only reach indirectly, producing a cleaner star schema — has gone beyond the baseline, not deviated from it. This technique was not explicitly taught; credit it the same as any other self-directed technique, provided it is correctly implemented and the student can explain what they did.
- **Global vs. grouped imputation for cleansing:** only global mean/median imputation was covered in lessons. Global, correctly justified, is fully creditable at the top band on its own — not a lesser fallback. Grouped (per-category) imputation is a valid self-directed enhancement to credit when correctly executed, but is not the expected standard global is measured against. See Section 2's Criterion 2 notes below for scenario-specific detail.

### Appendix B — Presentation (Content Criterion)

- The predictive analytics segment should focus on business implications of the model, not technical details already covered in the written report. Do not penalise students for not repeating technical explanation in the presentation.

### General

- Where a required submission (Power BI file, Python Notebook, or supporting evidence) is missing or inaccessible, the components that cannot be verified are treated as unmet and marked within the F band.

---

## Section 2 — Scenario & Technical Detail Notes

*Reference-level detail for specific data handling and format questions.*

### Criterion 2 — Data Modelling and Cleansing

- Students report exactly TWO (2) data cleansing activities. Assess the quality and justification of those two — not whether more were performed.
- Grouped imputation (e.g. mean/median per product category) is a valid enhancement when correctly executed, but global imputation is not weaker or less rigorous — only global mean/median imputation was covered in lessons, and it is fully creditable at the top band on its own. Do not treat grouped as the expected standard global falls short of.
- Scenario 2 (discount_rate nulls): replacing with 0 is the only defensible approach — a null discount rate has a clear business meaning (no discount applied). Mean/median imputation here is not appropriate.
- Scenario 4 (null order_id in order_items): row removal is the only valid approach — these records cannot be meaningfully imputed.
- Existing null delivery dates (order_delivered_carrier_date, order_delivered_customer_date) are null for cancelled orders in all datasets. This is a data characteristic, not a quality issue. Credit students who correctly identify "no action required" with justification. Do not credit imputation or removal of these rows as one of the two required activities.

### Criterion 4 — Predictive Analytics (Detail)

- Class imbalance (Scenarios 1 and 5): cancellation models will show high accuracy but near-zero recall. Use as a guide — reports accuracy only (basic) → discusses precision/recall (good) → connects imbalance to business implications (strong).
- Scenario 3 linear regression on freight value: poor model fit is expected and acceptable. Assess the quality of the student's explanation for why it underperforms and what that implies for the business.
- Python Notebook (.ipynb) is submitted as a file, not a sharing link. If missing or non-functional, treat the unverifiable components as unmet and mark within the F band.
