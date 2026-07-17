# Extraction Workflow — Step by Step

A repeatable procedure for turning one published report into a validated,
schema-conformant extraction plus derived parameter tables. It uses the
**Microsoft 2026 Environmental Data Fact Sheet** as the running example; follow
the same steps for any other report.

Prerequisites: `python`, `jsonschema`; a `config.local.json` pointing `pdf_root`
at the local folder holding the source documents (gitignored).

---

## Step 1 — Register the report

Add a row to [`report_registry.csv`](report_registry.csv):

| column | example |
|--------|---------|
| `company` | `microsoft` |
| `report_id` | `microsoft_environmental_data_factsheet_2026` (clean stem = output filename) |
| `report_title` | `Microsoft 2026 Environmental Data Fact Sheet` |
| `organization` | `Microsoft` |
| `year` | `FY25` |
| `link` | official URL |
| `local_pdf` | filename only (resolved under `pdf_root`) |

Create the company folder if new: `<company>/{json,csv}/`.

## Step 2 — Open the primary source

Resolve the local file under `pdf_root`. Use the text extract (`.txt`) for
searching; keep the PDF for tables/figures. **Never** copy the source into the
repo — reference it by `link` and `local_archive_path` only.

## Step 3 — Locate all water content

Scan the source for every water figure, not just the headline ones:

```bash
grep -n -iE "water|withdraw|consum|discharge|reuse|WUE|replenish|water stress|aqueduct|aware" report.txt
```

Then read each hit **in full** (tables and their footnotes). For Microsoft this
surfaced: Table 8 (annual water & effluents), Table 14 (by region and source),
Table 15 (29 datacentre locations), the FY25 water-stress note, and the WUE /
replenishment narrative.

## Step 4 — Pin down the definitions (boundaries)

Before recording any number, determine and note, per metric:

- **Flow** — withdrawal / consumption / discharge / reuse / replenishment /
  avoided / "provider-reported water use" (a "water use" figure not split into
  withdrawal vs consumption).
- **End uses** — cooling, humidification, all operations, etc.
- **Facility scope** — owned datacentres vs all corporate operations (offices,
  labs). *Microsoft WUE = owned datacentres + cooling/humidification; the volume
  tables = all corporate operations. Different boundaries.*
- **Freshwater status**, **water sources**, **units**, **reporting standard**
  (e.g. GRI 303-3/4/5).
- **Sanity identities** — e.g. `consumption = withdrawal − discharge`
  (Microsoft FY25: 13,266 − 5,096 = 8,170 ML ✓). Cross-check any derived column
  (Microsoft's "Olympic pools" ≈ withdrawal / 2.5) to confirm you parsed the
  right column.

## Step 5 — Author the JSON (guided by `../schema.json`)

Write `<company>/json/<report_id>.json` with:

1. **`report`** — entity, edition, `report_year`, `publication_year`,
   `source_document_type`, `reporting_period`, `source_url`,
   `local_archive_path`, `accessed_at`. Set `restatement` if prior years were
   recalculated (Microsoft recalculated FY20–FY24 and adjusted for the ABK
   acquisition).
2. **`definitions.metric_definitions`** — one per distinct metric, with exact
   `definition_text`, `metric_family`, `quantity_kind`, `water_accounting_flow`,
   `water_layer`. Define once; observations reference by id.
3. **`definitions.scope_definitions`** — one per reporting scope (corporate
   global, by region, by source, datacentre location, water-stress subset).
4. **`definitions.framework_definitions`** — if the report uses a risk/impact
   framework (Microsoft uses WRI Aqueduct → `risk_tool`, indicator
   `baseline_water_stress`).
5. **`observations`** — one per atomic (flow × period × geography × scope):
   - **Normalize to metric.** `normalized_unit` must be metric — litres (`L`) for
     volumes, `L/kWh` for intensities. Convert non-metric source units (US gal →
     L at 3.785411784 L/gal; ML → L ×1e6; million m³ → L ×1e9) into
     `normalized_value` while keeping the original figure and unit in
     `value` / `reported_unit`.
   - Use `value_status`: `reported`, `bounded` (with `value_low`/`value_high` and
     a `greater_than`/`less_than` qualifier), or `below_reporting_threshold`
     (a dash/blank — **not** zero; e.g. Auckland).
   - Attach `risk_context` + `framework_definition_ids` for water-stress rows.
   - Set `quality.assurance` (Microsoft: Section 1 = limited assurance; Section 2
     = not reviewed).
6. **`relationships`** — prevent double counting and preserve structure:
   `rollup_of` (total ← by-source), `subset_of` (water-stressed ⊂ total),
   `same_concept_as` (year-over-year).

Tips that avoid rework:
- Keep flows **separate**; never merge withdrawal and consumption.
- Distinguish **company vs cloud service** (Microsoft ≠ Azure) in scope names and
  caveats.
- Replenishment / avoided / progress are **`context_only`** — not withdrawal or
  consumption; never net them against operational water.
- For large tabular reports, a transient transcription script is fine, but the
  committed deliverable is the JSON (delete the builder afterwards).

## Step 6 — Validate

```bash
python validate_extractions.py
```

Fix every error (`additionalProperties`, missing required fields, enum
mismatches) until the file passes.

## Step 7 — Completeness re-scan

Re-run the Step 3 grep and confirm **every** water figure is now represented.
For Microsoft this second pass caught four replenishment/conservation metrics
(14.2 M m³ delivered, 133 M m³ contracted, 30% Chicago reduction, 8.5 M m³ FIDO)
that the first pass missed. Do not skip this.

## Step 8 — Derive parameter tables

```bash
python ../cross_provider/derive_parameters.py
```

This regenerates `<company>/csv/<theme>.csv` (wue, water_volumes, water_shares,
replenishment_and_progress) and the combined `cross_provider/*_all_providers.csv`.
Never hand-edit derived CSVs.

## Step 9 — Write the company docs

### `<company>/README.md`
What was extracted, per-source observation counts, and key caveats (boundaries,
company ≠ cloud service, which impact framework the company itself reports). The
**Sources** section must list each source as a **clickable link** (the
`source_url` from its JSON), not just a title — do not defer readers to the JSON
for the link.

### `<company>/worked_example.md`
An end-to-end **litres** calculation. To avoid thin or stale examples, it **must**
contain all of the following (or explicitly state, with the reason, when the data
does not support one):

1. **Metric units.** Litres / ML are primary. If a source reports US gallons (or
   other non-metric units), convert to litres and show the metric value first,
   with the original in parentheses — e.g. "≈ 9,463.5 ML (2.5 billion US gal)".
   Conversion: 1 US gal = 3.785411784 L; 1 ML = 1,000,000 L.
2. **A "what water means" boundary table** — flow, end-uses, facility scope,
   resolution, whether consumption/discharge are reported, freshwater status. If
   the provider does not disaggregate a dimension, say so.
3. **Use ALL extracted sources, not just the first/simplest.** Cross-check the
   company's `json/` folder and `csv/` tables and incorporate every relevant
   figure (WUE trend, volumes, replenishment, benchmarks). A worked example that
   ignores extracted data is a defect — re-open it whenever new sources are added.
4. **Both `SWI-C` and `SWI-W`.** Compute each where the data supports it; where it
   does not (e.g. the provider reports withdrawal only), **state explicitly which
   metric is unavailable and why**. Never merge C and W.
5. **Attribution method and the missing-data list.** State the method used
   (provider-attributed / WUE × energy / site × share) and enumerate what blocks a
   defensible per-workload figure (e.g. missing total IT-energy denominator,
   global-only resolution, boundary mismatches).
6. **The company's own impact/risk framework** — name it (e.g. WRI Aqueduct bws)
   or state that the company names none. This is context; the actual
   impact-weighting is deferred to the impact layer.
7. **"What you can / cannot say"** — a short honest-claims section.

> When new sources for a company are extracted (Step 1–8), **return to this step**
> and update the worked example so it reflects the full data set. Do not leave it
> pinned to the earliest source.

## Step 10 — Update status

Refresh [`extraction_index.csv`](extraction_index.csv) so the report shows
`done`.

---

## Checklist

- [ ] Registered in `report_registry.csv`
- [ ] All water content located (Step 3 grep) and read in full
- [ ] Definitions/boundaries pinned; identities cross-checked
- [ ] JSON authored with definitions, scopes, observations, relationships
- [ ] Validates against `../schema.json`
- [ ] Completeness re-scan passed (nothing missed)
- [ ] Parameter tables regenerated
- [ ] Company README written (per-source counts + caveats + Sources as clickable links)
- [ ] worked_example.md written and complete:
  - [ ] metric units (litres/ML primary; non-metric converted, original in parens)
  - [ ] "what water means" boundary table
  - [ ] uses ALL extracted sources (not just the first/simplest)
  - [ ] both SWI-C and SWI-W (computed, or "unavailable because…")
  - [ ] attribution method + missing-data list
  - [ ] company's own impact/risk framework noted (or "none named")
  - [ ] "what you can / cannot say"
- [ ] `extraction_index.csv` updated
