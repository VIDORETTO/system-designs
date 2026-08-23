#!/usr/bin/env python3
"""Run documentation anti-pattern checks on a manifest."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def walk(value: Any, path: str = "$"):
    yield path, value
    if isinstance(value, dict):
        for key, child in value.items():
            yield from walk(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk(child, f"{path}[{index}]")


def audit(data: dict[str, Any]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    meta = data.get("meta") or {}
    if meta.get("schema_version", 1) >= 2 and not data.get("experience"):
        findings.append({"severity": "P2", "path": "$.experience", "message": "v2 manifest has no Experience Layer"})
    for path, item in walk(data):
        if not isinstance(item, dict):
            continue
        if item.get("basis") == "recommended" and item.get("evidence_ids"):
            findings.append({"severity": "P2", "path": path, "message": "recommended claim carries source evidence; separate rationale from observation"})
        if item.get("driver") in {"scroll", "pointer"} and not (item.get("fallback") or item.get("reduced_motion")):
            findings.append({"severity": "P1", "path": path, "message": "interactive effect/motion has no fallback"})
        if item.get("kind") == "video" and item.get("role") in {"hero-background", "ambient-background"}:
            playback = item.get("playback") or {}
            fallback = item.get("fallback") or {}
            if playback.get("autoplay") and not (fallback.get("poster") or fallback.get("reduced_motion")):
                findings.append({"severity": "P1", "path": path, "message": "autoplay background video has no static/reduced fallback"})
            if not item.get("composition"):
                findings.append({"severity": "P2", "path": path, "message": "background video lacks crop/layer/text-safe composition"})
        if item.get("interaction") and isinstance(item.get("states"), list) and "focus-visible" not in item["states"]:
            findings.append({"severity": "P2", "path": path, "message": "interactive component omits focus-visible state"})
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    findings = audit(data)
    for finding in findings:
        print(f"{finding['severity']} {finding['path']}: {finding['message']}")
    print(f"Summary: {len(findings)} anti-pattern finding(s)")
    return 1 if any(item["severity"] in {"P0", "P1"} for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
