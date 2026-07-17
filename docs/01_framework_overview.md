# Framework Overview

## The 4-Layer Architecture

Water impact of software systems decomposes into four layers, each requiring different data sources:

| Layer | What it measures | Key question |
|-------|-----------------|--------------|
| 1. Direct water | Water used at data center facilities | How much water does my workload's data center consume/withdraw? |
| 2. Indirect water | Water used to generate electricity | How much water did the grid use to power my workload? |
| 3. Embodied water | Water in infrastructure lifecycle | How much water went into building the hardware I use? |
| 4. Impact conversion | Scarcity weighting | How much does that water matter given local conditions? |

## The SWI Formula

The [Software Water Intensity (SWI)](https://greensoftware.foundation/standards/swi/) specification defines:

```
SWI = ((D + I) + E) / R
```

Where:
- **D** = direct operational water consumption (Layer 1)
- **I** = indirect electricity-generation water consumption (Layer 2)
- **E** = embodied water consumption (Layer 3)
- **R** = functional unit (API requests, compute hours, users, etc.)

The stress-adjusted variant:

```
SWI-S = ((D × S_D + I × S_I) + E × S_E) / R
```

Where **S** is the AWARE characterization factor at the location of each water consumption component (Layer 4).

## Two Metrics, Not One

The specification defines separate metrics for consumption and withdrawal:

- **SWI-C** — Software Water Intensity for Consumption (water permanently removed from the watershed)
- **SWI-W** — Software Water Intensity for Withdrawal (total water taken, including returned water)

These capture fundamentally different dimensions of water impact and are reported separately, not combined.

## Minimum Defensible Report

A water impact report without the following is insufficient:
1. Volume (how much)
2. Location (where)
3. Consumption/withdrawal distinction (what type)
4. Scarcity weighting (how much it matters locally)

Reporting a single unweighted litre figure without location context is the water equivalent of reporting carbon without emission factors.

## References

- [SWI Specification — Green Software Foundation](https://greensoftware.foundation/standards/swi/)
- Boulay, A.-M., et al. (2018). The WULCA consensus characterization model for water scarcity footprints. *Int J Life Cycle Assess*, 23(2), 368–378. https://doi.org/10.1007/s11367-017-1333-8
