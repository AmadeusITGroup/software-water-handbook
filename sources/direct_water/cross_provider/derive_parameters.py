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
        "caveat", "source_report_id", "source_url",
    ]),
    "per_unit": ("per_unit_water.csv", [
        "provider", "service_applicability", "region", "period",
        "value", "reported_unit", "value_liters", "denominator",
        "value_qualifier", "water_flow", "caveat", "source_report_id", "source_url",
    ]),
    "volumes": ("water_volumes.csv", [
        "provider", "scope", "geographic_resolution", "location", "country",
        "period", "water_flow", "value", "reported_unit", "value_liters",
        "value_qualifier", "caveat", "source_report_id", "source_url",
    ]),
    "shares": ("water_shares.csv", [
        "provider", "scope", "location", "period", "metric", "water_flow",
        "percent", "value_qualifier", "caveat", "source_report_id", "source_url",
    ]),
    "progress": ("replenishment_and_progress.csv", [
        "provider", "scope", "location", "period", "metric", "category",
        "water_flow", "value", "reported_unit", "value_liters", "value_qualifier",
        "caveat", "source_report_id", "source_url",
    ]),
}

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


def main() -> None:
    combined: dict[str, list[dict]] = {t: [] for t in THEMES}

    for company_dir in sorted(p for p in DIRECT_WATER.iterdir() if (p / "json").is_dir()):
        company = company_dir.name
        by_theme: dict[str, list[dict]] = {t: [] for t in THEMES}
        for jf in sorted((company_dir / "json").glob("*.json")):
            for theme, row in rows_from_file(jf):
                by_theme[theme].append(row)
        for theme, rows in by_theme.items():
            if not rows:
                continue
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


if __name__ == "__main__":
    main()
