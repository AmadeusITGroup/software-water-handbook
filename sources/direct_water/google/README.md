# Google (Alphabet) — Direct Water Sources

Structured water data extracted from Google's primary reporting and corroborating
secondary sources.

## Contents

- `json/` — schema-conformant extractions (source of truth):
  - `google_environmental_report_2025.json` — **Google 2025 Environmental Report (2024 data year)**: aggregate withdrawal/discharge/consumption 2020–2024 (2024: 11,011 / 2,876 / 8,135 million US gal); 2024 data-centre vs office split; per-location 2024 withdrawal/discharge/consumption (~37 sites, e.g. The Dalles 461.1 / 99.7 / 361.4 million US gal); freshwater-at-risk shares (72/14/14%); replenishment series 2022–2024 (64% replenished in 2024). 147 observations. Predates the Gemini per-prompt figure.
  - `google_environmental_report_2026.json` — full water tables: aggregate **withdrawal / discharge / consumption 2021–2025** (2025: 14,689 / 3,820 / 10,869 million US gal ≈ 55,600 / 14,460 / 41,140 ML); 2025 **data-centre vs office split**; **per-location 2025** withdrawal/discharge/consumption (~40 sites, e.g. The Dalles 654.3 / 185.3 / 469.0 million US gal); freshwater-withdrawal-at-risk shares (72/15/13% low/med/high); **Gemini Apps median text prompt 0.26 mL**; freshwater replenishment 7.7 billion US gal (78% of freshwater consumption, 97 watersheds), 120% ambition and >19.7 billion US gal capacity target by 2030. 162 observations.
  - `google_operations_water_gwpc_2024.json` — secondary: 2024 direct-operations consumption ~8.1 billion US gal. 1 observation.
  - `google_the_dalles_records.json` — secondary (Latitude Media): litigation-disclosed The Dalles municipal records (~550 million US gal, ~40% of city water). 2 observations.
- `csv/` — themed tables derived from `json/` (per_unit_water, water_volumes, water_shares, replenishment_and_progress). Regenerate with `python ../cross_provider/derive_parameters.py`.
- `worked_example.md` — end-to-end direct-water calculation using Google data.

## Key caveats

- **All three flows reported.** Google reports **withdrawal, discharge, and
  consumption** (consumption = withdrawal − discharge), at aggregate (2021–2025),
  as a data-centre/office split, and **per location**. Both **SWI-C** and
  **SWI-W** are therefore derivable. There is still **no public per-kWh WUE**, so
  there is no `wue.csv`; the workload-usable intensity is the **per-prompt** figure.
- **Not GCP-attributed.** Data-centre figures serve multiple Google products; the
  totals are corporate (data centres + offices), not a GCP or workload factor.
  The Gemini per-prompt figure is a specific Google service, not generic GCP.
- **The Gemini 0.26 mL/prompt is a single global median, not per-location.** It is
  a blended fleet-average (energy per prompt × Google's 2024 average fleetwide WUE),
  covers **Gemini Apps text prompts only** (not images/video), and **cannot be
  localised to a watershed or combined with the per-location volume table** — the two
  have different bases (a service median vs site totals).
- **Two The Dalles figures differ by basis** — 469 million US gal (Google's 2025
  *consumption*; withdrawal 654.3, discharge 185.3) vs ~550 million US gal
  (municipal public records, a *withdrawal* basis); both retained with their sources.
- **Impact framework:** for **data centres**, Google uses its own **Water Risk
  Framework** (scarcity + depletion, low/medium/high) — not a public index. For
  **offices** it uses **WRI Aqueduct Water Risk Atlas + WWF Water Risk Filter**.

## Sources

- [Google 2026 Environmental Report](https://sustainability.google/reports/google-2026-environmental-report/) (2025 data)
- [Google 2025 Environmental Report](https://sustainability.google/reports/google-2025-environmental-report/) (2024 data)
- [Google Direct Operations Water — GWPC / Eric Olsen (secondary)](https://www.gwpc.org/wp-content/uploads/2024/10/Eric-Olsen.pdf)
- [Data center water use can be a 'black box' — Latitude Media (secondary)](https://www.latitudemedia.com/news/data-center-water-use-black-box-google-trying-to-change/)

## Not extracted

- The `datacenters.google/water` page is largely qualitative and duplicative of
  the environmental report (same replenishment goal and Water Risk Framework);
  not separately extracted to avoid duplicate observations.
- The Google Cloud carbon-footprint methodology is an **energy/carbon** tool
  (indirect layer), out of scope for direct water.
