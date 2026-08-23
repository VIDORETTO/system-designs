#!/usr/bin/env python3
"""Small regression runner for schema validation and report rendering."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_manifest(path: Path, validator, renderer) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    errors, warnings, issues = validator.validate(data)
    failures = [f"{path}: {item}" for item in errors]
    failures.extend(
        f"{path}: {issue['severity']} {issue['path']}: {issue['message']}"
        for issue in issues
        if issue["severity"] in {"P0", "P1"}
    )
    rendered = renderer.render(data, str(path))
    required_markers = (
        "Experience layer",
        "media",
        "motion",
        "prefers-reduced-motion",
        "evidence",
    )
    failures.extend(f"{path}: report missing marker '{marker}'" for marker in required_markers if marker not in rendered)
    print(f"{path}: {len(errors)} errors, {len(warnings)} warnings, {len(issues)} quality issues")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "manifest",
        nargs="*",
        type=Path,
        help="manifest paths; defaults to the media fixture",
    )
    args = parser.parse_args()
    manifests = args.manifest or [ROOT / "templates/media/experience-layer/design-system.json"]
    validator = load_module("design_system_validator", ROOT / "skill/scripts/validate_design_system.py")
    renderer = load_module("design_system_renderer", ROOT / "skill/scripts/render_design_system_report.py")
    failures: list[str] = []
    for manifest in manifests:
        if not manifest.is_absolute():
            manifest = Path.cwd() / manifest
        if not manifest.is_file():
            failures.append(f"{manifest}: file not found")
            continue
        failures.extend(check_manifest(manifest, validator, renderer))
    if failures:
        for failure in failures:
            print(f"FAIL {failure}", file=sys.stderr)
        return 1
    print("PASS design-system regression checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
