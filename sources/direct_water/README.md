# Layer 1 — Direct Water Sources

## What this covers

Water used directly at data center facilities for cooling and operations. This is the most visible and reported component, but also the hardest to attribute to a specific software workload.

## General Data Sources

| Source | Description | Link |
|--------|-------------|------|
| EESI | Data center water consumption overview | https://www.eesi.org/articles/view/data-centers-and-water-consumption |
| MOST Policy Initiative | Data center water use science note | https://mostpolicyinitiative.org/science-note/data-center-water-use/ |
| APS Tech Advisors | U.S. data center water trends 2025–2030 | https://apstechadvisors.com/data-center-water-consumption-in-the-us-challenges-trends-and-market-opportunities-for-2025-2030/ |

## WUE (Water Usage Effectiveness)

WUE = litres of water used for cooling / kWh of IT energy.

| Source | Description | Link |
|--------|-------------|------|
| Scope3 | WUE methodology and ranges | https://preview.methodology.scope3.com/water |
| Equinix | WUE explained, cooling-type ranges (0 to 2.5 L/kWh) | https://blog.equinix.com/blog/2024/11/13/what-is-water-usage-effectiveness-wue-in-data-centers/ |

## Provider-Specific Data

| Reporting scope | What they report | Resolution | Link |
|-----------------|------------------|------------|------|
| Google | Withdrawal, discharge, and consumption at global aggregate (2021–2025), data-centre / office split, and **per data-centre location** (~40 sites); Gemini Apps per-prompt water (median 0.26 mL/prompt, global fleet-blended, text prompts only); freshwater-at-risk shares (Google's own Data Center Water Risk Framework). **No headline per-kWh WUE published.** Not a GCP-service factor. | Global + per site | https://sustainability.google/reports/google-2026-environmental-report/ |
| Microsoft | Withdrawal, discharge, consumption at **global + region + 29 datacentre sites** (withdrawal only at site level) with FY20–FY25 history and by-source breakdown; WUE reported **global FY25 = 0.27** in the 2026 report and **by broad region** (Americas 0.34, APAC 0.25, EMEA 0.03 L/kWh FY25) on the datacenter efficiency page; water-stress shares via WRI Aqueduct (current baseline). Owned datacentres and corporate operations; not Azure-specific. | Global + regional + site (WUE regional only) | https://datacenters.microsoft.com/sustainability/efficiency/ |
| AWS | Global fleet **withdrawal-based WUE** 2021–2025: 0.25 → 0.19 → 0.18 → 0.15 → 0.12 L/kWh; 2025 data-centre withdrawal ≈ 9.4 billion L; water-stress shares via WRI Aqueduct (2030 business-as-usual scenario). **Withdrawal only** — no consumption or discharge reported. | Global fleet only | https://www.aboutamazon.com/news/sustainability/amazon-data-center-water-usage |
| Equinix | Portfolio withdrawal, discharge, consumption, WUE; customer-attributed water reports | Fleet + customer-level | https://www.equinix.com/resources/infopapers/customer-water-reports |
| Meta | 3,881 ML data-centre withdrawal; WUE 0.18 L/kWh | Global fleet | https://sustainability.atmeta.com/wp-content/uploads/2024/08/Meta-2024-Sustainability-Report.pdf |
| Apple | Total withdrawal + discharge annually | Corporate total | https://www.apple.com/environment/pdf/Apple_Environmental_Progress_Report_2025.pdf |
| NVIDIA | Total withdrawal, discharge, consumption annually | Corporate total | https://images.nvidia.com/aem-dam/Solutions/documents/NVIDIA-Sustainability-Report-Fiscal-Year-2025.pdf |
| Salesforce | Total withdrawal only | Corporate total | https://www.salesforce.com/en-us/wp-content/uploads/sites/4/documents/white-papers/salesforce-fy25-stakeholder-impact-report.pdf |

Microsoft fleet reporting is not an Azure-specific disclosure. Google corporate, data-centre, and Gemini reporting is not automatically applicable to GCP. Apply a value to a cloud workload only when the service, facility ownership, geography, year, water boundary, and energy denominator are compatible.

## Structure

```
direct_water/
├── README.md                       # this file
├── how_to_calculate_swi.md         # general guide: attribution methods, decision tree, caveats
├── schema.json                     # extraction schema (guides all extractions)
├── extraction/                     # shared pipeline: registry, config, validator
│   ├── report_registry.csv         # company, report_id, link, local_pdf
│   ├── config.example.json         # PDF-root config template (config.local.json is gitignored)
│   ├── validate_extractions.py     # validate all extractions vs schema.json
│   └── extraction_index.csv        # status of planned extractions
├── <company>/                      # one folder per company
│   ├── README.md                   # what we have + caveats
│   ├── worked_example.md           # end-to-end calculation with that provider's data
│   ├── json/                       # schema-conformant extractions (SOURCE OF TRUTH)
│   └── csv/                        # WUE etc. derived from json/
└── cross_provider/                 # combined tables across providers (latest-per-key deduped)
    ├── <theme>_all_providers.csv   # combined parameter tables (wue, volumes, shares, ...)
    ├── restatements.csv            # values changed across report editions (superseded vs kept)
    ├── datapackage.json            # canonical data dictionary (shared by all tables)
    └── derive_parameters.py        # regenerates per-company + combined tables
```

Combined and per-company tables are de-duplicated **latest-per-key**: facts repeated
across report editions collapse to the most recent edition's value, and superseded
values are logged in `cross_provider/restatements.csv`. See
[`cross_provider/README.md`](cross_provider/README.md) for the rule.

## Extraction

Reports are extracted into structured, schema-conformant JSON — one document per
report edition, under each company's `json/` folder — guided by
[`schema.json`](schema.json).

- **Pipeline & how to run:** [`extraction/`](extraction/) (see its README)
- **Detailed step-by-step procedure:** [`extraction/EXTRACTION_WORKFLOW.md`](extraction/EXTRACTION_WORKFLOW.md)
- **Input registry:** [`extraction/report_registry.csv`](extraction/report_registry.csv) (`company`, `report_id`, `link`, `local_pdf`)
- **Outputs:** `<company>/json/*.json`; status in [`extraction/extraction_index.csv`](extraction/extraction_index.csv)
- **Validation:** `python extraction/validate_extractions.py`

Source PDFs are **not stored in this repository**. The extraction process resolves
them at runtime from a local directory configured in `extraction/config.local.json`
(gitignored). Every observation retains a link and citation to its primary source.

## Using the data: how to calculate

The JSON extractions are the source of truth. For **calculating** software-attributed
direct water:

- **Guide:** [`how_to_calculate_swi.md`](how_to_calculate_swi.md) — attribution methods, decision tree, caveats
- **Worked examples:** each `<company>/worked_example.md` (e.g. [`microsoft/worked_example.md`](microsoft/worked_example.md))
- **Parameters:** per-company `<company>/csv/wue.csv`, combined [`cross_provider/wue_all_providers.csv`](cross_provider/wue_all_providers.csv), dictionary [`cross_provider/datapackage.json`](cross_provider/datapackage.json)

Parameter tables are **derived** from the JSON (`python cross_provider/derive_parameters.py`)
and carry units, the consumption/withdrawal flag, a caveat, and a `source_report_id`
back-reference. Never use a value without checking those.

## The Allocation Problem

Site-level water × workload share = software-attributed water, where the workload
share is a fraction (e.g. workload IT-energy ÷ total site IT-energy). Three methods exist:

### Method 1: Provider-attributed water
The provider directly reports water allocated to a customer deployment.
- **Only known source:** Equinix customer water reports (withdrawal only)
- Best-case scenario; rarely available

### Method 2: WUE × workload energy
```
D = workload_IT_kWh × WUE (L/kWh)
```
- Requires knowing workload energy (estimated via Cloud Carbon Footprint or provider tools)
- WUE is often a fleet average, not site-specific
- **The flow of `D` matches the flow of the WUE's numerator.** AWS WUE is
  **withdrawal-based** so its `D` feeds `SWI-W`; Microsoft's WUE is "cooling +
  humidification water use," neither pure withdrawal nor pure consumption, so its `D`
  is a provider-reported water-use figure and does not cleanly map to either metric.
  Never assume a WUE gives you consumption without checking `water_flow`.

### Method 3: Site water × workload share
```
D = site_water × (workload_IT_kWh / total_site_IT_kWh)
```
- Conceptually strongest; the flow of `D` matches the flow of `site_water`, so this
  method can bound both `SWI-C` and `SWI-W` when the site publishes both (e.g. Google
  reports both per site; Microsoft only withdrawal per site; AWS none)
- Rarely feasible: total site IT kWh is not publicly disclosed

### Key limitation

Most public provider data supports **site-year validation** (does the total look reasonable?) but not **software-level attribution** (how much water is my workload responsible for?). The workload energy denominator is the primary practical barrier.

## Impact frameworks in provider reports

Providers name water-risk frameworks in their reports, but they use them for **risk
screening** (categorising a site as low / medium / high stress), **not** to compute a
scarcity-weighted water-impact number. None of AWS, Microsoft, or Google publishes a
scarcity-weighted "L-equivalent" — the way carbon reports produce a CO2-equivalent.

- **AWS** — WRI Aqueduct, 2030 business-as-usual scenario (withdrawal share).
- **Microsoft** — WRI Aqueduct, current baseline water stress (share of withdrawal / discharge / consumption).
- **Google** — its own **Data Center Water Risk Framework** for data centres; WRI Aqueduct + WWF only for offices.

That is a genuinely different framework in the Google case, and different scenarios /
bases in the AWS vs Microsoft cases, so the published stress shares are **not directly
comparable across providers**. Converting litres to a scarcity-weighted impact is the
job of the **impact layer** ([`sources/impact_models/`](../impact_models/)) — AWARE for
consumption, and no clean equivalent for withdrawal — and that choice does not depend
on which framework the provider itself cites. See
[`cross_provider/README.md`](cross_provider/README.md) for the full comparability
matrix and the framework caveats.

## References

- Trellis (2025). Behind Amazon's Industry-Leading Water Efficiency Score. https://trellis.net/article/behind-amazons-industry-leading-water-efficiency-score/
- Latitude Media. Data Center Water Use: A Black Box Google Is Trying to Change. https://www.latitudemedia.com/news/data-center-water-use-black-box-google-trying-to-change/
