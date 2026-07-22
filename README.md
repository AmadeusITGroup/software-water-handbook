# Software Water Impact Resources

[![Validate extractions](https://github.com/AmadeusITGroup/software-water-handbook/actions/workflows/validate.yml/badge.svg)](https://github.com/AmadeusITGroup/software-water-handbook/actions/workflows/validate.yml)

A curated collection of datasets, models, and references for measuring the water impact of software systems and data centers.

## What this is

This repository **aggregates sources** and **structures knowledge** for computing software water impact across four layers: direct operational water, indirect electricity-generation water, embodied water, and scarcity-weighted impact.

This repository **does not propose a new framework**. It follows the methodology choices of the [SWI specification](https://greensoftware.foundation/standards/swi/) and aims to be a practical companion for anyone implementing it.

## Context

The [Green Software Foundation](https://greensoftware.foundation/) is developing the [Software Water Intensity (SWI)](https://greensoftware.foundation/standards/swi/) specification — a standard for measuring and reporting the water impact of software systems.

As a contributor to the SWI working group on behalf of [Amadeus](https://amadeus.com/), we found that assembling the relevant data sources, understanding their interactions, and identifying their limitations required significant research that falls outside the scope of the specification itself.

The SWI specification defines *what* to measure and *how* to compute it. This repository provides the *where to find the data*, *which sources to use*, and *what conflicts exist* between them.

No equivalent open resource currently exists that consolidates these sources into a structured, referenced guide.

## Repository structure

```
software-water-impact-resources/
├── README.md                           # This file
├── CONTRIBUTING.md                     # How to contribute
├── LICENSE                             # MIT (code)
├── LICENSE-data.md                     # CC-BY-4.0 (data & documentation)
├── .gitignore                          # Excludes copyrighted PDFs, bulk data
├── docs/
│   └── 01_framework_overview.md        # 4-layer architecture + SWI formula
├── sources/
│   ├── dataset_index.md                # Central index of all sources
│   ├── direct_water/                   # Layer 1: provider data, WUE, allocation
│   │   ├── README.md
│   │   ├── how_to_calculate_swi.md     # general calculation guide
│   │   ├── schema.json                 # extraction schema
│   │   ├── extraction/                 # shared pipeline (registry, config, validator)
│   │   ├── <company>/                  # per company: README, worked_example, json/, csv/
│   │   └── cross_provider/             # combined parameter tables + data dictionary
│   ├── indirect_water/                 # Layer 2: electricity water intensity
│   │   └── README.md
│   ├── embodied_water/                 # Layer 3: LCI and MRIO databases
│   │   └── README.md
│   └── impact_models/                  # Layer 4: AWARE and Aqueduct
│       └── README.md
└── methodology/
    ├── conflicts_and_limitations.md    # Known conflicts between frameworks
    └── consumption_vs_withdrawal.md    # The C vs W distinction across all layers
```

**Layer maturity:** `direct_water` has structured extractions (schema-conformant
JSON + derived CSVs) and worked examples for Microsoft, Google, and AWS.
`indirect_water`, `embodied_water`, and `impact_models` currently provide curated
source references and methodology; structured extractions there are planned.

## Key findings

1. **AWARE and Aqueduct can produce contradictory rankings** for the same locations. This is not an error — they measure different dimensions of water scarcity.
2. **AWARE is designed for water consumption only.** Applying it to withdrawal is methodologically non-standard.
3. **Sub-national AWARE factors exist** (3,652 regions) and can differ by 8.5× within a single country.
4. **No pre-calculated grid-level water intensity dataset exists.** Building one requires combining plant-level data (EIA/eGRID) with watershed-level stress factors.
5. **Software-level water attribution** is the main practical barrier — providers report site totals but not workload-level allocation.

## How to use this

- **Implementing SWI?** Start with [01_framework_overview.md](docs/01_framework_overview.md) for the formula, then follow the source folders for data sources.
- **Assessing a specific location?** Check [impact_models](sources/impact_models/README.md) for AWARE/Aqueduct and [conflicts_and_limitations.md](methodology/conflicts_and_limitations.md) for known issues.
- **Looking for a specific dataset?** See [dataset_index.md](sources/dataset_index.md) for the full table.

## Data provenance and licensing

This repository **references** all source documents (corporate sustainability
reports, government datasets, academic papers) by their official links. It
**does not redistribute** copyrighted source files (PDFs, spreadsheets, or
archived web pages). Copyright in the referenced sources remains with their
respective owners.

The curated extractions under `sources/**/json/` and the tables derived from them
under `sources/**/csv/` and `sources/**/cross_provider/` contain **factual values**
(measurements, provenance metadata, links) extracted for reference, not
reproductions of copyrighted text. Each extracted value retains a link and
citation to its primary source so it can be independently verified.

See [LICENSE](LICENSE) (code) and [LICENSE-data.md](LICENSE-data.md) (data & documentation) for details.

## Related resources

- [SWI Specification (Green Software Foundation)](https://greensoftware.foundation/standards/swi/)
- [AWARE 2.0 dataset (Zenodo)](https://doi.org/10.5281/zenodo.15133241)
- [Aqueduct 4.0 (World Resources Institute)](https://www.wri.org/aqueduct)
- [Cloud Carbon Footprint](https://www.cloudcarbonfootprint.org/) — the carbon equivalent; no water counterpart exists yet

## Background reading

- [Why AI's Water Footprint Is Harder to Measure Than Carbon](https://caohongliu.medium.com/why-ais-water-footprint-is-harder-to-measure-than-carbon-096fc76536ad) — companion article by the maintainer, on the measurement and comparability challenges this repository addresses.

## Future directions

- Machine-readable dataset schema (YAML) for programmatic access
- Community-contributed regional data (EU grid water intensity, Asia-Pacific provider data)
- Expanded coverage as new provider sustainability reports are published

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. The project's proposed
decision-making and transfer requirements are documented in
[docs/GOVERNANCE.md](docs/GOVERNANCE.md). Contributions are also subject to the
[Code of Conduct](CODE_OF_CONDUCT.md) and [Security Policy](SECURITY.md).

This repository is currently maintained under Amadeus stewardship. It is
designed to be compatible with a future community or Green Software Foundation
hosting arrangement, but it is not an official GSF deliverable yet.

## License

Permissive dual license:

- **Code** (Python scripts, `schema.json`, `datapackage.json`) → **MIT** — [`LICENSE`](LICENSE)
- **Data & documentation** (`**/*.md`, `sources/**/json/*.json`, `sources/**/csv/*.csv`) → **CC-BY-4.0** — [`LICENSE-data.md`](LICENSE-data.md)

Both are attribution-only (no copyleft). Contributions are accepted under the same
licenses (inbound = outbound) with a Developer Certificate of Origin (DCO)
sign-off — see [CONTRIBUTING.md](CONTRIBUTING.md).

## Maintainer

Hongliu Cao, PhD — Amadeus, contributing to the GSF SWI working group.
