# Data Visualization and Storytelling Design Principles (3.3 and 5.3 reference)

Source: W3S11 (Data Visualization and Infographics), W3S12 (Communicating Data Effectively), W3S21/W7S21 (Data Visualization Best Practices / Format Visuals in Power BI), W7S22 (Creating Dashboard for Data Storytelling), W7S11 (Data Storytelling). Grounds 3.3 and 5.3 assessment in what was actually taught, per Curriculum Scope — not a generic design-eye standard. The first four sections below (Preattentive Attributes through Tufte's Principles) ground 3.3, chart-level formatting. The two sections after that (Dashboard-Level Design Principles, Data Storytelling Principles) ground 5.3, report-level design and content framing.

## Preattentive Attributes

Visual properties the brain processes almost instantly and unconsciously, before conscious attention engages — used to make key information register at a glance rather than requiring a viewer to search for it. Four categories taught:

- **Form** — shape, size, orientation, length
- **Spatial Position** — 2D position, grouping/proximity
- **Movement** — animation, motion (rarely applicable to a static Power BI chart, but relevant if the report describes an animated/play-axis visual)
- **Colour** — hue, intensity, saturation

What to look for: is at least one preattentive attribute used deliberately to make a specific data point or category register immediately — e.g. one bar coloured differently from the rest to flag an outlier, a KPI made larger to signal importance, a trend line's steepest segment highlighted. Effective use is deliberate and tied to the chart's actual message, not decorative variation with no informational purpose.

## Colour Theory

**Match the colour scheme to the data type:**
- Categorical/qualitative data (e.g. product category, gender) → qualitative colour schemes — varied hues, no implied order or magnitude
- Sequential data (e.g. temperature, income level, anything with natural order) → sequential schemes — gradual shifts in lightness/saturation, lighter = lower value, darker = higher
- Diverging data with a meaningful midpoint (e.g. profit/loss around zero) → diverging schemes — two contrasting colours branching from a neutral centre

A chart using the wrong category here (e.g. a qualitative rainbow palette on sequential data, implying false categorical distinctness where there's actually a continuum) is a real formatting weakness to note specifically, not just "colour could be better."

**Use colour to direct focus:**
- Bold, high-contrast colour on the data points that matter (peaks, trends, anomalies, the specific finding the insight is about)
- Muted/neutral tones for background and secondary data, preserving context without competing for attention
- Avoid overusing bright/saturated colour across many elements at once — this creates clutter and defeats the purpose; reserve vivid colour for what's actually significant

## Visual Hierarchy

Using size, spatial position, and spacing together to assign visual weight and control the order in which a viewer processes information — the most important element should register first. Concretely: a KPI card made dominant through size and generous surrounding whitespace; in a stacked bar/column chart, the bottom/left sub-component typically carries the highest visual hierarchy and registers first.

## Tufte's Principles

The taught rationale underlying the above three techniques:

- **Show the Data** — the visualization should foreground the actual data, not decoration
- **Maximize Data-ink Ratio** — data-ink is the portion of ink/pixels representing actual data. Erase non-data ink where it adds no information (unnecessary 3D effects, heavy gridlines, decorative borders) and erase redundant data-ink (legends/labels duplicating information already conveyed elsewhere in the chart)
- **Avoid Chart Junk** — no decorative elements that don't serve the message
- **Use Small Multiples** — a series of similar charts sharing the same scale and design, enabling easy comparison across categories or time periods, where applicable
- **Show Data Variation, not Design Variation** — differences a viewer perceives should reflect real differences in the data, not inconsistent formatting choices across the same report
- **Integrate Text and Graphics** — labels, annotations, and titles should be part of the visual's communication, not a separate disconnected block of text
- **Use Visualizations to Reveal the Truth** — the chart should represent the underlying data honestly, not distort or mislead (e.g. a truncated y-axis exaggerating a small difference)

## How to use this file for 3.3

- This is a teachable, checkable framework, not a subjective aesthetic standard — ground every observation in one of the specific techniques above rather than a vague overall impression ("the colour scheme is sequential where the data is actually categorical, which understates the distinctness of these groups" rather than "the colours aren't great").
- 3.3 is inherently more of a judgment call than most other in-scope lines — even with this framework, reasonable people can land in different places on the same chart. Say so explicitly in the justification when a genuinely different reasonable read exists, rather than presenting the verdict with more certainty than it has.
- Do not re-assess chart type, fields, or aggregation here — that's 3.1's job. 3.3 is about how the chosen chart is formatted, not whether the chart choice itself was right.
- A screenshot is required for this line — there is no text-description fallback the way other lines have one. Formatting quality genuinely can't be judged from a typed description of what colours were used; the actual rendered chart is needed every time.

## Dashboard-Level Design Principles (5.3 reference — visual/layout half)

Source: W7S22 (Creating Dashboard for Data Storytelling). This is the *dashboard design* half of 5.3's descriptor — the report-wide equivalent of the chart-level content above. Do not re-check chart type here (3.1's job) or per-chart formatting (3.3's job) — this is about the report as a whole: layout, colour consistency across pages, and simplicity at the report level.

**Positive attributes:**
- **A page carrying multiple visuals — the normal case for a dashboard — should group visuals that are coherently related: serving one shared question, theme, or part of the narrative, not an arbitrary or unrelated collection sharing a page for space reasons alone.** "Dashboard" itself means multiple coordinated visuals on one interface — that's the design task this half of 5.3 is actually assessing, not something to be avoided. For this assignment specifically, the structure requires 4 EDA visualizations plus the predictive analytics outcome — 5 required pieces of content — fitting into only 3 middle pages (5-page limit, minus the First Page, minus the Conclusion & Recommendations page); at least two of the three middle pages will necessarily carry more than one required visual, and no compliant layout can avoid this. **Never treat a page carrying multiple required visuals as a deviation on its own — that would penalise the exact thing "dashboard design" asks for.** What's actually assessable is the *coherence of the grouping*: do the visuals sharing a page work together (one finding setting up another, a shared theme, a natural sequence), or do they read as arbitrary or crowded regardless of visual tidiness. Treat strong, deliberate grouping as a plus to credit; treat weak or incidental grouping as neutral, not as a flaw to penalise, since some grouping was always going to be necessary and the group still had to choose *something*.
- Keep a clean and compact layout
- Select a suitable, *consistent* colour theme — a limited set of colours, applied consistently across pages, not varying styling page to page
- Keep it simple and easy to use

**Negative attributes:**
- Cluttering the dashboard with unimportant, decorative, or unrelated information — not "more than one chart" on its own, but content that doesn't serve the page's shared theme or that's present for filler rather than purpose
- Over-designed or too flashy graphics/layout
- Overuse of colours, or colour used only for decoration with no meaning attached to it
- Too much complexity — metrics or visuals that don't clearly serve the message

**On "simplicity" specifically — this is not the same standard as chart-level simplicity (3.3's Tufte grounding).** At the chart level, decorative elements are discouraged because they add non-data ink with no informational purpose. At the report/dashboard level, some decorative or illustrative elements are legitimate storytelling devices, not clutter — an icon reinforcing a KPI's meaning, a background image establishing business context, an annotation calling out a key takeaway. The test isn't "is there any decoration," it's "does this decoration serve understanding and impact, or is it purely ornamental and distracting." Ask what purpose, if any, a decorative element serves before treating its presence as a simplicity violation.

**On "accuracy" — deliberately not a separate 5.3 checklist item.** Visual accuracy/honesty (no truncated axes, no distorted scales) is already covered under 3.3's Tufte grounding ("Use Visualizations to Reveal the Truth," above) on a per-chart basis. Re-checking it here would be redundant — don't ask the marker for this again at the report level.

**5.3 checklist to ask the marker for (Description, not verbatim — same reasoning as other observed-facts checks):**
- How many visuals appear on the busiest page? Any overlapping or cut-off content, or significant unused empty space on any page?
- What chart type(s) appear on the First Page, the predictive analytics outcomes page, and the Conclusion page (EDA chart choices are already covered by 3.1 — don't re-ask about those pages here)
- The main colours used, what each represents, and whether one consistent Power BI theme was applied throughout or styling differs page to page
- Any decorative elements present (icons, images, borders, backgrounds) and what purpose, if any, they serve

A screenshot of one or two representative pages is useful supplementary evidence here, same as 3.1, but not mandatory the way it is for 3.3 — most of this checklist is factual and observable without needing the rendered image.

## Data Storytelling Principles (5.3 reference — content/framing half)

Source: W7S11 (Data Storytelling). This is the *data storytelling* half of 5.3's descriptor — about whether the report's insights and conclusion are framed with context and turned into actionable insights, not about visuals at all. This reuses text already supplied for 3.2 (insight text) and 5.2 (conclusion and recommendations) — no new input needed from the marker for this half.

**Context and Benchmarking.** "A number without context is just a number" — every metric needs a reference point telling the audience whether it's good, bad, expected, or surprising. Four reference points taught:
- vs Target
- vs Last period
- vs Same period last year
- vs Benchmark/Competitor

A finding presented as a raw, isolated number ("website traffic increased by 15,000 visitors this month") has no way to be judged as good or bad without one of these. Check whether the report's key insights and conclusion use at least one such reference point, rather than presenting figures in isolation.

**The "So What?" Test.** Before a finding is presented, it should be able to answer: does this matter, what should be done, and who should do it. Three-question checklist that turns an observation into an insight:
- **So what?** — why does this finding matter to this specific audience?
- **Now what?** — what action or decision does this finding point to?
- **For whom?** — who in the audience needs to act, and what do they need to do?

An observation ("42% of customers churned") is not yet an insight until it can answer all three (e.g. "Basic and Standard subscribers churn at twice the rate of Premium — the business should prioritise retention efforts there, and marketing needs to run a targeted campaign"). Check whether the report's conclusion and key insights read as insights in this sense, or remain at the level of raw observations.
