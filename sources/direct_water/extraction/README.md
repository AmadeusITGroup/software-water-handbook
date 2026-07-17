# Report Extraction Pipeline

This folder turns published water reports into structured, schema-conformant
extractions, one JSON document per report edition, organized by company.

**For a detailed, repeatable step-by-step procedure (with the Microsoft report as
a worked example), see [`EXTRACTION_WORKFLOW.md`](EXTRACTION_WORKFLOW.md).** The
summary below is the quick version.

## Design

- **Input** — `report_registry.csv`: one row per source, with `company`,
  `report_id`, `report_title`, `organization`, `year`, `link`, and `local_pdf`
  (filename only).
- **Source PDFs live outside this repository.** Their directory is resolved at
  runtime from `config.local.json` → `pdf_root`. Only `config.example.json` is
  committed; `config.local.json` is gitignored. No PDFs or local paths are ever
  committed.
- **Schema** — every extraction must conform to `../schema.json`
  (draft 2020-12). The schema separates metric definitions, scope definitions,
  and framework definitions from atomic observations, and records whether
  observations may be merged (same company, over time) or compared (across
  companies).
- **Output** — `../<company>/json/<report_id>.json`.

## Workflow

1. Copy `config.example.json` to `config.local.json` and set `pdf_root` to the
   local folder holding the source PDFs.
2. Open a report from `report_registry.csv`. Use its `local_pdf` (resolved under
   `pdf_root`) and `link` as the evidence source.
3. Author one JSON document per report edition following `../schema.json`:
   - Define each metric once in `definitions.metric_definitions`.
   - Define each reporting scope once in `definitions.scope_definitions`.
   - Record one accounting flow, period, geography, and scope per observation.
   - Keep withdrawal, consumption, discharge, reuse, and provider-reported water
     use as separate flows. Do not merge across companies.
4. Save to `../<company>/json/<report_id>.json`.
5. Validate:

   ```bash
   python validate_extractions.py
   ```
6. Regenerate derived parameter tables: `python ../cross_provider/derive_parameters.py`.

## Worked example

`../amazon_aws/json/aws_sustainability_report_2025.json` is a complete, validated
example: two fleet-average withdrawal-based WUE observations (2024 and 2025) with
definitions, scope, evidence, and a same-concept relationship linking the two
years. See `../microsoft/json/` for a richer 177-observation extraction.

## Notes

- Extraction requires human judgment (definitions, boundaries, comparability),
  so it is curated and guided by the schema rather than scraped automatically.
- Facts are transcribed with citations; the schema stores short evidence
  snippets, not reproductions of copyrighted text.
