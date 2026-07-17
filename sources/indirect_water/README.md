# Layer 2 — Indirect Water Sources (Electricity Generation)

> **Status:** curated source references and methodology. Structured per-source
> extractions and worked examples (as in [`direct_water/`](../direct_water/)) are
> planned, not yet available. Contributions welcome — see
> [CONTRIBUTING](../../CONTRIBUTING.md).

## What this covers

Water consumed or withdrawn to generate the electricity that powers data centers. Often the **dominant component** (>80% of total water footprint in many scenarios), because thermal power plants use large volumes of water for cooling.

## Why it's hard

Unlike direct water (one data center, one location), electricity comes from a grid with many generating plants across different watersheds. Computing indirect water requires:
1. Knowing which plants supply the grid region
2. Each plant's water intensity (depends on fuel type, cooling technology)
3. Each plant's local water stress factor

No one currently publishes this as a pre-calculated dataset.

## Data Sources

### Electricity Water Intensity Tools

| Source | Coverage | Link |
|--------|----------|------|
| Berkeley Lab Water IMPACT Tool | U.S. electricity water intensity | https://industrialapplications.lbl.gov/water-impact-tool |

### U.S. Plant-Level Data

| Source | What it provides | Link |
|--------|-----------------|------|
| EPA eGRID 2023 | U.S. generation, emissions, grid-region assignments | https://www.epa.gov/egrid |
| EIA-923 (2024) | Plant-level generation, fuel, cooling-water schedules (Schedule 8) | https://www.eia.gov/electricity/data/eia923/ |
| EIA-860 (2024) | Plant/generator characteristics, cooling-system equipment | https://www.eia.gov/electricity/data/eia860/ |

### European Data

| Source | What it provides | Link |
|--------|-----------------|------|
| ENTSO-E Transparency Platform | European generation data by plant/fuel type | https://transparency.entsoe.eu/ |

### LCI Databases (lifecycle water intensity for energy processes)

| Source | Description | Link |
|--------|-------------|------|
| ecoinvent | Comprehensive LCI database including energy processes | https://ecoinvent.org/database/ |
| GaBi (Sphera) | LCA database with energy and materials | https://fslci.org/databases/gabi-lca-databases/ |

## Aggregation Methodology

The SWI specification defines the grid-level stress-adjusted water intensity as:

```
I_grid_stress = Σ(E_i × WI_i × S_i) / Σ(E_i)
```

Where for each generating plant `i`:
- `E_i` = electricity generation (kWh)
- `WI_i` = water consumption intensity (L/kWh)
- `S_i` = AWARE characterization factor at the plant's watershed

### Typical water intensity by generation type

| Technology | Withdrawal (L/kWh) | Consumption (L/kWh) |
|------------|--------------------|--------------------|
| Coal (tower cooling) | 2–4 | 1.5–3 |
| Natural gas (combined cycle) | 0.5–1.5 | 0.3–1 |
| Nuclear (tower cooling) | 3–5 | 2–3 |
| Solar PV | ~0 | ~0 |
| Wind | ~0 | ~0 |
| Hydroelectric | Varies widely | Varies widely (evaporation) |

*Values are approximate; actual intensity depends on cooling system, climate, and plant efficiency.*

## Practical approach

For a first-pass estimate without building the full plant-level pipeline:

```
I = workload_electricity_kWh × regional_grid_water_intensity (L/kWh)
```

Regional grid water intensity can be approximated from Berkeley Lab's IMPACT Tool or from literature values for the grid's generation mix.

## References

- Macknick, J., et al. (2012). Operational water consumption and withdrawal factors for electricity generating technologies. *Environmental Research Letters*, 7(4). https://doi.org/10.1088/1748-9326/7/4/045802
