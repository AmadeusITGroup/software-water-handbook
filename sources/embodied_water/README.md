# Layer 3 — Embodied Water Sources (Infrastructure & Supply Chain)

> **Status:** curated source references and methodology. Structured per-source
> extractions and worked examples (as in [`direct_water/`](../direct_water/)) are
> planned, not yet available. Contributions welcome — see
> [CONTRIBUTING](../../CONTRIBUTING.md).

## What this covers

Water embedded in the lifecycle of IT infrastructure: manufacturing servers, constructing buildings, producing materials, maintenance, and end-of-life treatment.

Typically the **smallest component** of data center water impact (relative to operational direct + indirect), but non-negligible for comprehensive lifecycle assessment.

## Data Sources

### LCI Databases

| Source | Description | Link |
|--------|-------------|------|
| ecoinvent | Comprehensive LCI database (>20,000 processes) | https://support.ecoinvent.org/introduction-to-the-database |
| GaBi (Sphera) | LCA database with industry data | https://fslci.org/databases/gabi-lca-databases/ |
| EU Environmental Footprint datasets | Free access LCI data | https://lcdn.thinkstep.com/index.xhtml?stock=Free_GaBi_data |

### Multi-Regional Input-Output (MRIO) Databases

| Source | Description | Link |
|--------|-------------|------|
| EXIOBASE | Global MRIO with environmental extensions (water) | https://zenodo.org/records/14614930 |
| REX3 (resolved EXIOBASE) | Higher-resolution variant | https://zenodo.org/records/10354283 |

### Data Center Lifecycle Studies

| Source | Description | Link |
|--------|-------------|------|
| WSP | LCA of data centre cooling systems | https://www.wsp.com/en-us/insights/how-a-new-life-cycle-assessment-is-contributing-to-more-sustainable-data-centre-cooling |

## Practical notes

- Embodied water is typically amortized over infrastructure lifetime (e.g. server lifetime of 3–5 years, building lifetime of 20–30 years)
- For a first-pass SWI estimate, embodied water (E) can often be deferred — operational water (D + I) dominates for active workloads
- When included, the stress factor S_E should correspond to the manufacturing location, not the data center location

## References

- Whitehead, B., et al. (2015). The life cycle assessment of a UK data centre. *Int J Life Cycle Assess*, 20, 332–349. https://doi.org/10.1007/s11367-014-0838-7
