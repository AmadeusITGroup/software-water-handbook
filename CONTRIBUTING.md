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

## Licensing of contributions (inbound = outbound)

By submitting a contribution, you agree it is provided under the **same licenses
as the project**: **MIT** for code and **CC-BY-4.0** for data and documentation
(see [LICENSE.md](LICENSE.md)). Do not submit material you cannot license this way.

## Developer Certificate of Origin (DCO)

All contributions require a **DCO sign-off**, certifying you have the right to
submit the work under the project licenses (see <https://developercertificate.org/>).
Add a sign-off line to every commit:

```bash
git commit -s -m "Your message"
```

This appends `Signed-off-by: Your Name <your@email>` to the commit. Configure your
identity once with `git config user.name` and `git config user.email`. The DCO is
how Green Software Foundation / Linux Foundation projects manage contribution
provenance, so adopting it now keeps the project ready for donation.

## Neutrality

This repository documents the methodology choices of the [SWI specification](https://greensoftware.foundation/standards/swi/) and the differences between impact frameworks objectively. It stays **framework-neutral**: the direct-water layer is in physical litres, and impact-weighting (AWARE, Aqueduct, or others) is deferred to the impact layer rather than prescribed.

Where conflicts exist between frameworks, we document both positions with references. See [conflicts_and_limitations.md](methodology/conflicts_and_limitations.md).

## Code of conduct

Be respectful, constructive, and evidence-based. Technical disagreements should reference published methodology or data, not authority or opinion.
