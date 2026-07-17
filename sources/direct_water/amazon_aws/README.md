# Amazon Web Services — Direct Water Sources

Structured water data extracted from Amazon/AWS primary reporting.

## Contents

- `json/` — schema-conformant extractions (source of truth):
  - `aws_sustainability_report_2025.json` — 2025 data-centre **withdrawal (9.4 billion L)**; withdrawal-based WUE (0.15 in 2024, 0.12 in 2025); **water-stress shares via WRI Aqueduct** (48% low, 22% high/extremely high, 2030 BAU scenario); water-positive progress (53% 2024 → 75% 2025); replenishment returned (9.4 billion L in 2025; >18 billion L contracted); avoided/preserved water (938 M L cooling reduced; 849 M L potable preserved). 11 observations.
  - `aws_water_efficiency_page_2025.json` — WUE (0.12 L/kWh 2025, 0.25 in 2021) vs industry average (0.84), 2025 data-centre withdrawal (~2.5 billion US gal), water-positive progress (75%), return-to-use ratio, 50+ replenishment projects (>5.8 billion US gal/yr), 130 data centres using reclaimed water. 8 observations.
  - `aws_withdrawal_trellis_2025.json` — secondary source (Trellis) corroborating the ~2.5 billion US gal withdrawal, WUE 0.12, replenishment (>5.8 and >19 billion US gal/yr by 2030). 4 observations, all flagged `secondary_source_only`.
- `csv/` — themed tables derived from `json/` (wue, water_volumes, water_shares, replenishment_and_progress). Regenerate with `python ../cross_provider/derive_parameters.py`.
- `worked_example.md` — end-to-end direct-water calculation using AWS data.

## Key caveats

- **Withdrawal-based WUE** (0.25 in 2021 → 0.15 in 2024 → 0.12 in 2025), global
  fleet average — not regional, site, or workload-attributed, and not Amazon
  corporate operations. Consumption-based impact frameworks (e.g. AWARE) should
  not be applied to a withdrawal figure without adjustment. Impact weighting is
  out of scope here (impact layer); this layer stays in litres.
- **Withdrawal only** — AWS publishes no consumption or discharge, so **SWI-C is
  not derivable** from AWS data; only SWI-W is supported.
- **Risk framework: AWS uses WRI Aqueduct.** Amazon assesses data-centre water
  stress with the **WRI Aqueduct Water Risk Atlas** on the **2030 business-as-usual
  baseline scenario** and reports the withdrawal share by stress level (48% low,
  22% high/extremely high, 2025). This is the *same tool* Microsoft uses but a
  *different scenario/threshold* (Microsoft uses the current baseline), so the two
  stress shares are not directly comparable. Aqueduct is a risk screen, not a
  characterization factor — impact weighting still belongs to the impact layer.
- **Replenishment / water-positive / avoided-water metrics are context**
  (`context_only`) — not operational water, and must not be netted against withdrawal.
- The **0.84 L/kWh** "industry average" is a benchmark AWS cites, not AWS's own value.

## Sources

- [Amazon 2025 Sustainability Report](https://sustainability.aboutamazon.com/)
- [Amazon: AWS Data Center Water Usage](https://www.aboutamazon.com/news/sustainability/amazon-data-center-water-usage)
- [Behind Amazon's Industry-Leading Water Efficiency Score (Trellis, secondary source)](https://trellis.net/article/behind-amazons-industry-leading-water-efficiency-score/)
