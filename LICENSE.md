# License (Pending Amadeus Open-Source Approval)

> **This is a placeholder.** The final license must be confirmed by Amadeus
> open-source policy before public release. Do not publish without a finalized
> license.

## Recommended dual-license approach

Data-and-documentation repositories commonly separate the license for content
from the license for code:

| Content type | Recommended license | Rationale |
|--------------|--------------------|-----------|
| Documentation, curated data tables, methodology notes (`docs/`, `methodology/`, `sources/**/*.md`, `sources/**/json/*.json`, `sources/**/csv/*.csv`, `sources/**/cross_provider/*.csv`) | **CC-BY-4.0** | Standard for open data and reference material; requires attribution |
| Code (notebooks, scripts) | **Apache-2.0** | Permissive, patent-grant, widely accepted for open-source code |

## Important scope note

This repository **references** third-party source documents (corporate
sustainability reports, government datasets, academic papers) by official link.
It **does not redistribute** those documents. Copyright in the referenced
sources remains with their respective owners. The curated data tables in this
repository contain factual values (measurements, links, provenance metadata)
extracted for reference, not reproductions of copyrighted text.

## Action required before release

1. Confirm the license choice with Amadeus legal / open-source office.
2. Replace this file with the finalized `LICENSE` text.
3. Add an SPDX identifier header to code files if required by policy.
