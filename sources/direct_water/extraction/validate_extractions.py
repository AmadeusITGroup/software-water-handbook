"""Validate every extraction JSON against the extraction schema.

Usage (from the repository, no arguments needed):

    python validate_extractions.py

It finds schema.json (in ../schema.json relative to this file), then validates
every *.json under ../extractions/ and prints a pass/fail summary.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError:
    sys.exit("Please install jsonschema: pip install jsonschema")


HERE = Path(__file__).resolve().parent
DIRECT_WATER = HERE.parent
SCHEMA_PATH = DIRECT_WATER / "schema.json"


def main() -> int:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)

    # Extraction JSON lives under each company's json/ folder: <company>/json/*.json
    json_files = sorted(DIRECT_WATER.glob("*/json/*.json"))
    if not json_files:
        print(f"No extraction JSON found under {DIRECT_WATER}/*/json/")
        return 0

    failures = 0
    for path in json_files:
        rel = path.relative_to(DIRECT_WATER)
        try:
            instance = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print(f"FAIL  {rel}  (invalid JSON: {exc})")
            failures += 1
            continue

        errors = sorted(validator.iter_errors(instance), key=lambda e: e.path)
        if errors:
            failures += 1
            print(f"FAIL  {rel}  ({len(errors)} error(s))")
            for err in errors[:10]:
                location = "/".join(str(p) for p in err.path) or "<root>"
                print(f"      - {location}: {err.message}")
        else:
            n_obs = len(instance.get("observations", []))
            print(f"PASS  {rel}  ({n_obs} observation(s))")

    print()
    print(f"{len(json_files) - failures}/{len(json_files)} files valid")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
