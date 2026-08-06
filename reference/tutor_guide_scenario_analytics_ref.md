# Tutor & Marker Guide — Part 2: Scenario Analytics Reference (background plausibility check only — NOT an answer key)

Source: `26S1_BM4088_ICA2_TutorGuide_v1_3.docx`, internal, not released to students.

**This is not a source of correct answers.** Per the guide's own note and the marking notes' overarching principle: a student whose hypothesis angle, model choice, or target variable differs from the directions below, but meets the rubric descriptor, gets full marks for that band. Do not compare a student's choices against this table to check if they "got it right." Use it only to recognise when an unusual-looking result is actually expected, so it isn't mistaken for a modelling error.

**EDA — Acceptable Variations (verbatim from the guide):** "Students may discover the same patterns through different chart types or variable combinations. The key criterion is whether the visualization effectively tests the stated hypothesis — there is no single correct chart for each hypothesis." Applies directly to 3.1 — don't cap a band because a chart type differs from what's suggested below, only because it fails to test the hypothesis it's paired with.

## EDA Directions (background reference for 3.1 and 3.2 plausibility only)

| Scenario | Hypothesis Angle | Expected Direction |
|---|---|---|
| 1 — Delivery Performance | Cancellation rate by product category | Electronics highest, Toys lowest |
| 1 | Cancellation rate by quarter | Q4 cancellation rate nearly doubles compared to Q1–Q3 |
| 1 | Cancellation rate by customer state | Noticeable variation across states |
| 1 | Cancellation rate by order value | Higher-value orders show higher cancellation rates |
| 1 | Delivery delay by product category | Variation in delay rates across categories |
| 1 | Delivery delay by seller state | Variation in delay rates across seller locations |
| 2 — Customer Basket Analysis | Multi-category order rate by customer segment | VIP segment shows significantly higher multi-category rate than Consumer and Corporate |
| 2 | Order value by number of categories purchased | Order value increases meaningfully with each additional category in the basket |
| 2 | Top category combinations in multi-item orders | Certain category pairings dominate multi-category orders |
| 2 | Item count by customer segment | VIP segment purchases significantly more items per order |
| 2 | Multi-category rate by customer state | Minimal variation across states — geography is not a strong differentiator |
| 3 — Shipping Cost Optimisation | Freight as % of item price by category | Books and Toys have freight costs that are a very high multiple of item price; Electronics is low |
| 3 | % of items where freight exceeds item price | Books and Toys have a very high proportion of items where freight exceeds product value |
| 3 | Freight by seller state | Significant geographic variation in average freight cost by seller location |
| 3 | Freight by customer state | Geographic variation in average freight cost by customer location |
| 3 | Freight by product weight band | Heavier products incur higher freight costs |
| 3 | Order freight as % of order value by category | Books and Toys carry disproportionately high freight burden relative to order value |
| 4 — Product Portfolio Profitability | Revenue share vs margin % by category | Electronics dominates revenue but only the 3rd highest in margin %; Fashion has the highest margin but low revenue share — a core tension in the portfolio |
| 4 | Margin % by price band | Top 4 (out of 10) price bands contribute to the highest and lowest 4 margin % performance; higher price does not equate with higher margin % |
| 4 | Revenue growth by category year-on-year | Electronics growth dominates; other categories grow at slower rates |
| 4 | Discount impact on margin by category | Fashion is the only discounted category but has the highest average margin % |
| 5 — Seasonal Performance | Order volume by year and quarter | Q4 is consistently the highest-volume quarter every year; clear year-on-year growth trend |
| 5 | Cancellation rate by quarter | Q4 cancellation rate is significantly higher than other quarters — nearly doubles |
| 5 | Cancellation by quarter and category | Q4 cancellation spike is consistent across all product categories, suggesting a platform-wide issue |
| 5 | Month-level cancellation | December shows a particularly sharp spike in cancellation rate |
| 5 | Order value by quarter | Q4 has higher average order value alongside higher cancellation rates |
| 6 — Demand Patterns | Revenue by category | Electronics dominates revenue; significant gap between electronics and other categories |
| 6 | Demand (order count) by category | Large variation in order volume across categories; Electronics far outpaces others |
| 6 | Demand by customer geography | Demand is concentrated in certain states, particularly CA |
| 6 | Price vs demand | Higher-priced products tend to have higher demand — counterintuitive and worth exploring |
| 6 | Physical specs (weight) by category | Significant weight differences across categories; furniture heaviest, fashion lightest |
| 6 | Margin % by category | Fashion has the highest margin %; Electronics the lowest |

Notes from the source: for Scenario 1, the delay range is narrow — cancellation patterns tend to be more revealing than delay distributions, but a student focusing on delay isn't wrong for it. For Scenario 2, gender/age/geography show almost no variation for repeat purchase or order value — a student exploring these and finding a weak result has made a valid finding, not a mistake. For Scenario 4, overall margin % is relatively flat across years, so that specific angle tends to be unproductive, but again isn't an error to have tried.

## Predictive Analytics (background reference for Criterion 4 plausibility only)

| Scenario | Typical model / target | Expected behaviour to recognise as normal |
|---|---|---|
| 1 — Delivery Performance | Cancellation or delivery-delay (binary) | Class imbalance expected — high accuracy, near-zero recall is a normal, creditable finding if discussed, not a broken model |
| 2 — Customer Basket Analysis | Order value (Multiple Linear Regression) | Item count typically dominant driver; reasonable fit expected |
| 3 — Shipping Cost Optimisation | Freight value (Multiple Linear Regression) or high-freight (binary) | Regression on freight value is expected to fit poorly — this is acceptable; assess the explanation, not the R² |
| 4 — Product Portfolio Profitability | Product demand (Linear Regression or Decision Tree) | Category typically the dominant driver |
| 5 — Seasonal Performance | Order cancellation (binary) or monthly order volume (regression/forecasting) | Same class-imbalance pattern as Scenario 1 if cancellation is chosen; quarter/month typically strong predictors |
| 6 — Demand Patterns | Product demand (regression) or K-Means clustering (k≈3) | Category typically the dominant driver for regression; clusters expected to map loosely to product categories for clustering |

## Use these tables only to

- Avoid flagging an expected poor fit or expected class imbalance as if it were a technical error (Predictive Analytics table)
- Sanity-check whether a stated evaluation metric is being interpreted sensibly for that kind of target (e.g. recognising that "accuracy only" under class imbalance is a shallower discussion than one that addresses precision/recall)
- Recognise when an EDA finding that looks "wrong" or "weak" is actually an expected/valid result for that scenario (EDA Directions table), so it isn't mistaken for a poorly executed analysis

## Do not use them to

- Judge whether a hypothesis "should" have been about a different angle
- Judge whether a different target variable, algorithm, or clustering approach "should" have been chosen
- Judge whether a different chart type "should" have been used, per the "EDA — Acceptable Variations" note above
- Cap a band because the direction of a result, or the angle of a hypothesis, differs from what's shown here
