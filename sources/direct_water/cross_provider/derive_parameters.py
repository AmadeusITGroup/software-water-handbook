"""Derive themed, computation-ready parameter tables from the JSON extractions.

For every <company>/json/*.json it produces themed CSVs, routed by metric family:

  - wue.csv                      water_intensity (WUE, L/kWh)
  - water_volumes.csv            water_volume (withdrawal/consumption/discharge)
  - water_shares.csv             water_share (percentages)
  - replenishment_and_progress.csv   water_replenishment / avoided_water / water_positive_progress

Outputs are written both per company (<company>/csv/<theme>.csv) and combined
(cross_provider/<theme>_all_providers.csv). Every row carries units, the
consumption/withdrawal flag, a caveat, and a source_report_id back-reference.

Run from this directory:  python derive_parameters.py
"""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
DIRECT_WATER = HERE.parent

# theme -> (filename, fieldnames)
ENERGY_DENOMINATORS = {
    "it_equipment_energy", "it_load_energy", "server_energy",
    "facility_energy", "allocated_customer_energy",
}

THEMES = {
    "wue": ("wue.csv", [
        "provider", "service_applicability", "region", "period",
        "wue_l_per_kwh", "value_qualifier", "water_flow", "denominator",
        "caveat", "source_report_id", "source_url", "report_year",
    ]),
    "per_unit": ("per_unit_water.csv", [
        "provider", "service_applicability", "region", "period",
        "value", "reported_unit", "value_liters", "denominator",
        "value_qualifier", "water_flow", "caveat", "source_report_id", "source_url", "report_year",
    ]),
    "volumes": ("water_volumes.csv", [
        "provider", "scope", "geographic_resolution", "location", "country",
        "period", "water_flow", "value", "reported_unit", "value_liters",
        "value_qualifier", "caveat", "source_report_id", "source_url", "report_year",
    ]),
    "shares": ("water_shares.csv", [
        "provider", "scope", "location", "period", "metric", "water_flow",
        "percent", "value_qualifier", "caveat", "source_report_id", "source_url", "report_year",
    ]),
    "progress": ("replenishment_and_progress.csv", [
        "provider", "scope", "location", "period", "metric", "category",
        "water_flow", "value", "reported_unit", "value_liters", "value_qualifier",
        "caveat", "source_report_id", "source_url", "report_year",
    ]),
}

# Columns that are NOT part of a row's identity. Two rows that match on every OTHER
# column describe "the same thing"; if their value differs it is a restatement.
PRIMARY_VALUE = {"wue": "wue_l_per_kwh", "per_unit": "value",
                 "volumes": "value", "shares": "percent", "progress": "value"}
NON_KEY_COLS = {"value", "wue_l_per_kwh", "percent", "value_liters",
                "value_qualifier", "caveat", "source_report_id", "source_url", "report_year"}
RESTATE_FIELDS = ["theme", "provider", "period", "identity", "water_flow",
                  "superseded_value", "superseded_report", "superseded_year",
                  "kept_value", "kept_report", "kept_year"]

FAMILY_TO_THEME = {
    "water_intensity": "wue",
    "water_volume": "volumes",
    "water_share": "shares",
    "water_replenishment": "progress",
    "avoided_water": "progress",
    "water_positive_progress": "progress",
}


def pick_value(val: dict):
    """Return (display_value, normalized_liters) from a value package."""
    for v_key, n_key in (("value", "normalized_value"),
                          ("value_low", "normalized_value_low"),
                          ("value_high", "normalized_value_high")):
        if val.get(v_key) is not None:
            return val[v_key], val.get(n_key)
    return None, None


def caveat_for(scope: dict, obs: dict) -> str:
    bits = list(scope.get("exclusions", []) or [])
    bits += (obs.get("quality", {}) or {}).get("caveats", []) or []
    return "; ".join(dict.fromkeys(bits))


def rows_from_file(path: Path):
    """Yield (theme, row_dict) for every observation with a usable value."""
    doc = json.loads(path.read_text(encoding="utf-8"))
    rep = doc["report"]
    metrics = {m["metric_definition_id"]: m for m in doc["definitions"]["metric_definitions"]}
    scopes = {s["scope_definition_id"]: s for s in doc["definitions"]["scope_definitions"]}

    for obs in doc.get("observations", []):
        md = metrics.get(obs["metric_definition_id"], {})
        theme = FAMILY_TO_THEME.get(md.get("metric_family"))
        if theme is None:
            continue
        val = obs.get("value", {})
        display, liters = pick_value(val)
        if display is None and val.get("value_status") not in ("below_reporting_threshold",):
            continue

        geo = obs.get("geography", {})
        scope = scopes.get(obs["scope_definition_id"], {})
        flow = obs["water_boundary"]["accounting_flow"]
        common = {
            "provider": rep["reporting_entity"],
            "period": obs["period"]["period_label"],
            "water_flow": flow,
            "value_qualifier": val.get("value_qualifier", ""),
            "caveat": caveat_for(scope, obs),
            "source_report_id": rep["report_id"],
            "source_url": rep["source_url"],
            "report_year": rep.get("publication_year") or rep.get("report_year") or "",
        }

        if theme == "wue":
            denom = obs.get("denominator") or {}
            denom_q = denom.get("denominator_quantity", "it_equipment_energy")
            if denom_q in ENERGY_DENOMINATORS:
                # Energy-denominated WUE (L/kWh). Use the normalized L/kWh value.
                yield "wue", {
                    **common,
                    "service_applicability": scope.get("scope_name", ""),
                    "region": geo.get("geography_name", ""),
                    "wue_l_per_kwh": val.get("normalized_value", display),
                    "denominator": denom_q,
                }
            else:
                # Per-unit intensity (e.g. per prompt / per response) — different denominator.
                yield "per_unit", {
                    **common,
                    "service_applicability": scope.get("scope_name", ""),
                    "region": geo.get("geography_name", ""),
                    "value": display,
                    "reported_unit": val.get("reported_unit", ""),
                    "value_liters": liters,
                    "denominator": denom_q,
                }
        elif theme == "volumes":
            yield theme, {
                **common,
                "scope": scope.get("scope_name", ""),
                "geographic_resolution": geo.get("geographic_resolution", ""),
                "location": geo.get("geography_name", ""),
                "country": geo.get("country_code", ""),
                "value": display,
                "reported_unit": val.get("reported_unit", ""),
                "value_liters": liters,
            }
        elif theme == "shares":
            yield theme, {
                **common,
                "scope": scope.get("scope_name", ""),
                "location": geo.get("geography_name", ""),
                "metric": md.get("metric_name", ""),
                "percent": display,
            }
        elif theme == "progress":
            yield theme, {
                **common,
                "scope": scope.get("scope_name", ""),
                "location": geo.get("geography_name", ""),
                "metric": md.get("metric_name", ""),
                "category": md.get("metric_family", ""),
                "value": display,
                "reported_unit": val.get("reported_unit", ""),
                "value_liters": liters,
            }


def write_csv(path: Path, theme: str, rows: list[dict]) -> None:
    _, fields = THEMES[theme]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _year(row: dict) -> int:
    try:
        return int(row.get("report_year") or 0)
    except (TypeError, ValueError):
        return 0


def _identity(theme: str, row: dict) -> tuple:
    """Semantic key: all identifying columns except value/metadata.
    Two rows with the same identity describe the same fact."""
    fields = THEMES[theme][1]
    return tuple((f, row.get(f, "")) for f in fields if f not in NON_KEY_COLS)


def dedupe_latest(theme: str, rows: list[dict]):
    """Keep one row per identity, choosing the latest report edition.

    Rule: complementary rows (different identity) are all kept; rows that report
    the *same* fact (same identity) collapse to the value from the most recent
    report (highest report_year). Value disagreements across editions are logged
    as restatements.
    """
    prim = PRIMARY_VALUE[theme]
    groups: dict[tuple, list[dict]] = {}
    order: list[tuple] = []
    for r in rows:
        k = _identity(theme, r)
        if k not in groups:
            groups[k] = []
            order.append(k)
        groups[k].append(r)

    kept, restatements = [], []
    for k in order:
        group = groups[k]
        if len(group) == 1:
            kept.append(group[0])
            continue
        # Guard: if a single report contributes >1 row to this identity, the CSV
        # columns do not fully identify the fact (e.g. low/med/high risk shares, or
        # two avoided-water sub-metrics). Such rows are distinct, not duplicates —
        # keep them all and do NOT dedupe. Only collapse identities that appear at
        # most once per report but across multiple editions.
        per_report = Counter(r.get("source_report_id") for r in group)
        if any(c > 1 for c in per_report.values()) or len(per_report) < 2:
            kept.extend(group)
            continue
        winner = sorted(group, key=_year)[-1]  # latest edition (stable for ties)
        kept.append(winner)
        for r in group:
            if r is winner:
                continue
            if str(r.get(prim)) != str(winner.get(prim)):  # value changed => restatement
                restatements.append({
                    "theme": theme, "provider": r.get("provider", ""),
                    "period": r.get("period", ""),
                    "identity": r.get("location") or r.get("region") or r.get("scope") or "",
                    "water_flow": r.get("water_flow", ""),
                    "superseded_value": r.get(prim), "superseded_report": r.get("source_report_id"),
                    "superseded_year": r.get("report_year"),
                    "kept_value": winner.get(prim), "kept_report": winner.get("source_report_id"),
                    "kept_year": winner.get("report_year"),
                })
    return kept, restatements


def main() -> None:
    combined: dict[str, list[dict]] = {t: [] for t in THEMES}
    all_restatements: list[dict] = []

    for company_dir in sorted(p for p in DIRECT_WATER.iterdir() if (p / "json").is_dir()):
        company = company_dir.name
        by_theme: dict[str, list[dict]] = {t: [] for t in THEMES}
        for jf in sorted((company_dir / "json").glob("*.json")):
            for theme, row in rows_from_file(jf):
                by_theme[theme].append(row)
        for theme, rows in by_theme.items():
            if not rows:
                continue
            # Latest-per-key: same fact across editions -> keep newest; log restatements.
            rows, restates = dedupe_latest(theme, rows)
            all_restatements.extend(restates)
            rows.sort(key=lambda r: (str(r.get("location") or r.get("region", "")), str(r["period"])))
            write_csv(company_dir / "csv" / THEMES[theme][0], theme, rows)
            combined[theme].extend(rows)
        made = [THEMES[t][0] for t in THEMES if by_theme[t]]
        print(f"{company}: {', '.join(made)}")

    for theme, rows in combined.items():
        if not rows:
            continue
        rows.sort(key=lambda r: (r["provider"], str(r.get("location") or r.get("region", "")), str(r["period"])))
        combined_name = THEMES[theme][0].replace(".csv", "_all_providers.csv")
        write_csv(HERE / combined_name, theme, rows)
        print(f"combined: {len(rows):>4} rows -> cross_provider/{combined_name}")

    # Restatements log: same fact reported with different values across editions.
    restate_path = HERE / "restatements.csv"
    with restate_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=RESTATE_FIELDS)
        writer.writeheader()
        writer.writerows(sorted(all_restatements, key=lambda r: (r["provider"], r["theme"], str(r["period"]))))
    print(f"restatements: {len(all_restatements)} -> cross_provider/restatements.csv")


if __name__ == "__main__":
    main()
