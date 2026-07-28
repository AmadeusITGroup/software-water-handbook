# Worked Example — AWS: Direct Water for a Cloud Workload

Estimating the **direct operational water (`D`)** of a workload on AWS, in
**litres** (physical water). All values are in the **metric system**; where a
source reports US gallons, the metric value is primary and the original is shown
in parentheses.

> **Scope of this example.** This is Layer 1 (direct water) and stays in
> **litres**. Turning litres into a scarcity-weighted *impact* — using whichever
> impact framework applies — belongs to the **impact layer**
> (`sources/impact_models/`), not here. See the note at the end on what AWS itself
> reports.

Parameter values come from this folder's `csv/` tables, derived from `json/`:
`csv/wue.csv`, `csv/water_volumes.csv`, `csv/water_shares.csv`,
`csv/replenishment_and_progress.csv`.

---

## First: what "water" means here (read before calculating)

| Dimension | AWS WUE (`wue.csv`) | Fleet withdrawal (`water_volumes.csv`) |
|-----------|---------------------|-----------------------------------------|
| **Flow** | withdrawal-based intensity (L per IT kWh) | withdrawal |
| **End uses** | cooling (evaporative on hot days) | cooling / data-centre operations |
| **Facility scope** | **global AWS data-centre fleet** average | global AWS data-centre footprint |
| **Resolution** | global fleet only | global total; plus a **water-stress-level share** breakdown (WRI Aqueduct) but no per-region volumes |
| **Consumption / discharge** | **not reported** by AWS | **not reported** |
| **Freshwater status / sources** | not disaggregated | not disaggregated |

Key facts:
- AWS reports **withdrawal only** — no consumption and no discharge. So the
  `consumption = withdrawal − discharge` identity cannot be evaluated, and
  **SWI-C cannot be derived** (see below).
- AWS publishes **global fleet** withdrawal volumes only. It does report the
  **share** of withdrawal by WRI Aqueduct water-stress level (48% low, 22%
  high/extremely high in 2025), but not per-region volumes — so you know *how much
  is stressed*, not *where* in volume terms.

---

## Scenario A — Single workload via WUE

Method 2 from [`../how_to_calculate_swi.md`](../how_to_calculate_swi.md):
`D = workload_IT_kWh x WUE`.

- Workload on AWS, period **2025**.
- Workload IT energy: **50,000 kWh** (from your own tooling — not provided here).

From `csv/wue.csv`:

| provider | region | period | wue_l_per_kwh | water_flow | source_report_id |
|----------|--------|--------|---------------|------------|------------------|
| Amazon Web Services | global fleet | 2025 | 0.12 | withdrawal | aws_water_efficiency_page_2025 |

```
D_W = 50,000 kWh x 0.12 L/kWh = 6,000 L        -> feeds SWI-W
```

Trend for context (all withdrawal-based, global fleet, from `csv/wue.csv`):
0.25 (2021) → 0.19 (2022) → 0.18 (2023) → 0.15 (2024) → 0.12 (2025) L/kWh. AWS cites an
**industry average of 0.84 L/kWh** as a benchmark (not AWS's own value).

## Scenario B — Can the fleet withdrawal total be allocated?

AWS reports a **global fleet withdrawal** for 2025 (`csv/water_volumes.csv`):

| water_flow | location | period | value | metric value |
|------------|----------|--------|-------|--------------|
| withdrawal | AWS global leased, owned, and shared data centres | 2025 | 9.4 billion L | **9,400 ML (9.4 billion L)** |

(Amazon reports this figure directly in litres, so no conversion is needed.)

To attribute this total to a workload by energy share:

```
D_W = fleet_withdrawal x (workload_IT_kWh / total_AWS_IT_kWh)
    = 9.4e9 L x (workload_IT_kWh / total_AWS_IT_kWh)
```

*Blocked:* AWS does not publish **total AWS data-centre IT energy** (the
denominator), so the 9.4-billion-litre total cannot be turned into a
per-workload share. The **WUE method (Scenario A) is the practical path** — it is
the fleet total expressed per kWh, which sidesteps the missing denominator.

Sanity check: the Scenario A result (6,000 L) is a ~6.4e-7 share of the 9.4
billion L fleet total — i.e. this workload is a tiny slice of global AWS
withdrawal, as expected.

## Why SWI-C and region-wise are not available (data-driven)

- **SWI-C (consumption):** AWS publishes withdrawal-based WUE and **no consumption
  or discharge**, so consumption cannot be derived. Only **SWI-W** is supported.
  (Contrast: Microsoft reports withdrawal, discharge, and consumption, enabling
  both — see [`../microsoft/worked_example.md`](../microsoft/worked_example.md).)
- **Region-wise:** AWS reports withdrawal **volumes** at the global-fleet level
  only. It does publish the **share** of withdrawal by WRI Aqueduct water-stress
  class (2025: 48% low, 22% high/extremely high; the ~30% medium is not stated),
  so you can bound how much of the fleet withdrawal sits in stressed basins
  (≈ 0.22 × 9.4 bn L ≈ 2.07 bn L in high/extremely-high stress), but not attribute
  it to specific regions or workloads.

## Context metrics (not operational water)

From `csv/replenishment_and_progress.csv` — **replenishment/offset metrics, not
withdrawal or consumption; never net them against `D`:**
- Water-positive progress: **75%** toward the 2030 goal; returned 3 L for every 4 L used in 2025.
- Announced projects expected to return **> 21,955 ML/yr (5.8 billion US gal/yr)**; projects under way targeting **> 71,923 ML/yr (19 billion US gal/yr) by 2030**.
- **130 data centres** using reclaimed/recycled water.

## Impact framework AWS reports (context, not a calculation here)

Amazon uses the **WRI Aqueduct Water Risk Atlas** to assess data-centre water
risk, specifically on WRI's **2030 business-as-usual baseline scenario** (a
future-projected, source-water-stress basis, covering leased and owned data
centres). On that basis it reports the share of 2025 data-centre withdrawal by
stress level: **48% low**, **22% high or extremely high**.

Note this is the **same tool** Microsoft uses (WRI Aqueduct) but a **different
scenario/threshold** — Microsoft reports on the *current* baseline water-stress
classification, not the 2030 projection — so the two providers' stress shares are
not directly comparable. Google, by contrast, uses its own proprietary Data
Center Water Risk Framework for its data-centre share.

Aqueduct is a **risk-screening** tool (a stress *category*), not a
characterization factor. Turning litres into a scarcity-weighted *impact* still
belongs to the **impact layer** (`sources/impact_models/`), which chooses the
impact framework independently of the provider's own risk screen.

## What you can / cannot say

- **Can:** "Using the AWS fleet-average withdrawal WUE (0.12 L/kWh, 2025), the
  estimated direct water withdrawal for this 50,000 kWh workload is ~6,000 L
  (SWI-W)."
- **Cannot:** claim it equals consumption (AWS reports none), reflects a specific
  site or region (global fleet only), or is comparable to Microsoft/Google figures
  (different boundaries — withdrawal vs "water use", global vs regional).
