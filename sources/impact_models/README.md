# Layer 4 — Impact Models (Scarcity & Risk Conversion)

> **Status:** curated source references and methodology. Structured per-source
> extractions and worked examples (as in [`direct_water/`](../direct_water/)) are
> planned, not yet available. Contributions welcome — see
> [CONTRIBUTING](../../CONTRIBUTING.md).

## What this covers

Converting physical water volumes into meaningful impact assessments using location-specific characterization factors or risk scores.

Without this layer, a litre in Norway and a litre in Egypt look identical. With it, 100L in Egypt becomes 7,148 L-eq (world-equivalent litres), reflecting 96× more scarcity impact than the same volume in Norway.

## AWARE (Primary for SWI)

### What it is

AWARE (Available WAter REmaining) is the consensus characterization model for water scarcity footprints in Life Cycle Assessment (LCA). It is recommended by the UN Environment Programme's Life Cycle Initiative and is consistent with ISO 14046.

### What it measures

The inverse of available freshwater remaining per unit area after human and ecosystem demand. The characterization factor (CF) answers:

> "What is the potential to deprive another freshwater user (human or ecosystem) by consuming water in this area?"

### Key properties

- **Range:** 0.1 to 100
- **Unit:** m³ world-equivalent / m³ consumed
- **CF = 1:** remaining water per area equals world average
- **CF = 10:** ten times less available water per area than world average
- **Usage:** multiply by water consumption volume → impact in L-eq or m³ world-eq

### Available resolutions

| Resolution | Coverage | File |
|-----------|----------|------|
| Native watershed | Global | `AWARE20_Native_CFs_geospatial.gpkg` |
| Sub-national (admin-1) | 3,652 regions | `AWARE20_Subnational_Resolution.xlsx` |
| Country/region | 558 entries | `AWARE20_Countries_and_Regions.xlsx` |

### Temporal resolution

Monthly CFs (Jan–Dec) plus Annual aggregate. Monthly factors should be used when monthly water consumption is known.

### Sector variants

- `CFs_nonagri` — for non-agricultural use (**use this for data centers**)
- `CFs_agri` — for agricultural/irrigation use
- `CFs_unspecified` — default when sector is unknown

### Critical scope limitation

**AWARE is designed for water consumption only.** It is not validated for withdrawal. See [consumption_vs_withdrawal.md](../../methodology/consumption_vs_withdrawal.md) for details.

### Sources

- Dataset: https://zenodo.org/records/15133241
- Method description: https://wulca-waterlca.org/what-is-aware/
- Boulay, A.-M., et al. (2018). *Int J Life Cycle Assess*, 23(2), 368–378. https://doi.org/10.1007/s11367-017-1333-8
- Seitfudem, G., et al. (2025). *Journal of Industrial Ecology*, 1–17. https://doi.org/10.1111/jiec.70023
- Underlying hydrology: Müller Schmied, H., et al. (2024). WaterGAP v2.2e. *Geoscientific Model Development*, 17(23), 8817–8852. https://doi.org/10.5194/gmd-17-8817-2024

---

## Aqueduct (Diagnostic Context for SWI)

### What it is

Aqueduct is WRI's global water-risk framework. It is widely used for corporate risk screening and decision-making. It is **not** an LCA characterization model.

### What it measures

Multiple water risk indicators at sub-basin level (HydroBASINS level 6):

| Indicator | Code | Definition |
|-----------|------|-----------|
| Baseline Water Stress | `bws` | Total withdrawals / available renewable supply |
| Baseline Water Depletion | `bwd` | Total consumption / available renewable supply |
| Drought Risk | `drr` | Combined drought hazard, exposure, and vulnerability |
| Seasonal Variability | `sev` | Intra-annual variation in water availability |
| Interannual Variability | `iav` | Year-to-year variation in water availability |
| Groundwater Table Decline | `gtd` | Rate of groundwater level decline (cm/year) |

All scored on a 0–5 scale with category labels (Low, Low-Medium, Medium-High, High, Extremely High).

### Key properties

- **Resolution:** Sub-basin level, with monthly variants for bws, bwd, iav
- **Temporal:** Baseline + future projections (2030, 2050, 2080)
- **Not a characterization factor:** Cannot be directly multiplied by water volumes for impact assessment

### Role in SWI

Aqueduct provides **diagnostic context** alongside the primary AWARE-weighted result. It reveals operational risk dimensions (depletion severity, groundwater sustainability, variability) that AWARE alone does not capture. Report both, interpret together.

### Sources

- Platform: https://www.wri.org/aqueduct
- Dataset: https://www.wri.org/data/aqueduct-global-maps-40-data
- Kuzma, S., et al. (2023). Aqueduct 4.0 Technical Note. https://doi.org/10.46830/writn.23.00061
- Indicator help: https://www.wri.org/aqueduct/help-center/water-risk-indicators

---

## Other LCIA Methods

| Method | Description | Link |
|--------|-------------|------|
| ReCiPe | Comprehensive LCIA method (includes water) | https://www.rivm.nl/en/life-cycle-assessment-lca/recipe |
| LCIA comparison guide | Comparing ReCiPe, EF, TRACI, CML | https://www.lcawise.com/learn/practitioner/07-lcia-method-selection |
