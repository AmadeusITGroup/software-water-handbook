# Cross-Provider Parameter Tables

Combined, computation-ready parameters aggregated across all companies, for
comparison and lookup.

## Contents

Themed parameter tables, combined across every extracted provider:

- `wue_all_providers.csv` — Water Usage Effectiveness (intensity)
- `water_volumes_all_providers.csv` — withdrawal/consumption/discharge volumes
- `water_shares_all_providers.csv` — percentage-share metrics
- `replenishment_and_progress_all_providers.csv` — replenishment / avoided / progress

Plus:

- `datapackage.json` — the canonical Frictionless data dictionary describing all
  four table schemas. Shared by these combined tables **and** the per-company
  `<company>/csv/<theme>.csv` tables, which use the same field schemas.
- `derive_parameters.py` — regenerates all parameter tables from the JSON
  extractions:
  - per company → `<company>/csv/<theme>.csv`
  - combined → `cross_provider/<theme>_all_providers.csv`

## What is comparable across providers — and what is not

These tables put three providers side by side, but **most of the headline
numbers are not directly comparable**. Before comparing any two values, check
that they agree on the six dimensions below. The `water_flow`, `caveat`,
`source_report_id`, and `period` columns exist so you can do this.

### Comparability by metric family

| Metric family | Amazon (AWS) | Google | Microsoft | Directly comparable? |
|---------------|:---:|:---:|:---:|---|
| **WUE (L/kWh)** | ✅ 0.12–0.25 | ❌ none published | ✅ 0.03–0.38 | **No** — different water flow and energy denominator (see below) |
| **Per-unit (per prompt)** | ❌ | ✅ 0.26 mL/prompt (Gemini) | ❌ | **No** — only Google; a single **global median** (blended fleet-average), Gemini text prompts only, not per-location and not generic cloud |
| **Volumes: withdrawal** | ✅ (fleet only) | ✅ (global + per site) | ✅ (global + regional) | Only at matching resolution + year |
| **Volumes: consumption** | ❌ not reported | ✅ | ✅ | AWS cannot be compared here at all |
| **Volumes: discharge** | ❌ not reported | ✅ | ✅ | AWS cannot be compared here at all |
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
4. **Geographic resolution.** Google gives **per-site** and global; Microsoft gives
   **broad region** (Americas/APAC/EMEA) and some site-level (Section 2, unassured)
   and global; AWS gives **global fleet only**. Compare site-to-site or global-to-
   global, never site-to-fleet.
5. **Reporting period basis.** Google reports **calendar years**; Microsoft reports
   **fiscal years** (FY25 ≠ CY2025); AWS mixes both. Match the `period` column.
6. **Units and assurance.** Reported units differ (US gal / ML / million m³); use
   the normalized litres columns. Assurance also differs (e.g. Google 2025 metrics
   limited-assured; Microsoft Section 1 assured but Section 2 not) — see `caveat`.

### What you *can* safely do

- Compare **the same provider across years** (e.g. Google withdrawal 2020→2025),
  filtering on one `source_report_id` to avoid double-counting a year that appears
  in two report editions.
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
