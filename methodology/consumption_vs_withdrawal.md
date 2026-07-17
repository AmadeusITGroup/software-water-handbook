# Consumption vs Withdrawal

## The distinction

| | Consumption | Withdrawal |
|---|---|---|
| **Definition** | Water permanently removed from the watershed (evaporated, incorporated into product, transferred to another basin) | Total water taken from a source (includes water returned after use) |
| **Example** | Cooling tower: withdraws 100L, 80L evaporates (consumed) | Once-through: withdraws 10,000L, returns 9,980L (consumes only 20L) |
| **Impact mechanism** | Reduces available supply for downstream users | Temporarily reduces availability, may alter temperature/quality |
| **SWI metric** | SWI-C | SWI-W |

## Why both matter

A consumption-only metric would rank the once-through system as preferable (20L consumed vs 80L). But withdrawing 10,000L still affects:
- Downstream availability during the withdrawal period
- Aquatic thermal ecology (heated return water)
- Other users who need that water simultaneously
- Regulatory compliance (many permits limit withdrawal, not just consumption)

## AWARE: designed for consumption only

AWARE was explicitly designed for water **consumption**. Key evidence:

1. **Paper title:** "assessing impacts of **water consumption** based on available water remaining" (Boulay et al. 2018)
2. **Method scope:** "the potential to deprive another user when **consuming** water in this area"
3. **Inventory definition** (openLCA): "water **consumed** during the process (integrated into the product, evaporated or transferred to another watershed)"
4. **AWARE improvement paper:** "highlights the importance of considering **consumption rather than withdrawal**" (Nunez et al. 2020)

**Applying AWARE to withdrawal without adjustment overstates impact** for systems with high return flows.

## How this flows through each layer

| Layer | Consumption | Withdrawal |
|-------|-------------|-----------|
| 1. Direct | Water evaporated by cooling (WUE basis) | Total water taken from source |
| 2. Indirect | Water consumed by power plants (evaporation from cooling towers) | Water withdrawn by plants (includes once-through) |
| 3. Embodied | Typically consumption-based in LCI databases | Less commonly reported |
| 4. Impact | AWARE CF applies directly | **No validated stress factor yet** |
| SWI metric | SWI-C (defined) | SWI-W (formula pending) |

## Current SWI specification status

The stress-adjusted formula is defined for **consumption only**:

```
SWI-S = ((D × S_D + I × S_I) + E × S_E) / R
```

Where all variables represent consumption and S is the AWARE CF.

For withdrawal, the specification notes "For SWI for withdrawal, discussed next" — the formula is **not yet defined**. The working group agreed that:
- SWI-C and SWI-W should be separate metrics
- Whether AWARE applies to withdrawal requires further clarification
- No existing guidance for combining C and W into a single metric was identified

## Open questions

1. Should SWI-W use the same AWARE CF, a modified CF, or a different stress factor (e.g. Aqueduct bws)?
2. If AWARE is applied to withdrawal, should a consumption-to-withdrawal ratio discount be applied?
3. Is there ISO or LCA methodology guidance for stress-adjusting withdrawal?

## References

- Boulay, A.-M., et al. (2018). https://doi.org/10.1007/s11367-017-1333-8
- Nunez, M., et al. (2020). Improvement of the water footprint AWARE model. https://www.researchgate.net/publication/341793991_Improvement_of_the_water_footprint_AWARE_model
- openLCA (2024). AWARE 1.2 method description. https://www.openlca.org/openlca-lcia-method-package-2-6-0-update-aware-1-2-now-available/
- [SWI Specification — Green Software Foundation](https://greensoftware.foundation/standards/swi/)
