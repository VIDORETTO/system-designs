#!/usr/bin/env python3
"""Validate an extracted design-system manifest using only the standard library."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


TOP_LEVEL = {
    "meta", "sources", "principles", "foundations", "responsive", "motion",
    "components", "patterns", "accessibility", "content_style", "exceptions",
    "gaps", "additional_findings", "generated_assets",
}
META_REQUIRED = {
    "name", "source_name", "generated_at", "scope", "fidelity_target",
    "overall_confidence", "method_summary",
}
FOUNDATION_GROUPS = {
    "colors", "typography", "spacing", "sizing", "grid", "radii", "borders",
    "shadows", "opacity", "z_index", "iconography", "imagery",
}
BASIS = {"observed", "computed", "inferred", "recommended"}
CONFIDENCE = {"high", "medium", "low"}
SOURCE_TYPES = {"live", "screenshot", "recording", "source", "design-file", "user-note"}
HEX_COLOR = re.compile(r"^#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")


def add(bucket: list[str], path: str, message: str) -> None:
    bucket.append(f"{path}: {message}")


def walk(value: Any, path: str = "$"):
    yield path, value
    if isinstance(value, dict):
        for key, child in value.items():
            yield from walk(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk(child, f"{path}[{index}]")


def validate(data: Any) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(data, dict):
        return ["$: root must be a JSON object"], warnings

    for key in sorted(TOP_LEVEL - set(data)):
        add(errors, "$", f"missing required top-level key '{key}'")
    for key in sorted(set(data) - TOP_LEVEL):
        add(warnings, "$", f"unknown top-level key '{key}'; consider additional_findings")

    meta = data.get("meta")
    if not isinstance(meta, dict):
        add(errors, "$.meta", "must be an object")
    else:
        for key in sorted(META_REQUIRED - set(meta)):
            add(errors, "$.meta", f"missing '{key}'")
        if meta.get("overall_confidence") not in CONFIDENCE:
            add(errors, "$.meta.overall_confidence", f"must be one of {sorted(CONFIDENCE)}")
        if not isinstance(meta.get("scope"), list) or not meta.get("scope"):
            add(warnings, "$.meta.scope", "should be a non-empty array")

    sources = data.get("sources")
    source_ids: set[str] = set()
    if not isinstance(sources, list):
        add(errors, "$.sources", "must be an array")
    else:
        if not sources:
            add(errors, "$.sources", "must contain at least one evidence source")
        for index, source in enumerate(sources):
            path = f"$.sources[{index}]"
            if not isinstance(source, dict):
                add(errors, path, "must be an object")
                continue
            for field in ("id", "source_type", "locator", "captured_at", "context", "limitations"):
                if field not in source:
                    add(errors, path, f"missing '{field}'")
            source_id = source.get("id")
            if isinstance(source_id, str):
                if source_id in source_ids:
                    add(errors, f"{path}.id", "duplicate evidence ID")
                source_ids.add(source_id)
            if source.get("source_type") not in SOURCE_TYPES:
                add(errors, f"{path}.source_type", f"must be one of {sorted(SOURCE_TYPES)}")

    foundations = data.get("foundations")
    if not isinstance(foundations, dict):
        add(errors, "$.foundations", "must be an object")
    else:
        for key in sorted(FOUNDATION_GROUPS - set(foundations)):
            add(warnings, "$.foundations", f"missing token family '{key}'")
        for key, value in foundations.items():
            if key in FOUNDATION_GROUPS and not isinstance(value, (list, dict)):
                add(errors, f"$.foundations.{key}", "must be an array or object")

    for path, value in walk(data):
        if not isinstance(value, dict):
            continue
        if "basis" in value and value["basis"] not in BASIS:
            add(errors, f"{path}.basis", f"must be one of {sorted(BASIS)}")
        if "confidence" in value and value["confidence"] not in CONFIDENCE:
            add(errors, f"{path}.confidence", f"must be one of {sorted(CONFIDENCE)}")
        evidence_ids = value.get("evidence_ids")
        if evidence_ids is not None:
            if not isinstance(evidence_ids, list) or not all(isinstance(x, str) for x in evidence_ids):
                add(errors, f"{path}.evidence_ids", "must be an array of strings")
            else:
                for source_id in evidence_ids:
                    if source_id not in source_ids:
                        add(errors, f"{path}.evidence_ids", f"unknown source ID '{source_id}'")
        looks_like_claim = any(k in value for k in ("token", "anatomy", "trigger", "label"))
        if looks_like_claim and path not in ("$.meta",):
            if "basis" not in value:
                add(warnings, path, "claim-like item has no basis")
            if "confidence" not in value:
                add(warnings, path, "claim-like item has no confidence")
        token = value.get("token")
        raw_value = value.get("value")
        if isinstance(token, str) and token.startswith("color.") and isinstance(raw_value, str):
            if raw_value.startswith("#") and not HEX_COLOR.match(raw_value):
                add(errors, f"{path}.value", "invalid hexadecimal color")

    if isinstance(sources, list):
        viewports = {
            str(s.get("context", {}).get("viewport"))
            for s in sources if isinstance(s, dict) and isinstance(s.get("context"), dict)
            and s.get("context", {}).get("viewport")
        }
        if len(viewports) < 2:
            gaps = " ".join(map(str, data.get("gaps", []))).lower()
            if "viewport" not in gaps and "mobile" not in gaps and "responsive" not in gaps:
                add(warnings, "$.sources", "fewer than two viewports and no responsive limitation in gaps")

    colors = foundations.get("colors", []) if isinstance(foundations, dict) else []
    if not colors:
        add(warnings, "$.foundations.colors", "no color tokens found")
    if not data.get("components"):
        add(warnings, "$.components", "no components documented")
    motion = data.get("motion")
    has_motion_patterns = isinstance(motion, dict) and bool(motion.get("patterns"))
    if not has_motion_patterns:
        add(warnings, "$.motion", "no motion patterns; document the evidence gap if unavailable")

    return errors, warnings


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_design_system.py DESIGN_SYSTEM.json", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}", file=sys.stderr)
        return 1

    errors, warnings = validate(data)
    for item in errors:
        print(f"ERROR {item}")
    for item in warnings:
        print(f"WARN  {item}")
    print(f"Summary: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
