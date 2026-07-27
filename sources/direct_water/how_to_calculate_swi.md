# How to Calculate Software-Attributed Direct Water (D)

This guide shows how to estimate the **direct operational water** component (`D`)
of the [Software Water Intensity (SWI)](https://greensoftware.foundation/standards/swi/)
of a software workload, using the parameters distilled from the source
extractions in this repository.

It covers Layer 1 (direct data-centre water) only. Indirect electricity water
(`I`) and embodied water (`E`) are separate layers.

## The three data layers

```
JSON extractions            →   Parameter tables                  →   This guide
(<company>/json/*.json)         (<company>/csv/*.csv,                  (recipes + caveats)
 what was reported,              cross_provider/wue_all_providers.csv)  how to compute your number
 with full provenance            computation-ready inputs
```

Never plug a number into a calculation without checking its **unit**, its
**water_flow** (consumption vs withdrawal), and its **caveat**. Every parameter
row links back to its authoritative JSON via `source_report_id`.

## Step 1 — Choose your attribution method

Site-level water ÷ workload share = software-attributed water. Pick the best
method your data supports:

| Method | Formula | When to use |
|--------|---------|-------------|
| **1. Provider-attributed** | `D = provider_allocated_water` | The provider reports water for your specific deployment (rare; e.g. Equinix customer water reports). Best. |
| **2. WUE x workload energy** | `D = workload_IT_kWh x WUE` | You know your workload's IT energy and a relevant WUE. Most common. |
| **3. Site water x workload share** | `D = site_water x (workload_IT_kWh / total_site_IT_kWh)` | You have site totals and a credible energy share. Rarely feasible (total site IT kWh seldom public). |

Most practitioners use **Method 2**.

## Step 2 — Get your workload IT energy

`workload_IT_kWh` for the reporting period. Sources: provider billing/energy
tools, or estimators such as Cloud Carbon Footprint. This is your responsibility
to obtain; this repository does not provide workload energy.

## Step 3 — Pick a WUE (from `<company>/csv/wue.csv` or `cross_provider/wue_all_providers.csv`)

Choose the row whose `provider`, `service_applicability`, `region`, and `period`
best match your workload. Then check:

- **What water is included** — before anything else, confirm the boundary: which
  flow, which end-uses (e.g. cooling + humidification only, or all operations),
  which facilities (owned datacentres vs all corporate operations), and whether
  it is freshwater-only. Providers define "water" differently; two values are
  comparable only if these match. The boundary is in each observation's
  `water_boundary` and metric `definition_text` in `<company>/json/`.
- **`water_flow`** — `consumption`, `withdrawal`, or `provider_reported_water_use`.
  This determines whether you are computing `D_C` (consumption) or `D_W`
  (withdrawal). Report them separately (SWI-C vs SWI-W); do not add them.
- **`caveat`** — e.g. "Not Azure-specific"; a fleet average is not a site value.
- **`denominator`** — confirm it matches your `workload_IT_kWh` basis (IT-equipment energy).

Compute:

```
D = workload_IT_kWh x wue_l_per_kwh        # litres
```

## Beyond this guide: stress-weighting happens in Layer 4

This guide covers **Layer 1** and stops at **physical litres** (`D`) — that is the
whole scope of the direct-water volume calculation. Converting `D` into a
scarcity-weighted *impact* is a **separate layer of this repository — Layer 4,
[`impact_models`](../impact_models/)** — not a step of this Layer-1 guide.

Layer 4 stays **framework-neutral**: it curates and compares the candidate impact
frameworks — AWARE, WRI Aqueduct, and others, which are **not interchangeable** — and
links to their datasets, rather than prescribing a single one. See
[`methodology/`](../../methodology/) for how the frameworks differ and conflict.

Two cautions carry over regardless of framework:
- **Flow must match the framework.** Some frameworks (e.g. AWARE) are defined for
  consumption; do not apply them to a withdrawal-based `D` without an adjustment.
  Keep `D_C` and `D_W` separate.
- **Spatial resolution matters.** Use the finest location you can justify;
  country averages hide large sub-national variation.

## Worked examples

Each company folder has a `worked_example.md` showing an end-to-end calculation
with that provider's data, e.g. [`amazon_aws/worked_example.md`](amazon_aws/worked_example.md)
and [`microsoft/worked_example.md`](microsoft/worked_example.md).

## What this guide does not do

- It does not estimate your workload energy.
- It does not combine consumption and withdrawal into one number.
- It does not claim a fleet/corporate WUE is workload- or site-accurate; it
  gives you the value plus the caveats so you can judge applicability.

## Parameters

- Per company: `<company>/csv/wue.csv` — that provider's WUE values
- Combined: [`cross_provider/wue_all_providers.csv`](cross_provider/wue_all_providers.csv) — all providers in one table
- Data dictionary: [`cross_provider/datapackage.json`](cross_provider/datapackage.json) — units, field definitions, sources (shared by all WUE tables)

Regenerate all parameter tables from the JSON extractions with
`python cross_provider/derive_parameters.py`.
