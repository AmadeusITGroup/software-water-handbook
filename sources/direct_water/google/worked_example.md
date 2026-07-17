# Worked Example — Google: Direct Water for a Cloud Workload

Estimating the **direct operational water (`D`)** of a workload on Google, in
**litres**. All values are metric; where a source reports US gallons the metric
value is primary, original in parentheses.

> **Scope.** Layer 1 (direct water), in litres. Impact-weighting (any framework)
> is deferred to the **impact layer** (`sources/impact_models/`). See the note at
> the end on what Google itself reports.

Parameter values come from this folder's `csv/` tables, derived from `json/`:
`csv/per_unit_water.csv`, `csv/water_volumes.csv`, `csv/replenishment_and_progress.csv`.

---

## First: what "water" means here (read before calculating)

| Dimension | Per-prompt (`per_unit_water.csv`) | Volume totals (`water_volumes.csv`) |
|-----------|-----------------------------------|--------------------------------------|
| **Flow** | consumption (per Gemini prompt) | **withdrawal, discharge AND consumption** |
| **Denominator** | **per prompt** (not per kWh) | none (annual totals) |
| **Facility scope** | Gemini Apps inference | all Google **data centres + offices** |
| **Resolution** | service-level (Gemini Apps) | corporate total, DC/office split, **per location** (~40 sites) |
| **Withdrawal / discharge** | not reported | **both reported**; consumption = withdrawal − discharge |

Key facts:
- Google reports **all three flows** — withdrawal, discharge, and consumption —
  at aggregate (2021–2025), as a data-centre/office split, and per location. So
  **both SWI-C and SWI-W are derivable** from the volume tables. Contrast AWS
  (withdrawal only) and note this corrects an earlier "consumption-only" reading.
- Google still publishes **no per-kWh WUE**, so there is no `wue.csv`; the
  workload-usable intensity is **per prompt**.
- **Not GCP-attributed** — totals are corporate; the per-prompt figure is Gemini
  Apps specifically.

---

## Scenario A — AI inference via the per-prompt figure (the workload-usable one)

Google is the only provider here that publishes a **per-request** water figure,
which is directly usable for an AI-inference workload without an energy denominator.

From `csv/per_unit_water.csv`:

| provider | service | period | value | unit | value_liters | denominator | water_flow |
|----------|---------|--------|-------|------|--------------|-------------|------------|
| Google | Gemini Apps inference | 2025 | 0.26 | mL/prompt | 0.00026 L | prompt | consumption |

For a workload of **10 million** median Gemini text prompts:

```
D_C = prompts x per_prompt_water = 10,000,000 x 0.00026 L = 2,600 L      -> feeds SWI-C
```

So ~**2,600 litres** of consumption for 10 M prompts. This is `SWI-C`
(consumption). The per-prompt figure is a consumption-only intensity, so `SWI-W`
is not derivable *from this route* — but it **is** derivable from the volume
tables (Scenario C).

Caveats: median text prompt only (not images/video/long context); Gemini Apps
specifically, not generic GCP; May 2025 methodology.

## Scenario B — Can the corporate totals be allocated to a workload?

`csv/water_volumes.csv` gives Google's **2025 totals** for every flow:

| flow | scope | period | value | metric value |
|------|-------|--------|-------|--------------|
| withdrawal | data centres + offices | 2025 | 14,689 million US gal | **≈ 55,600 ML** |
| discharge | data centres + offices | 2025 | 3,820 million US gal | ≈ 14,460 ML |
| consumption | data centres + offices | 2025 | 10,869 million US gal | **≈ 41,140 ML (41 billion L)** |
| consumption | data centres only | 2025 | 10,523 million US gal | ≈ 39,830 ML |

To attribute a total by energy share `s = workload_IT_kWh / total_Google_IT_kWh`:

```
D_C = s x 41.14e9 L        D_W = s x 55.6e9 L
```

*Blocked:* Google does not publish **total Google IT energy** (the denominator).
So the corporate/site totals are for **site-year validation**, not per-workload
attribution. Use the per-prompt figure (Scenario A) for inference workloads.

## Scenario C — Region-wise water for a workload located at a specific site

Because Google reports **per-location** withdrawal, discharge, and consumption,
you can bound the water footprint of a workload that runs in a known region. From
`csv/water_volumes.csv` (2025, The Dalles, OR — million US gal → ML):

| flow | value | metric value |
|------|-------|--------------|
| withdrawal | 654.3 | **≈ 2,477 ML** |
| discharge | 185.3 | ≈ 701 ML |
| consumption | 469.0 | **≈ 1,775 ML** |

If a workload uses share `s_site` of that site's IT energy:

```
D_C(site) = s_site x 1,775 ML       D_W(site) = s_site x 2,477 ML
```

This gives **both** a consumption and a withdrawal footprint for the region, which
matters for impact-weighting (the impact layer weights withdrawal and consumption
differently by watershed).

**Missing data for the region-wise route:** per-site **IT energy** (the `s_site`
denominator is not published); the split between potable / non-potable / reclaimed
sources per site (only given for a few sites); and any sub-annual (seasonal)
breakdown. Without per-site energy, the site totals are ceilings, not allocations.

## Both flows

- **SWI-C:** consumption is reported at aggregate, DC/office, and per-location
  levels, plus the per-prompt figure — so `SWI-C` is well supported.
- **SWI-W:** **derivable** — Google reports withdrawal at the same three levels
  (2025 total 14,689 million US gal ≈ 55,600 ML; The Dalles 654.3 ≈ 2,477 ML).
  Both flows are blocked from per-workload attribution only by the missing
  IT-energy denominator, not by missing water data. Contrast AWS (withdrawal only,
  so no SWI-C) — Google, like Microsoft, supports both.

## Context metrics (not operational water)

From `csv/replenishment_and_progress.csv` — replenishment/offset, never netted
against `D`: 2025 replenishment ≈ 29,000 ML (7.7 billion US gal, 78% of freshwater
consumption); 120% ambition and > ~74,573 ML (19.7 billion US gal) target by 2030.

## Impact framework Google reports (context, not a calculation here)

- **Data centres:** Google's own **Water Risk Framework** (assesses scarcity and
  depletion; assigns low/medium/high) — a proprietary framework, not a public index.
- **Offices:** **WRI Aqueduct Water Risk Atlas + WWF Water Risk Filter**, adjusted
  for local context.

So Google mixes a proprietary framework (data centres) with public tools
(offices). None of these is a drop-in AWARE input; impact-weighting is deferred to
the impact layer.

## What you can / cannot say

- **Can:** "Using Google's median Gemini text-prompt figure (0.26 mL/prompt, 2025),
  ~10 M prompts consume ~2,600 L (SWI-C)." "Google's 2025 The Dalles site reports
  2,477 ML withdrawal and 1,775 ML consumption, so both SWI-W and SWI-C can be
  bounded for a workload located there."
- **Cannot:** attribute the corporate or site totals to a workload without Google's
  **per-site IT-energy** denominator; or treat the per-prompt figure as covering
  images/video or as a generic GCP factor.
