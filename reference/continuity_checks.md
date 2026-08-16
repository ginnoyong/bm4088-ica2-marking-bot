# Continuity Checks — EDA to Model, and Power BI to Notebook

## Companion to Criterion 4.1 · For Internal Use Only

**This file adds three checks; it does not replace or amend anything.** `rubric_descriptors.md` remains the sole source of band text and weights, `marking_notes.md` remains authoritative for marking principles, and `system_instructions.md` remains authoritative for per-line workflow. Nothing here introduces a new criterion, a new weight, or a penalty outside the existing descriptors — every finding below lands inside 4.1's own band language.

All three checks exist because a feature set can be described in fluent, plausible prose and still have no logical continuity with the analysis that preceded it — or cite that analysis inaccurately. Reading the justification on its own terms cannot detect either problem; only comparing it against the group's own earlier work can.

---

## Relationship to the existing null-findings knock-on

`marking_notes.md` (Criterion 3) and `system_instructions.md` ("Hold the whole submission in mind") already describe a knock-on effect: where 3 or 4 of the 4 hypotheses yield no meaningful pattern, 4.1's justification and 5.2's sequencing are weakened, because both depend on an understanding of relevant variables built up through the EDA.

**That note is unchanged and keeps its own trigger.** The checks below are separate and differ from it in two ways:

- **They run regardless of how the hypotheses turned out.** A submission where all four hypotheses produced strong findings can still fail continuity, by not using any of them.
- **They run in both directions.** The existing note asks whether weak EDA degrades 4.1. These ask whether 4.1 reflects the EDA at all, strong or weak.

Both can fire on the same submission. Do not treat one as covering the other.

---

## When these checks run

| Check | Requires in the case file | If only one side is present |
|---|---|---|
| A — EDA to feature selection | The EDA insights/findings (from 3.2) **and** the report's stated explanatory variable list, **and** the notebook's actual variable list | 4.1 stays Provisional; Status names which side is missing |
| B — Power BI to notebook | The notebook's data-preparation code **and** the Power Query steps or Applied Steps | 4.1 stays Provisional; Status names which side is missing |

Check B does not apply where the model's preparation legitimately has no Power BI counterpart — say so rather than recording a finding.

---

## Check A — EDA to feature selection continuity

Four questions. Each produces a countable or quotable fact, not an impression.

1. **How many explanatory variables correspond to something the EDA examined? State the count.**
   Report as a ratio (e.g. "4 of 23 strictly, 7 counting adjacent variants"). Count generously and say so — a state-level variable where the EDA examined city level is adjacent, not absent.

2. **Was any factor the EDA found weak, absent, or non-varying retained as a predictor? Is that acknowledged?**
   Check the retained variable's actual distribution in the training data, not just the EDA's verdict on it. A factor the EDA found weak may be a defensible inclusion; a factor with no variance at all is not, and the two are worth distinguishing.

3. **Was any factor the EDA found significant left out? Is that acknowledged?**
   Omission is not automatically a fault — a group may have sound reasons. Silent omission of their own strongest finding is the finding.

4. **Do variables outside EDA coverage carry their own reasoning, or only a shared category label?**
   A single sentence naming broad groupings ("operational, product, seller and customer factors") is a category label, not reasoning. Ask whether the text would read differently if a different variable set had been chosen; if not, it is not justifying anything specific.

### Guard — do not turn this into "variables must come from EDA"

Students develop four hypotheses and may reasonably train on twenty or more variables. **Most feature sets will sit outside EDA coverage, and that is normal, expected, and not a fault.** Domain-driven or exploratory feature selection is legitimate and should be credited when reasoned.

The two things actually being assessed are narrower:

- Variables outside the EDA's scope carry **their own** reasoning
- Findings the EDA **did** produce are reflected in the selection, or explicitly set aside with a stated reason

A submission that satisfies both passes this check with a low EDA-overlap count. A submission that satisfies neither fails it even if every variable happens to trace back to a hypothesis.

---

---

## Check C — variable citation support

For any predictor variable whose justification cites a specific EDA finding (not a general appeal to "the analysis," a named hypothesis or EDA entry specifically):

1. **Identify what the citation claims the finding shows.** State it in one sentence before checking anything.
2. **Check the cited finding's actual, established result** — reuse whatever's already in the case file from 3.2 rather than re-deriving it. If the specific finding cited hasn't been assessed yet in this session, ask for the Written Report's own text for it, verbatim.
3. **Does the actual finding support the claim, partially support it, or not support it at all?**
   - Full support: the finding genuinely shows what the citation says it shows.
   - Partial support: the finding shows something related but weaker or narrower than claimed — acceptable if the report itself acknowledges the gap.
   - No support: the finding is null, contradicts the claim, or shows something substantively different.

**This is separate from Check A's Question 4, not a duplicate of it.** Question 4 sweeps every non-cited variable and asks whether it carries its own reasoning at all, generic or specific. Check C only activates when a variable's justification names a *specific* EDA finding, and verifies that finding is represented accurately — a targeted check on cited variables, not a sweep of uncited ones.

### Guard — acknowledged weakness is not a failure

A citation to a weak or mixed finding is not automatically a problem — the fault is specifically unacknowledged misrepresentation, not citing anything short of a strong result. "While H2 showed only a modest effect, it's directionally consistent with..." correctly represents a weak finding as weak and still uses it as legitimate context.

### Guard — the penalty attaches to the misrepresentation, not independently to reusing a flawed object

**When a predictor variable is computed from an object already found flawed elsewhere (a mis-grained DAX column, an invalid categorization confirmed at 3.1/3.2), that fact is context for judging the justification's honesty — it is not a second, independent penalty on top of whatever the misrepresentation earns.** Test this with the same honesty check Check C already uses: if the report had accurately disclosed the known flaw and reasonably justified proceeding anyway ("this categorization was later found unreliable, but we retain it here because..."), the flaw itself would already be fully priced into 3.1/3.2's band — that variable's inclusion should not *also* independently cap 4.1 for the flaw's mere presence. What 4.1 can catch is only whether the justification accurately represents what was already known about the variable, per Check C above. Do not describe "the predictors are drawn from a confirmed-invalid column" as a standalone finding in its own right — state it as the evidence establishing how serious a misrepresentation is, not as a second, separately-counted fault.

---

## Check B — Power BI to notebook pipeline continuity

Whether the model's data preparation continues from the Power BI work or restarts independently.

1. **Does the notebook read the raw source files, or the Power BI output?**
2. **Are Requirement 2's cleansing decisions reproduced, altered, or dropped?**
3. **Where the two differ — different imputation statistic, different filtering, different grain — is the difference acknowledged in the report?**
4. **Do both pipelines treat the same field the same way, and yield consistent row counts?**

Question 4 is the one that surfaces problems the report cannot. Compare row counts per table across the two pipelines and check the treatment of any field cleansed in both. A field imputed with the mean in Power BI and the median in Python is two different datasets underlying two different requirements.

### Non-penalty clause — as important as the check itself

**Preparing data in Python from the raw source files is permitted by the assignment and is not a fault in itself.** Requirement 4 states the dataset must not be modified outside of Power BI and the online Python notebook — both tools are sanctioned, and a group may legitimately do all of their model preparation in the notebook. Re-reading raw files, re-applying cleansing, or preparing the training data independently of the Power BI model are all acceptable choices.

What is assessed is only:

- whether the report's account of the preparation matches what the code actually does, and
- whether divergence between the two pipelines is acknowledged.

**Unacknowledged divergence is a code/description discrepancy under 4.1's own band language** — "minor discrepancies between the code and the written description" (C), "significant discrepancies" (D), "not implemented as described" (F). It has a home in the existing descriptor and needs no separate penalty. Do not record it as an additional deduction on top of the band.

A group that says plainly "the model data was prepared independently in Python from the raw files, because X" has no finding against them here, however different the two pipelines are.

---

## Where findings land in 4.1's band language

No new penalty. Route each finding to the descriptor wording it matches:

| Finding | Descriptor language | Band signal |
|---|---|---|
| Variables stated in the report differ from those in the code | "minor discrepancies between the code and the written description" | C |
| Pipeline divergence unacknowledged, materially different data | "significant discrepancies between the code and the written description" | D |
| Predictor retained after the group's own EDA showed it non-varying or unrelated, unacknowledged | "Variable/cluster selection is weak or questionable" | D |
| Majority of variables carry no reasoning beyond a shared category label | "Variable/cluster selection is weak or questionable" · "justification is limited"/"weak" | C or D |
| A cited EDA finding overstates a weak/null result as strong, unacknowledged | "Variable/cluster selection is weak or questionable" | C or D |
| A cited EDA finding is directly contradicted by its actual result | "Variable/cluster selection is weak or questionable" | D |
| Preparation described but not present in the code | "not implemented as described" | F |

**Two named patterns for "questionable" selection.** The D descriptor's "weak or questionable" is otherwise a judgment call that tends to default upward when the implementation is clean. These two patterns are instances of it, and either one on its own supports D:

- a predictor retained after the group's own EDA showed it has no variation or no relationship, with no acknowledgement
- a feature set where the majority of variables have no stated reasoning beyond a shared category label

Implementation quality does not offset either. 4.1's A descriptor is justification-led — "well-justified, clearly appropriate, and correctly implemented" — with implementation named once, as one of three qualities in the construction half, and not at all in the variable-selection half. Per Marking Principle 12, a correctly built model with a poorly reasoned feature set is not a well-justified one.

---

## Recording the evidence

Report both checks as dense itemized evidence, per the Output format compression rule — the judgment that follows stays full prose.

Suggested form:

> **Check A** — EDA overlap 4/23 strict, 7/23 adjacent · non-varying predictor retained: yes, unacknowledged · significant EDA factor omitted: no · non-EDA variables reasoned: shared category label only
>
> **Check C** — "H2 supports VIP-tier relevance" claimed for `is_vip_flag` · H2's actual verdict: null (per 3.2) · acknowledged in text: no · support: none
>
> **Check B** — notebook source: raw files · R2 cleansing: re-done, altered · divergence acknowledged: no · same-field treatment: differs (mean vs median) · row counts: differ on fact table

Then state the band consequence in prose, citing the descriptor language from the table above.

---

## Adjacent, not covered here

One related gap sits in **4.2**, not 4.1, and is not addressed by either check above: where a report cites a hypothesis or EDA finding as justification for the target variable, the cited finding should be checked to confirm it actually supports the claim. A citation to a hypothesis that returned a null result is not support for anything. `system_instructions.md` §5.2 already applies this discipline to the conclusion; §4.2 currently has no equivalent. Noted here so it isn't lost — deciding whether to add it is a separate call.
