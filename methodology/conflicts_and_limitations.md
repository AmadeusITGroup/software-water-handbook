# Known Conflicts and Limitations

## 1. AWARE vs Aqueduct Ranking Conflict

### The problem

AWARE and Aqueduct can produce **contradictory rankings** for locations with similar extreme stress levels.

> **Note on methodology:** No published study has systematically compared AWARE and Aqueduct rankings for identical locations. The conflicts documented below are directly observable by comparing the two published datasets (AWARE 2.0 from Zenodo, Aqueduct 4.0 from WRI). The root cause analysis represents plausible explanations derived from the published methodology descriptions of each framework (Boulay et al. 2018; Kuzma et al. 2023), not independently verified causal claims.

### Demonstration (D = 100L, equal for all)

| Metric | Norway | Egypt / Al Qahirah | Dubai (UAE) |
|--------|--------|-------------------|-------------|
| AWARE factor (subnational) | 0.744 | 71.5 | 63.7 |
| AWARE-weighted D (L-eq) | 74 | **7,148** | 6,370 |
| Aqueduct bws | 0.07 (Low) | 5.0 (Extremely High) | 5.0 (Extremely High) |
| Aqueduct bwd | 0.08 (Low) | 3.6 (Medium-High) | **5.0 (Extremely High)** |
| Aqueduct gtd | N/A | 2.2 (Medium-High) | **2.5 (Medium-High)** |

**AWARE says:** Egypt has 12% higher impact per litre than Dubai.
**Aqueduct says:** Dubai is worse on depletion (bwd) and groundwater decline (gtd).

### Notable cases where the frameworks diverge

The divergence is observable by directly comparing published AWARE CFs (Seitfudem et al. 2025, Zenodo) against Aqueduct 4.0 baseline scores (Kuzma et al. 2023, WRI) for the same administrative regions:

| Location | AWARE CF (nonagri) | Aqueduct bws | Aqueduct bwd | Conflict type |
|----------|-------------|-------------|-------------|--------------|
| Bahrain | 0.56 | 5.0 | 5.0 | Aqueduct extreme, AWARE benign |
| Arizona, USA | 99.5 | 3.6 | 3.4 | AWARE near-max, Aqueduct only "High" |
| Uganda (multiple regions) | 75.4 | 0.0 | 0.003 | AWARE severe, Aqueduct zero stress |
| Virginia, USA | 1.6 | 2.3 | 1.0 | Aqueduct more concerned |
| California, USA | 34.4 | 3.2 | 2.8 | Same direction, different magnitude |

*Values sourced from: AWARE20_Subnational_Resolution.xlsx (Zenodo DOI 10.5281/zenodo.15133241) and Aqueduct40_baseline_annual CSV (WRI Aqueduct 4.0 data download).*

### Root cause

The frameworks measure **related but non-equivalent quantities**:

| Aspect | AWARE | Aqueduct bws | Aqueduct bwd |
|--------|-------|-------------|-------------|
| What it measures | Remaining freshwater per area after demand | Withdrawal / supply ratio | Consumption / supply ratio |
| Normalisation | To world average | Absolute ratio → 0–5 scale | Absolute ratio → 0–5 scale |
| Spatial unit | Watershed, aggregated via consumption-weighted averaging | Sub-basin (HydroBASINS level 6) | Sub-basin |
| Hydrological model | WaterGAP 2.2e | PCR-GLOBWB 2 / WaterGAP | PCR-GLOBWB 2 / WaterGAP |

Contributing factors (inferred from published methodology descriptions, not independently verified):
1. **Different denominators** — AWARE divides by area (Boulay et al. 2018, Section 2.1); Aqueduct divides by supply volume (Kuzma et al. 2023, Section 3.1)
2. **Aggregation method** — AWARE uses consumption-weighted averaging across watersheds (Boulay et al. 2018); Aqueduct reports at sub-basin level
3. **Non-conventional sources** — how desalination and inter-basin transfers are treated as "availability" may differ between the WaterGAP model (used by AWARE) and the supply estimates in Aqueduct (not explicitly documented in either methodology for these specific cases)
4. **Temporal reference** — AWARE 2.0 uses WaterGAP 2.2e with 2019 demand reference (Müller Schmied et al. 2024); Aqueduct 4.0 uses a different baseline period

### Implication

Neither framework is wrong. They answer different questions. Report both for transparency.

---

## 2. Sub-national Resolution Gap

Country-level AWARE factors hide within-country variation:

| Country | Min CF | Max CF | Spread |
|---------|--------|--------|--------|
| Norway | 0.30 (Hordaland) | 2.52 (Finnmark) | 8.5× |
| Egypt | 63.7 (Al Fayyum) | 96.0 (Janub Sina') | 1.5× |
| UAE | 45.7 (Fujairah) | 63.7 (Dubai) | 1.4× |

**Always use sub-national CFs when the data center location is known.** Country-level is a fallback for unknown or mixed locations.

---

## 3. Drought Risk Data Gap

Aqueduct's drought risk (`drr`) is unavailable (NaN) for many arid regions including Egypt and UAE. This is a significant gap since drought is arguably most relevant in water-scarce locations.

---

## 4. bws Ceiling Effect

Both Egypt and Dubai score the maximum bws (5.0 / Extremely High >80%). Aqueduct cannot differentiate their stress levels on this metric, even though their underlying hydrological conditions differ. bwd and gtd provide additional discrimination.

---

## 5. The Allocation Problem

Public provider reports give site-level or fleet-level water totals. Moving to software-level requires a workload energy denominator that is not publicly disclosed by most providers. This is the primary practical barrier to per-workload water impact reporting.

---

## 6. Conceptual and Structural Conflicts

These are broader limitations that apply across all water impact frameworks, well-established in LCA and water footprinting literature.

### 6.1 Scarcity vs Risk vs Damage

Different frameworks define "water impact" differently:

| Concept | What it measures | Example framework |
|---------|-----------------|-------------------|
| **Scarcity** | Reduction in available water relative to demand | AWARE |
| **Risk** | Competition for water, likelihood of shortages | Aqueduct |
| **Damage** | Actual harm to ecosystems or human health | ReCiPe endpoint, LANCA |

These are not equivalent. A region can be high-scarcity but low-damage (if users adapt), or high-risk but low-scarcity (if risk comes from variability rather than average shortage). Comparing results across these categories is not meaningful.

*Reference: ISO 14046:2014, Section 5.3 — distinguishes midpoint and endpoint impact categories for water footprinting.*

### 6.2 Midpoint vs Endpoint

AWARE operates at **midpoint** level: it quantifies scarcity potential (a proxy for harm) but not actual damage to human health or ecosystems. Endpoint methods (e.g. ReCiPe endpoint, Pfister et al. 2009) attempt to model actual consequences but require more assumptions and carry greater uncertainty.

Most software water impact applications (including SWI) use midpoint methods because they are more robust, more widely accepted, and require fewer contested value judgments.

*Reference: Boulay, A.-M., et al. (2015). Consensus building on the development of a stress-based indicator for LCA-based impact assessment of water consumption: outcome of the expert workshops. Int J Life Cycle Assess, 20, 927–933. https://doi.org/10.1007/s11367-015-0869-8*

### 6.3 Linear Proportionality Assumption

AWARE (and most LCA characterization models) assumes **linear proportionality**: consuming 100L has exactly 10× the impact of consuming 10L at the same location. Real water systems exhibit thresholds and non-linearities — a river at 79% withdrawal may function normally while at 81% ecological collapse begins.

This is a known limitation of midpoint LCA methods. It means AWARE-weighted results should be interpreted as relative indicators, not as predictions of actual ecological outcomes.

*Reference: Boulay et al. (2018), Section 4 (Limitations): acknowledges that the method assumes marginal changes and may not capture threshold effects.*

### 6.4 Water Quality Is Excluded

Most water scarcity frameworks (AWARE, Aqueduct bws/bwd) address **water quantity** only. Water quality impacts (thermal pollution from cooling return water, chemical discharges) are a separate dimension not captured by the SWI formula or the sources in this repository.

The "grey water footprint" concept addresses pollution but uses a different methodology and is not integrated into AWARE or Aqueduct.

*Reference: ISO 14046:2014 — defines water footprint as including degradative use (quality) alongside consumptive use, but notes that practical methods often address them separately.*

### 6.5 Cross-Layer Incompatibility

The four layers of water impact (direct, indirect, embodied, impact) use fundamentally different data models:

| Layer | Data model | Unit basis |
|-------|-----------|------------|
| Direct | Operational measurement | L or m³ per facility |
| Indirect | Process-based LCI or grid statistics | L/kWh |
| Embodied | Process LCI or MRIO | L per product unit |
| Impact | Geospatial watershed model | Dimensionless CF per location |

Combining them requires unit harmonisation and careful handling of spatial attribution. There is no single database that spans all four layers.

### 6.6 Model Selection Determines Outcome

The choice of impact framework is not neutral. Using AWARE vs Aqueduct vs ReCiPe vs WSI for the same water volume at the same location will produce different results, different rankings, and potentially different decisions.

There is no universally agreed "correct" framework. The SWI specification selects AWARE based on its ISO 14046 alignment and WULCA consensus status, but this is a methodological choice, not an objective truth.

*Reference: Pfister, S., & Bayer, P. (2014). Monthly water stress: spatially and temporally explicit consumptive water footprint of global crop production. Journal of Cleaner Production, 73, 52–62. — demonstrates that different methods produce substantially different geographic rankings.*

### 6.7 Non-Comparability Across Frameworks

Results from AWARE (L-eq) and Aqueduct (0–5 score) cannot be directly compared or combined. They use different units, different scales, and different underlying models. Presenting them side by side (as this repository recommends) is appropriate for context. Averaging them, weighting them, or deriving a composite score is not methodologically supported.

---

## References

- Boulay, A.-M., et al. (2018). The WULCA consensus characterization model for water scarcity footprints: assessing impacts of water consumption based on available water remaining (AWARE). *Int J Life Cycle Assess*, 23(2), 368–378. https://doi.org/10.1007/s11367-017-1333-8
- Seitfudem, G., et al. (2025). The updated and improved method for water scarcity impact assessment in LCA, AWARE2.0. *Journal of Industrial Ecology*, 1–17. https://doi.org/10.1111/jiec.70023
- AWARE 2.0 dataset [Data set]: https://doi.org/10.5281/zenodo.15133241
- Kuzma, S., Saccoccia, L., & Chertock, M. (2023). Aqueduct 4.0: Updated Decision-Relevant Global Water Risk Indicators. *WRI Technical Note*. https://doi.org/10.46830/writn.23.00061
- WRI Aqueduct 4.0 data download: https://www.wri.org/data/aqueduct-global-maps-40-data
- WRI Aqueduct indicator definitions: https://www.wri.org/aqueduct/help-center/water-risk-indicators
- Müller Schmied, H., et al. (2024). The global water resources and use model WaterGAP v2.2e. *Geoscientific Model Development*, 17(23), 8817–8852. https://doi.org/10.5194/gmd-17-8817-2024

## Further reading

- [Why AI's Water Footprint Is Harder to Measure Than Carbon](https://caohongliu.medium.com/why-ais-water-footprint-is-harder-to-measure-than-carbon-096fc76536ad) — a plain-language companion article on the measurement, attribution, and framework-comparability challenges documented above.
