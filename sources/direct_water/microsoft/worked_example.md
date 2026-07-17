# Worked Example — Microsoft: Direct Water for a Cloud Workload

Estimating the **direct operational water (`D`)** of a workload on
Microsoft-owned datacentres, in **litres** (physical water).

> **Scope of this example.** This is Layer 1 (direct water) and stays in
> **litres**. Turning litres into a scarcity-weighted *impact* — using whichever
> impact framework applies (AWARE, Aqueduct, or another) — belongs to the
> **impact layer** (`sources/impact_models/`), not here. See the note at the end
> on what impact framework Microsoft itself reports.

Parameter values come from this folder's `csv/` tables, derived from `json/`:
`csv/wue.csv`, `csv/water_volumes.csv`, `csv/water_shares.csv`.

---

## First: what "water" means here (read before calculating)

A number is meaningless without its boundary. As reported by Microsoft:

| Dimension | WUE (`wue.csv`) | Volume tables (`water_volumes.csv`) |
|-----------|-----------------|--------------------------------------|
| **Flow** | "water used for cooling and humidification" per IT kWh — a *water-use* intensity, not split into withdrawal vs consumption | withdrawal (GRI 303-3), consumption (GRI 303-5), discharge (GRI 303-4), reported separately |
| **End uses** | cooling + humidification only | all operational water uses |
| **Facility scope** | Microsoft **owned datacentres** (operational 12 months) | **all corporate operations** — owned & leased offices, datacentres, and labs |
| **Sources** | not specified | third-party, surface, ground water |
| **Freshwater?** | not specified | freshwater vs other **not broken out** (Microsoft states it is currently unavailable) |

Key definitional facts:
- **Consumption = withdrawal − discharge.** Microsoft's FY25 figures satisfy this exactly: 13,266 − 5,096 = 8,170 ML.
- **WUE and the volume tables have different boundaries.** WUE is owned-datacentres + cooling/humidification; the volume totals are all corporate facilities and all uses. They are **not** the same water, so do not mix them casually (this matters for Scenario B).
- **"Water use" (WUE) is neither withdrawal nor consumption** as defined — it is a provider-reported intensity. Treating it as either without confirmation introduces error.

These boundaries are recorded in each observation's `water_boundary` (flow, end_uses,
freshwater_status) and the metric `definition_text` in `json/`.

---

## Scenario A — Single workload via WUE (fleet/region intensity)

Method 2 from [`../how_to_calculate_swi.md`](../how_to_calculate_swi.md):
`D = workload_IT_kWh x WUE`.

- Workload on Microsoft-owned datacentres in the **Americas**, period **FY25**.
- Workload IT energy: **50,000 kWh** (from your own tooling).

From `csv/wue.csv`:

| provider | region | period | wue_l_per_kwh | water_flow | source_report_id |
|----------|--------|--------|---------------|------------|------------------|
| Microsoft | Americas | FY25 | 0.34 | provider_reported_water_use | microsoft_datacenter_wue_2025 |

```
D = 50,000 kWh x 0.34 L/kWh = 17,000 L
```

`water_flow = provider_reported_water_use` — Microsoft's WUE numerator is
"water used for cooling and humidification," not split into withdrawal vs
consumption. So `D ≈ 17,000 L` is provider-reported water use, not specifically
consumption or withdrawal.

---

## Scenario B — Region-wise, reporting BOTH withdrawal and consumption

**Question:** "How much water is attributable to my software running in
Microsoft's North America operations in FY25 — as both withdrawal (SWI-W) and
consumption (SWI-C)?"

`SWI-C` and `SWI-W` are **separate metrics** and must be reported separately —
never added. Microsoft's regional volume table gives both flows, so both can be
estimated (subject to the attribution caveats below).

### What data is available

From `csv/water_volumes.csv` (Table 14, corporate, North America, FY25):

| water_flow | location | period | value (ML) | value_liters |
|------------|----------|--------|-----------|--------------|
| withdrawal | North America | FY25 | 7,366 | 7.366e9 |
| discharge | North America | FY25 | 2,747 | 2.747e9 |
| consumption | North America | FY25 | 4,619 | 4.619e9 |

Note the identity holds: **consumption = withdrawal − discharge** (7,366 − 2,747 = 4,619 ML).

### Attribute by energy share (both flows)

With an energy share `s = workload_IT_kWh_in_region / total_regional_IT_kWh`:

```
D_W = s x regional_withdrawal   = s x 7.366e9 L      -> feeds SWI-W
D_C = s x regional_consumption  = s x 4.619e9 L      -> feeds SWI-C
```

Both use the **same** energy share; only the flow volume differs. Report them as
two separate numbers.

*Blocked by the denominator:* Microsoft does not publish **total North America IT
energy**, so `s` cannot be computed from public data. This is the regional form of
the allocation problem — it blocks **both** SWI-C and SWI-W equally.

### If you only have an intensity (WUE)

`csv/wue.csv` gives Americas WUE FY25 = 0.34 L/kWh, but its flow is
`provider_reported_water_use` (cooling + humidification "water use"), which is
**neither withdrawal nor consumption**. So a WUE-based estimate:

```
water_use ≈ workload_IT_kWh_Americas x 0.34 L/kWh
```

does **not** cleanly populate either SWI-W or SWI-C. To split it you would need a
withdrawal-vs-consumption ratio; Microsoft's regional totals imply a
consumption-to-withdrawal ratio of ~0.63 (4,619 / 7,366) for North America, but
applying an all-operations ratio to a datacentre-only WUE mixes boundaries and is
only a rough approximation.

### What is missing for a defensible region-wise number

1. **Workload IT energy per region** — you must supply this (Layer 1 does not provide it).
2. **Total regional IT energy denominator** — not published; blocks the volume allocation for both flows.
3. **Boundary alignment** (see the definitions table above):
   - WUE regions (Americas/APAC/EMEA) ≠ volume regions (North America/Asia/EMEA/Latin America);
   - WUE covers **owned datacentres + cooling/humidification**, while the regional volumes cover **all corporate operations** (offices, labs, datacentres) — a WUE-based estimate is a *subset* of the regional volume, not a share of it;
   - WUE "water use" ≠ the volume table's withdrawal/consumption split.
4. **Site vs region** — site-level data (`water_volumes.csv`, 29 locations) is **withdrawal only**, so there is no per-site consumption to attribute (you could produce a site-level SWI-W but not SWI-C).

**Conclusion:** Microsoft's data lets you *define* both SWI-C and SWI-W from the
regional withdrawal/consumption pair, but a defensible per-workload figure is
blocked for both by the missing IT-energy denominator. A WUE-based estimate yields
an ambiguous "water use" that maps cleanly to neither metric without a
withdrawal/consumption split.

---

## Contrast with AWS (boundary matters)

Same 50,000 kWh workload: AWS gives ~6,000 L (withdrawal WUE 0.12), Microsoft
Americas gives ~17,000 L (water-use WUE 0.34). The gap is mostly **boundary and
scope** (withdrawal vs "water use", global vs regional), not a clean efficiency
comparison. This is why every parameter row keeps `water_flow`,
`service_applicability`, and `caveat`.

---

## Note: impact framework Microsoft reports (context, not a calculation here)

This example stays in **litres**. For completeness, Microsoft's own reports assess
water *risk/impact* using **WRI Aqueduct**, specifically the **Baseline Water
Stress (bws)** indicator, thresholded at the **"high or extremely high"** category.
They report, for FY25, that **48% of consumption** and **50% of withdrawal** occur
in such areas (see `csv/water_shares.csv` and
[`json/microsoft_environmental_data_factsheet_2026.json`](json/microsoft_environmental_data_factsheet_2026.json)).

Two things to keep straight:

- Microsoft's own water-stress classification is **Aqueduct bws (categorical)**.
  If you later apply a different impact framework, its results are **not
  interchangeable** with this Aqueduct classification.
- Converting these litres into a scarcity-weighted impact — whichever framework
  is chosen — is done in the **impact layer** (`sources/impact_models/`), not in
  this direct-water layer. This layer stays in physical litres.
