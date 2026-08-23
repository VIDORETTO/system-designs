#!/usr/bin/env python3
"""Validate browser capture coverage and runtime probe output."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def add(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--strict-request-failures", action="store_true")
    args = parser.parse_args()
    data: dict[str, Any] = json.loads(args.manifest.read_text(encoding="utf-8"))
    captures = data.get("captures") or []
    errors: list[str] = []
    if not captures:
        add(errors, "manifest has no captures")

    groups: dict[tuple[str, int, int], set[bool]] = {}
    for index, capture in enumerate(captures):
        path = f"captures[{index}]"
        if capture.get("error"):
            add(errors, f"{path}: {capture['error']}")
            continue
        for field in ("id", "url", "viewport", "screenshot", "probe"):
            if not capture.get(field):
                add(errors, f"{path}: missing {field}")
        viewport = capture.get("viewport") or {}
        width = int(viewport.get("width") or 0)
        height = int(viewport.get("height") or 0)
        if width < 240 or height < 240:
            add(errors, f"{path}: invalid viewport {width}x{height}")
        screenshot = args.manifest.parent / str(capture.get("screenshot") or "")
        if not screenshot.is_file() or screenshot.stat().st_size == 0:
            add(errors, f"{path}: screenshot missing or empty: {screenshot}")
        probe = capture.get("probe") or {}
        if not (probe.get("meta") or {}).get("tool") == "runtime_media_probe":
            add(errors, f"{path}: runtime media probe result missing")
        page = capture.get("page") or {}
        if not page.get("title"):
            add(errors, f"{path}: page title missing")
        key = (str(capture.get("target")), width, height)
        groups.setdefault(key, set()).add(bool(capture.get("reduced_motion")))
        if args.strict_request_failures and capture.get("request_failures"):
            add(errors, f"{path}: request failures present")

    for key, states in groups.items():
        if states != {False, True}:
            add(errors, f"{key}: expected normal and reduced-motion captures")

    summary = {
        "captures": len(captures),
        "coverage_groups": len(groups),
        "errors": len(errors),
        "page_errors": sum(len(item.get("page_errors") or []) for item in captures),
        "request_failures": sum(len(item.get("request_failures") or []) for item in captures),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    for error in errors:
        print("ERROR " + error, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
