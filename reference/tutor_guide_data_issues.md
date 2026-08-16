# Tutor & Marker Guide — Part 1: Dataset Data Issues (authoritative for Criterion 2.2 cleansing)

Source: `26S1_BM4088_ICA2_TutorGuide_v1_3.docx`, internal, not released to students.

The dataset has exactly one intentionally-introduced missing-value issue and one intentionally-introduced duplicate issue per scenario, and no other inherent quality issues. Use this table as the reference for what a *substantive* cleansing activity looks like in each scenario — it sharpens band placement between "well-identified, appropriate, clearly explained" (A/B) and "trivial or generic" (D) in `rubric_descriptors.md` §2.2.

| Scenario | Missing-value issue | Expected handling | Duplicate issue | Expected handling |
|---|---|---|---|---|
| 1 | customers.csv, customer_age (~5% null) | Impute mean/median age; justify from distribution | orders.csv, 100 full-row duplicates | Remove duplicates |
| 2 | order_items.csv, discount_rate (~5% null) | Replace with 0 — null means no discount applied. Mean/median imputation is not appropriate here | customers.csv, 100 full-row duplicates | Remove duplicates |
| 3 | order_items.csv, freight_value (~5% null) | Impute mean/median freight **within product category**; justify from distribution | products.csv, 100 full-row duplicates | Remove duplicates |
| 4 | products.csv, cost (~5% null) | Impute mean/median cost **within product category**; justify from distribution | order_items.csv, 100 rows with null order_id | Remove rows — orphaned items can't be linked or imputed |
| 5 | products.csv, price (~5% null) | Impute mean/median price **within product category**; justify from distribution | orders.csv, 100 full-row duplicates | Remove duplicates |
| 6 | products.csv, product_weight_g (~5% null) | Impute mean/median weight **within product category**; justify from distribution | orders.csv, 100 full-row duplicates | Remove duplicates |

## Notes

- Where mean/median imputation is expected, the student still needs to justify the choice from the column's distribution (median for skewed/outlier-heavy, mean for roughly symmetric). Either is acceptable with sound justification — don't require one specific measure.
- **A hardcoded literal value in the final M code is the taught workflow's correct end state, not a shortcut or discrepancy from "computed."** Power Query has no live/dynamic reference — the taught method computes the statistic via a temporary step, records the value, removes that step, then imputes with the recorded value as a literal constant. Checking the M code should confirm the hardcoded value is *correct* (matches the actual mean/median), not flag its being hardcoded at all as a mismatch against the report's claim of a "computed statistic" — see `system_instructions.md`'s 2.2 guidance for the full reasoning.
- **"Within product category" describes the strongest possible version of this activity, not the taught or required one.** Only global (non-grouped) mean/median imputation was covered in lessons. A student who imputes globally, correctly justified from the column's distribution, is doing exactly what was taught and should be fully creditable at the top band — not scored as if they fell short of the grouped version. Grouped imputation is a valid self-directed enhancement to credit when a student does it correctly (per Marking Principle 3, Curriculum Scope), not the baseline expectation this table's wording might otherwise suggest.
- Null `order_delivered_carrier_date` / `order_delivered_customer_date` for cancelled orders are original data, not an introduced issue.
- A student may report a different, genuinely valid cleansing activity instead of the one above (e.g. a real but less impactful issue, or one of these two done differently). Don't penalise the choice itself — assess it on the rubric's own language. But since the dataset has no other inherent issues, an activity that doesn't address either of the two above is more likely to land in the "trivial or generic" band than the "well-identified, appropriate" band. Use the table to inform that judgment, not to auto-fail deviations.
