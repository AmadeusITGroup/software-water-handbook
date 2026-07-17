# Microsoft — Direct Water Sources

Structured water data extracted from Microsoft's primary reports.

## Contents

- `json/` — schema-conformant extractions (source of truth), one per report:
  - `microsoft_environmental_data_factsheet_2026.json` — Tables 8, 14, 15 (annual withdrawal/consumption/discharge, by region and source, 29 datacentre locations) + FY25 water-stress subset. **177 observations.**
  - `microsoft_environmental_sustainability_report_2026.json` — WUE, WUE reduction/target, Phoenix improvement, avoided cooling water, replenishment. **10 observations.**
  - `microsoft_datacenter_wue_2025.json` — regional WUE (Global/Americas/APAC/EMEA x FY24/FY25). **8 observations.**
- `csv/` — themed parameter tables derived from `json/` (regenerate with `python ../cross_provider/derive_parameters.py`). Together they cover all 195 observations:
  - `wue.csv` — Water Usage Effectiveness (9 rows)
  - `water_volumes.csv` — withdrawal/consumption/discharge at total, regional, by-source, and site resolution (164 rows)
  - `water_shares.csv` — water-stress and non-potable share percentages (6 rows)
  - `replenishment_and_progress.csv` — replenishment, avoided-water, WUE-reduction progress (16 rows)
- `worked_example.md` — end-to-end direct-water calculation using Microsoft data.

## Key caveats

- **Not Azure-specific.** Microsoft reports corporate/fleet water; it is not a
  cloud-service or workload factor. A fleet or regional WUE is not a site value.
- **WUE is "water use"** (cooling + humidification per IT kWh), not stated as
  withdrawal or consumption — captured as `provider_reported_water_use`.
- **Water stress via WRI Aqueduct**, using the Baseline Water Stress indicator
  ("high or extremely high" category) only — not AWARE, and not the fuller
  Aqueduct multi-metric set.
- FY20–FY24 volumes were **recalculated** and adjusted for the ABK acquisition
  (see `report.restatement` in the factsheet JSON).

## Sources

- [Microsoft 2026 Environmental Data Fact Sheet](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/2026-Environmental-Data-Fact-Sheet.pdf)
- [Microsoft 2026 Environmental Sustainability Report](https://www.microsoft.com/en-us/corporate-responsibility/sustainability/report)
- [Microsoft Datacenters — Sustainability / Efficiency (WUE)](https://datacenters.microsoft.com/sustainability/efficiency/)
