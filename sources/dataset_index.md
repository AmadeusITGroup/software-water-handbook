# Dataset Index

Central registry of all data sources referenced in this repository.

## Layer 1 — Direct Water

| Name | Type | Organization | Geography | Access | Link |
|------|------|-------------|-----------|--------|------|
| Google Data Centre Water | dataset | Google | Global (site-level) | open | https://datacenters.google/water/ |
| Microsoft WUE | dataset | Microsoft | Global + regional | open | https://datacenters.microsoft.com/sustainability/efficiency/ |
| AWS WUE | dataset | Amazon | Global fleet | open | https://www.aboutamazon.com/news/sustainability/amazon-data-center-water-usage |
| Equinix Customer Water Reports | dataset | Equinix | Customer deployment | restricted | https://www.equinix.com/resources/infopapers/customer-water-reports |
| Equinix Sustainability Data | dataset | Equinix | Global fleet | open | https://www.equinix.com/resources/data-sheets/sustainability-data-summary |
| Meta Water/WUE | dataset | Meta | Global fleet | open | https://www.datacenterdynamics.com/en/news/meta-data-center-electricity-consumption-hits-14975gwh-leased-data-center-use-nearly-doubles/ |
| Apple Environmental Report | dataset | Apple | Corporate total | open | https://www.apple.com/environment/pdf/Apple_Environmental_Progress_Report_2025.pdf |
| NVIDIA Sustainability Report | dataset | NVIDIA | Corporate total | open | https://images.nvidia.com/aem-dam/Solutions/documents/NVIDIA-Sustainability-Report-Fiscal-Year-2025.pdf |
| Salesforce Impact Report | dataset | Salesforce | Corporate total | open | https://www.salesforce.com/en-us/wp-content/uploads/sites/4/documents/white-papers/salesforce-fy25-stakeholder-impact-report.pdf |
| Scope3 WUE Methodology | model | Scope3 | Generic | open | https://preview.methodology.scope3.com/water |
| Equinix WUE Explainer | study | Equinix | Generic | open | https://blog.equinix.com/blog/2024/11/13/what-is-water-usage-effectiveness-wue-in-data-centers/ |

## Layer 2 — Indirect Water (Electricity)

| Name | Type | Organization | Geography | Access | Link |
|------|------|-------------|-----------|--------|------|
| Berkeley Lab Water IMPACT Tool | tool | LBNL | U.S. | open | https://industrialapplications.lbl.gov/water-impact-tool |
| EPA eGRID | dataset | U.S. EPA | U.S. | open | https://www.epa.gov/egrid |
| EIA-923 | dataset | U.S. EIA | U.S. | open | https://www.eia.gov/electricity/data/eia923/ |
| EIA-860 | dataset | U.S. EIA | U.S. | open | https://www.eia.gov/electricity/data/eia860/ |
| ENTSO-E Transparency Platform | dataset | ENTSO-E | Europe | open (registration) | https://transparency.entsoe.eu/ |
| ecoinvent (energy processes) | dataset | ecoinvent | Global | commercial | https://ecoinvent.org/database/ |
| GaBi (energy processes) | dataset | Sphera | Global | commercial | https://fslci.org/databases/gabi-lca-databases/ |

## Layer 3 — Embodied Water

| Name | Type | Organization | Geography | Access | Link |
|------|------|-------------|-----------|--------|------|
| ecoinvent | dataset | ecoinvent | Global | commercial | https://support.ecoinvent.org/introduction-to-the-database |
| GaBi | dataset | Sphera | Global | commercial | https://fslci.org/databases/gabi-lca-databases/ |
| EU Environmental Footprint | dataset | EU/Sphera | EU | open | https://lcdn.thinkstep.com/index.xhtml?stock=Free_GaBi_data |
| EXIOBASE | dataset | NTNU/TNO | Global | open | https://zenodo.org/records/14614930 |
| REX3 (resolved EXIOBASE) | dataset | Various | Global | open | https://zenodo.org/records/10354283 |

## Layer 4 — Impact Models

| Name | Type | Organization | Geography | Access | Link |
|------|------|-------------|-----------|--------|------|
| AWARE 2.0 | model | WULCA / CIRAIG | Global | open | https://zenodo.org/records/15133241 |
| AWARE description | study | WULCA | — | open | https://wulca-waterlca.org/what-is-aware/ |
| Aqueduct 4.0 | model | WRI | Global | open | https://www.wri.org/data/aqueduct-global-maps-40-data |
| Aqueduct Indicator Help | study | WRI | — | open | https://www.wri.org/aqueduct/help-center/water-risk-indicators |
| ReCiPe | model | RIVM | Global | open | https://www.rivm.nl/en/life-cycle-assessment-lca/recipe |

## Cross-Layer / Integration

| Name | Type | Organization | Geography | Access | Link |
|------|------|-------------|-----------|--------|------|
| Cloud Carbon Footprint | tool | Thoughtworks | Global | open | https://www.cloudcarbonfootprint.org/ |
| Google Cloud Carbon Footprint | tool | Google | Google Cloud | restricted | https://docs.cloud.google.com/carbon-footprint/docs/methodology |
| re:cinq Cloud CPU Energy | tool | re:cinq | AWS | open | https://re-cinq.com/blog/cloud-cpu-energy-consumption |
| SWI Specification | study | Green Software Foundation | — | open | https://greensoftware.foundation/standards/swi/ |

## Methodology References

| Name | Type | Authors | Year | Link |
|------|------|---------|------|------|
| AWARE original paper | study | Boulay et al. | 2018 | https://doi.org/10.1007/s11367-017-1333-8 |
| AWARE 2.0 paper | study | Seitfudem et al. | 2025 | https://doi.org/10.1111/jiec.70023 |
| WaterGAP 2.2e | model | Müller Schmied et al. | 2024 | https://doi.org/10.5194/gmd-17-8817-2024 |
| Aqueduct 4.0 Technical Note | study | Kuzma et al. | 2023 | https://doi.org/10.46830/writn.23.00061 |
| AWARE improvement paper | study | Nunez et al. | 2020 | https://www.researchgate.net/publication/341793991_Improvement_of_the_water_footprint_AWARE_model |
