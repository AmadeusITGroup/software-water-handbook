# Cross-Provider Parameter Tables

Combined, computation-ready parameters aggregated across all companies, for
comparison and lookup.

## Contents

Themed parameter tables, combined across every extracted provider:

- `wue_all_providers.csv` — Water Usage Effectiveness (energy-denominated intensity)
- `per_unit_water_all_providers.csv` — non-energy intensities (e.g. water per AI prompt)
- `water_volumes_all_providers.csv` — withdrawal/consumption/discharge volumes
- `water_shares_all_providers.csv` — percentage-share metrics
- `replenishment_and_progress_all_providers.csv` — replenishment / avoided / progress

Plus:

- `restatements.csv` — every case where two report editions report the **same fact**
  with a **different value** (a provider restatement). See "How duplicates and
  restatements are handled" below.
- `datapackage.json` — the canonical Frictionless data dictionary describing all
  table schemas (the themed tables plus `restatements`). Shared by these combined
  tables **and** the per-company `<company>/csv/<theme>.csv` tables, which use the
  same field schemas.
- `derive_parameters.py` — regenerates all parameter tables from the JSON
  extractions:
  - per company → `<company>/csv/<theme>.csv`
  - combined → `cross_provider/<theme>_all_providers.csv`
  - restatements → `cross_provider/restatements.csv`

## How duplicates and restatements are handled (latest-per-key)

Providers publish **multi-year historical tables in every report**, so successive
editions overlap (e.g. Google's 2025 and 2026 reports both report 2021–2024). The
derivation applies one rule when building the tables:

> **Complementary → keep both. Same fact → keep the most recent report.**

- A row's **identity** is `(provider, metric, water_flow, geography, period, …)` —
  every descriptive column except the value. Rows with **different** identity are
  complementary and all kept (different year, flow, location, or provider).
- Rows with the **same** identity coming from **different report editions** are the
  same fact reported twice. Only the value from the **most recent** report
  (highest `report_year`) is kept; the older duplicate is dropped from the tables.
- If those editions **disagree** on the value, it is a provider **restatement** and
  is logged in [`restatements.csv`](restatements.csv) (superseded vs kept value,
  with both report ids and years).
- **Guard against over-merging:** if a single report contributes more than one row
  to the same identity (e.g. low/medium/high risk shares, or two avoided-water
  sub-metrics that share columns), those are genuinely distinct facts, so they are
  **all kept** and never collapsed.

The full history (every edition, including superseded values) always remains in the
per-company `json/` — the source of truth. Each CSV row carries `report_year` and
`source_report_id` so its edition is explicit. This runs automatically in
`derive_parameters.py`; no manual filtering is needed to avoid double-counting.

## What is comparable across providers — and what is not

These tables put three providers side by side, but **most of the headline
numbers are not directly comparable**. Before comparing any two values, check
that they agree on the six dimensions below. The `water_flow`, `caveat`,
`source_report_id`, and `period` columns exist so you can do this.

### Comparability by metric family

**Recommended comparison snapshot: each provider's most recent report** — AWS **2025**
(Amazon 2025 report), Google **2025** (2026 report), Microsoft **FY25** (2026 factsheet).
Using the newest edition per provider maximises temporal alignment and avoids the Google
edition-overlap. **Note:** Microsoft's **FY25 is a fiscal year** (≈ mid-2024 to mid-2025),
so it is offset ~6 months from AWS's and Google's calendar 2025. The table below is that
snapshot; ranges shown are regional/sub-annual spread within it (not multi-year trends).

**Note on Microsoft WUE.** For a like-for-like **global-to-global** comparison, the matrix
uses Microsoft's **global FY25 WUE (0.27)** — the value in the 2026 annual report, matching
AWS's global fleet figure. Microsoft also reports **FY25 WUE by region** (Americas 0.34,
Asia Pacific 0.25, EMEA 0.03), but on its **datacenter efficiency web page** rather than in
the annual report. That regional breakdown is the **same FY25 period** (current, not older);
it is simply a different document and a finer resolution, and it is the value the Microsoft
[`worked_example.md`](../microsoft/worked_example.md) uses for a region-specific workload.

| Metric family | Amazon (AWS) | Google | Microsoft | Directly comparable? |
|---------------|:---:|:---:|:---:|---|
| **WUE (L/kWh)** | ✅ 0.12 (2025 global fleet) | ❌ none published | ✅ 0.27 (FY25 global) | **No** — different water flow and energy denominator (see below) |
| **Per-unit (per prompt)** | ❌ | ✅ 0.26 mL/prompt (Gemini) | ❌ | **No** — only Google; a single **global median** (blended fleet-average), Gemini text prompts only, not per-location and not generic cloud |
| **Volumes: withdrawal** | ✅ (fleet only) | ✅ (global + per site) | ✅ (global + regional + 29 sites) | Only at matching resolution + year |
| **Volumes: consumption** | ❌ not reported | ✅ (global + per site) | ✅ (global + regional) | AWS cannot be compared here at all |
| **Volumes: discharge** | ❌ not reported | ✅ (global + per site) | ✅ (global + regional) | AWS cannot be compared here at all |
| **At-risk / water-stress share** | ✅ (WRI Aqueduct, 2030 BAU) | ✅ (Google's own DC Water Risk Framework) | ✅ (WRI Aqueduct, current baseline) | **No** — mixed frameworks, scenarios, and thresholds (see below) |
| **Replenishment / progress** | ✅ | ✅ | ✅ | **No** — different units and accounting methods |

> **On the water-stress share row:** all three report a stress breakdown, but they
> are still not comparable.
> - **Amazon (AWS)** uses **WRI Aqueduct**, but on the **2030 business-as-usual
>   baseline scenario** (a *future-projected* stress level, source-water-stress
>   basis, leased and owned data centres): 48% low, 22% high/extremely high (2025).
> - **Microsoft** also uses **WRI Aqueduct**, but on the **current baseline
>   water-stress** classification (high/extremely-high threshold), corporate
>   operations: 50% of withdrawal, 54% of discharge, 48% of consumption (FY25).
> - **Google** does **not** use Aqueduct for this figure — its published at-risk
>   share is for **data centres** and uses **Google's own proprietary Data Center
>   Water Risk Framework** (scarcity + depletion, low/medium/high). Google applies
>   Aqueduct + WWF only to its *office* operations, which this share doesn't cover.
>
> So even the two Aqueduct users (AWS and Microsoft) differ on the **scenario**
> (2030 projection vs current), the **basis** (source water stress vs baseline
> water stress), and the **reporting boundary** — and Google uses a different tool
> entirely. Do not line these percentages up as if they were the same metric.

### Year coverage — this is multi-year data, not a single snapshot

The single-year figures quoted above (e.g. 2025 / FY25) are **latest-year snapshots**
for illustration. The extractions actually span several years, and the coverage is
**uneven across providers**, which matters for any trend or time-series comparison:

| Metric family | Amazon (AWS) | Google | Microsoft |
|---------------|--------------|--------|-----------|
| Volumes | 2025 only | **2020–2025** | **FY20–FY25** |
| WUE | 2021–2025 | none | FY24–FY25 |
| At-risk / stress share | 2025 | 2024–2025 | FY25 |

Implications:
- **Trend analysis is possible for Google and Microsoft volumes** (six years each),
  but **not cross-provider**: AWS reports volume for 2025 only, so a like-for-like
  multi-year comparison across all three is not yet supported.
- **Two report editions overlap for Google.** The 2025 report (2024 data year) and
  the 2026 report (2025 data year) both carry some of the same calendar years, and a
  figure can be **restated** between editions (e.g. 2024 freshwater replenishment is
  64% in the 2025 report and 63% in the 2026 report; 2024 freshwater consumption
  7,210 → 7,240 million US gal). The combined tables already resolve this by
  keeping the latest edition's value per fact (see "How duplicates and restatements
  are handled"); the superseded values are recorded in `restatements.csv`.
- **Calendar vs fiscal year.** Google's years are calendar; Microsoft's are fiscal
  (FY25 ≈ mid-2024 to mid-2025), so even matching "2025" labels are not the same period.

**Rule of thumb:** for **cross-provider comparison**, use the **latest-report snapshot**
(AWS 2025, Google 2025, Microsoft FY25 — the matrix above). Reserve the **multi-year
series** (Google 2020–2025, Microsoft FY20–FY25) for **single-provider trends**, since
AWS is 2025-only and the two Google editions overlap.

### Reporting evolution across editions — Google as a worked example

When more than one annual edition is extracted for a provider, you can track how its
reporting *evolves* year over year. Google is used here as an example because two of its
editions are currently extracted (2025 report = 2024 data; 2026 report = 2025 data); the
same comparison applies to any provider once multiple editions are available. Comparing
the two Google editions (structure is additive — nothing was dropped):

- **New AI metric.** The 2026 edition adds a **per-prompt water figure** for Gemini
  (median 0.26 mL/prompt) — absent from the 2025 edition. First workload-level AI water
  disclosure.
- **New forward-looking target.** The 2026 edition makes the **120% replenishment
  ambition (by 2030)** explicit as a reported item; the 2025 edition reported progress
  only.
- **More site-level disclosure.** Per-location data-centre reporting grew from **37 to
  41 sites** (added Mesa AZ, New Haven IN, Red Oak TX, Winschoten NL).
- **Observation count** rose 147 → 162, all additive.
- **Restatements.** Two 2024 figures were revised between editions and are logged in
  [`restatements.csv`](restatements.csv): freshwater replenishment **64% → 63%** and
  freshwater consumption **7,210 → 7,240** million US gal. The combined tables keep the
  2026 (latest) values.

Overall the trend is toward **more disclosure** (a new AI metric, more sites, explicit
targets) on a stable structure — a good signal for a data resource that depends on
provider transparency. It also shows why versioning and restatement-tracking matter:
even a stable report restates prior-year numbers.

### The six dimensions that must match before you compare

1. **Water flow.** Withdrawal ≠ consumption ≠ discharge. AWS reports
   **withdrawal only** (so no `SWI-C` from AWS); Google and Microsoft report all
   three. Never compare an AWS withdrawal-WUE to a Microsoft WUE without noting
   the flow difference.
2. **Energy denominator (WUE).** AWS WUE is per **IT-load energy** and framed on a
   **withdrawal** basis; Microsoft WUE is per **IT-equipment energy** on its own
   provider-defined basis. So AWS 0.12 vs Microsoft 0.27 is *not* a like-for-like
   efficiency gap — the numerator (which water) and denominator (which energy)
   differ.
3. **Scope / product.** None of these is a cloud-service factor. Google's totals
   are **corporate (data centres + offices), not GCP**; Microsoft's are
   **owned-datacentre fleet, not Azure**; AWS is a **global data-centre fleet
   average**. The Gemini per-prompt figure is one Google product, not generic GCP —
   and it is a **single global median** (blended fleet-average WUE, Gemini text prompts
   only), so it cannot be localised or combined with Google's per-location volume table.
4. **Geographic resolution.** Google gives **per-site** and global (all three flows);
   Microsoft gives **global** and **broad region** (Americas/APAC/EMEA) for all three
   flows, plus **site-level for withdrawal only** (29 datacentres, Section 2, unassured —
   no per-site consumption or discharge); AWS gives **global fleet only**. Compare
   site-to-site or global-to-global, never site-to-fleet.
5. **Reporting period basis.** Google reports **calendar years**; Microsoft reports
   **fiscal years** (FY25 ≠ CY2025); AWS mixes both. Match the `period` column.
6. **Units and assurance.** Reported units differ (US gal / ML / million m³); use
   the normalized litres columns. Assurance also differs (e.g. Google 2025 metrics
   limited-assured; Microsoft Section 1 assured but Section 2 not) — see `caveat`.

### What you *can* safely do

- Compare **the same provider across years** (e.g. Google withdrawal 2020→2025).
  The combined tables are already de-duplicated to one value per fact (latest
  edition), so a year that appeared in two editions is not double-counted.
- Compare **withdrawal volumes at the same resolution and year** across providers,
  as an order-of-magnitude check — while stating the scope caveat.
- Use each provider's own **flow identity** (`consumption = withdrawal − discharge`)
  for internal consistency checks.

### What you should *not* do

- Rank providers by a single WUE or volume number as if it were an efficiency
  league table — the boundaries differ too much.
- Treat replenishment as if it cancels operational water — it is an **offset**,
  reported in different units and methods, and never netted against withdrawal or
  consumption.
- Apply a corporate or fleet figure to a specific cloud workload without the scope,
  geography, year, flow, and energy denominator all matching (see each
  `worked_example.md`).

## Regenerate

```bash
python derive_parameters.py
```

## Important

These are **derived** artifacts — never hand-edit them. The source of truth is
the JSON under each `<company>/json/`. Comparing WUE across providers requires
care: values differ by `water_flow` (withdrawal vs consumption vs
provider-reported), scope, and reporting boundary. Always read the `caveat` and
`water_flow` columns before comparing.
