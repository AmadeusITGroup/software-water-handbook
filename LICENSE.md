# License

> **Status: recommended, pending final sign-off.** The license below is the
> recommended default for this project, chosen to support open community
> contribution and a planned donation to the [Green Software Foundation](https://greensoftware.foundation/)
> (a Linux Foundation project). It must be confirmed by the Amadeus open-source
> office and reconciled with GSF's project-onboarding terms before public release
> or transfer. This is not legal advice.

## Dual license (permissive)

This repository contains both **code** and **data/documentation**, which are
licensed separately following common practice for data-plus-tooling projects and
Green Software Foundation / Linux Foundation conventions.

| Content type | License | Files |
|--------------|---------|-------|
| **Code** | **MIT** | scripts and schemas: `sources/**/*.py`, `sources/**/schema.json`, `sources/**/datapackage.json` |
| **Data & documentation** | **CC-BY-4.0** | everything else: `**/*.md`, `sources/**/json/*.json`, `sources/**/csv/*.csv`, `sources/**/*.csv` |

- **MIT** — <https://opensource.org/license/mit> — permissive, matches GSF code repos.
- **CC-BY-4.0** — <https://creativecommons.org/licenses/by/4.0/> — attribution required; standard for open data and reference material.

Both are **permissive** (attribution only, no share-alike/copyleft) so the material
can be freely reused and incorporated into standards and downstream tools.

## Contributions (inbound = outbound)

Unless stated otherwise, any contribution you intentionally submit for inclusion
is provided under the **same licenses** as above (MIT for code, CC-BY-4.0 for
data/documentation), and must carry a **Developer Certificate of Origin (DCO)**
sign-off (`git commit -s`). See [CONTRIBUTING.md](CONTRIBUTING.md).

## Scope note — referenced third-party sources

This repository **references** third-party source documents (corporate
sustainability reports, government datasets, academic papers) by official link.
It **does not redistribute** those documents; copyright in them remains with their
respective owners. The curated tables here contain **factual values**
(measurements, links, provenance metadata) extracted for reference, not
reproductions of copyrighted text. Note that facts themselves are generally not
copyrightable; CC-BY-4.0 governs the curation, arrangement, and written text.

## Action required before release / donation

1. Confirm MIT + CC-BY-4.0 with the Amadeus open-source office.
2. Confirm alignment with GSF project-onboarding terms (charter, contribution
   policy, and whether a CLA is required in addition to DCO).
3. Replace this file's status banner and add the full `LICENSE` (MIT) text plus a
   `LICENSE-data` (CC-BY-4.0) reference; add SPDX headers to code files if required.
