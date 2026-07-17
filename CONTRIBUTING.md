# Contributing

Thank you for your interest in contributing to this resource.

## What we accept

- **Datasets** — LCI databases, grid water intensity data, provider operational data, water stress/impact models
- **Impact models** — characterization factors, risk frameworks with peer-reviewed methodology
- **Tools** — references to working tools that integrate these datasets for water impact calculation
- **Academic studies** — with reproducible data or methodology that advances the field
- **Corrections** — to links, methodology descriptions, or data values

## What we do not accept

- Marketing content or vendor pitches
- Opinion articles without peer-reviewed backing
- Unverified claims or data without traceable sources
- Duplicate entries already covered in existing docs

## How to contribute

### Adding a data source

Each entry must include these mandatory fields:

| Field | Description |
|-------|-------------|
| **Name** | Official dataset or tool name |
| **Link** | URL to the primary/official source |
| **Layer** | `direct` / `indirect` / `embodied` / `impact` |
| **Type** | `dataset` / `model` / `tool` / `study` |
| **Description** | What it provides (3 lines max) |

Optional but helpful:
- Geography coverage
- Temporal resolution
- Access type (open / restricted / commercial)
- Known limitations

### Process

1. Open an issue describing what you want to add or change
2. Fork the repository and make your changes
3. Submit a pull request referencing the issue
4. A maintainer will review for accuracy, relevance, and formatting

### Updating provider data

Provider sustainability reports typically publish annually (Q1–Q2). When new WUE or water data is published:
1. Update the relevant entry in `sources/direct_water/README.md`
2. Update `sources/dataset_index.md`
3. Note the report year in your PR description

## Neutrality

This repository follows the methodology choices of the [SWI specification](https://greensoftware.foundation/standards/swi/) (AWARE as primary impact model, Aqueduct as diagnostic context). It does not advocate for alternative frameworks but documents their differences objectively.

Where conflicts exist between frameworks, we document both positions with references. See [conflicts_and_limitations.md](methodology/conflicts_and_limitations.md).

## Code of conduct

Be respectful, constructive, and evidence-based. Technical disagreements should reference published methodology or data, not authority or opinion.
