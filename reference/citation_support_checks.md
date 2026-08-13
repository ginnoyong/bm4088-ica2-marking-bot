# Business-Alignment Check — For 4.2 and 4.3

## Companion to Criteria 4.2 and 4.3 · For Internal Use Only · DRAFT

**Status: drafted as a starting point, not yet reviewed by the marker who identified the underlying gap.** Her original "Adjacent, not covered here" note flagged an unverified-citation risk in 4.2. On review, the citation-support mechanism for predictor-variable citations turned out to belong to 4.1 instead (see `continuity_checks.md`'s Check C) — 4.1 is what actually cites specific EDA findings, since those are the predictor variables the EDA explores. 4.2 and 4.3 don't typically cite anything specific; what they need is a check against a different reference point entirely: does the claim they're making actually connect to the business problem established in 1.1. This file is what's left once that reallocation happened. Treat as provisional until she's reviewed it.

**This file adds one check; it does not replace or amend anything.** `rubric_descriptors.md` remains the sole source of band text and weights, `marking_notes.md` remains authoritative for marking principles, and `system_instructions.md` remains authoritative for per-line workflow. Every finding below lands inside 4.2's or 4.3's own existing band language — no new penalty category.

**Why 1.1, not 3.2, for both of these lines.** 4.2's descriptor language is "directly tied to the *business challenge*" — the target variable's relevance is a business-context question, not an EDA-evidence question; what predictor variables the EDA examined is a different concern that belongs to 4.1. 4.3's descriptor language is "specific and meaningful implications for *business decision-making*" — again a business-context question about the model's results, not about which hypothesis motivated anything. Both lines are ultimately asking the same thing: does this connect back to the actual decision-maker and objective the group set up in 1.1, or does it drift into something generic or unconnected to that.

The check exists because a claim can be well-written and still not actually connect to anything specific. A target-variable justification or a business-implications discussion can use fluent, plausible business language that would read exactly the same regardless of which business problem the group had actually been assigned — which means it hasn't really engaged with *this* decision-maker's *specific* need, even though nothing in it is technically false. Reading either section on its own terms cannot detect that; only checking it against 1.1's actual, specific problem statement can.

---

## Relationship to `system_instructions.md` §5.2

5.2 already applies a structurally similar discipline to the conclusion — cross-referencing its claims against what earlier sections actually found, not judging plausibility in isolation. This check applies the same underlying discipline earlier in the report, to 4.2's and 4.3's own text — but against a different reference point (1.1's problem statement, not 3.2's findings), since these two lines are about business-context alignment, not the same kind of factual-support check 5.2 or 4.1's Check C need.

---

## When this check runs

Requires 1.1's problem statement (business problem, decision-maker, objective, success metric) already established in the case file — reuse it, don't re-ask if it's already been gathered for 1.1's own assessment. If 1.1 hasn't been assessed yet in this session, ask for it, verbatim, before running this check on 4.2 or 4.3.

This check does not require an explicit citation to run — unlike 4.1's Check C, it applies to the discussion generally, since 4.2 and 4.3 typically don't cite anything specific in the first place. It's checking connection, not citation accuracy.

---

## The check

1. **What does 4.2 (or 4.3) actually claim serves the business, and for whom?** State it plainly, in one sentence, before checking anything.
2. **Check this against 1.1's own decision-maker, objective, and success metric.** Does the claim serve the same decision-maker and objective 1.1 established, or does it drift toward a different business concern 1.1 never raised?
3. **Would this text read the same way regardless of which business problem the group had been assigned?** If the language is generic enough to attach to almost any target variable or almost any model's results, it hasn't actually connected to *this* decision-maker's specific need.

### Guard — this is not requiring a literal re-citation of 1.1

**The connection can be implicit and still be genuine — the check is for actual alignment, not for restating 1.1's wording.** A 4.2 or 4.3 passage that clearly serves the same decision-maker and objective 1.1 established, without literally repeating 1.1's language, passes this check. What fails it is a real disconnect: language that could belong to any business problem, or that addresses something 1.1 never established as the actual need.

---

## Where findings land

No new penalty. Route each finding to the descriptor wording it already matches:

| Finding | Line | Descriptor language | Band signal |
|---|---|---|---|
| Claim genuinely serves 1.1's decision-maker and objective, even without literal re-citation | 4.2 or 4.3 | (no issue) | — |
| Language generic enough to belong to any business problem | 4.2 | "generic," "weak connection to the business challenge" | C |
| Language generic enough to belong to any business problem | 4.3 | "superficial," "weakly connected to the scenario" | C |
| Claim drifts to a concern 1.1 never established, or contradicts 1.1's stated objective | 4.2 | "does not relate," "too vague to be credited" | D |
| Claim drifts to a concern 1.1 never established, or contradicts 1.1's stated objective | 4.3 | "little meaningful business discussion" | D |

---

## Recording the evidence

Report as dense itemized evidence, per the Output format compression rule — the judgment that follows stays full prose.

Suggested form:

> **4.2 alignment check** — target's stated relevance: "predicting VIP churn risk supports retention" · 1.1's decision-maker: marketing team, objective: improve order value via targeting · alignment: consistent
>
> **4.3 alignment check** — decision stated: "prioritise retention outreach for high-risk segments" · 1.1's decision-maker: marketing team, objective: improve order value via targeting · alignment: consistent, same decision-maker and objective

Then state the band consequence in prose, citing the descriptor language from the table above.

---

## Open question for the marker who flagged this

Whether this should live as its own file (as drafted here) or be folded into a single companion file spanning 4.1–4.3 together, given the underlying discipline across all three files (verify a claim against what was actually established elsewhere, don't grade plausibility alone) is the same principle throughout, just applied against different reference points per line. Her call.
