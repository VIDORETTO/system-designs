#!/usr/bin/env python3
"""Compare browser captures against an authorized visual baseline directory."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def compare_with_pillow(reference: Path, candidate: Path, diff_path: Path) -> dict[str, Any]:
    try:
        from PIL import Image, ImageChops
    except ImportError:
        return {"available": False, "reason": "Pillow is not installed"}
    reference_image = Image.open(reference).convert("RGBA")
    candidate_image = Image.open(candidate).convert("RGBA")
    if reference_image.size != candidate_image.size:
        return {
            "available": True,
            "same_dimensions": False,
            "reference_size": reference_image.size,
            "candidate_size": candidate_image.size,
            "different_pixels": None,
            "ratio": 1.0,
        }
    difference = ImageChops.difference(reference_image, candidate_image)
    bbox = difference.getbbox()
    if bbox is None:
        different_pixels = 0
        ratio = 0.0
    else:
        pixels = list(difference.getdata())
        different_pixels = sum(1 for pixel in pixels if pixel != (0, 0, 0, 0))
        ratio = different_pixels / max(1, len(pixels))
        diff_path.parent.mkdir(parents=True, exist_ok=True)
        difference.save(diff_path)
    return {
        "available": True,
        "same_dimensions": True,
        "reference_size": reference_image.size,
        "candidate_size": candidate_image.size,
        "different_pixels": different_pixels,
        "ratio": round(ratio, 8),
        "diff_path": str(diff_path) if bbox is not None else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("baseline_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--allow-missing-baseline", action="store_true")
    parser.add_argument("--max-ratio", type=float, default=0.01)
    args = parser.parse_args()
    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, Any]] = []
    failures: list[str] = []
    missing: list[str] = []
    for capture in data.get("captures") or []:
        filename = str(capture.get("screenshot") or "")
        candidate = args.manifest.parent / filename
        reference = args.baseline_dir / filename
        if not reference.is_file():
            missing.append(filename)
            results.append({"screenshot": filename, "status": "baseline-missing"})
            continue
        if not candidate.is_file():
            failures.append(filename + ": candidate screenshot missing")
            continue
        result = compare_with_pillow(reference, candidate, args.output_dir / (filename + ".diff.png"))
        result.update({
            "screenshot": filename,
            "reference_sha256": digest(reference),
            "candidate_sha256": digest(candidate),
        })
        if result.get("available") is False:
            failures.append(filename + ": no pixel comparison backend")
            result["status"] = "unavailable"
        elif result.get("ratio", 1.0) > args.max_ratio:
            failures.append(filename + ": pixel difference ratio exceeds threshold")
            result["status"] = "changed"
        else:
            result["status"] = "pass"
        results.append(result)

    report = {
        "schema_version": 2,
        "tool": "run_visual_regression",
        "manifest": str(args.manifest),
        "baseline_dir": str(args.baseline_dir),
        "max_ratio": args.max_ratio,
        "missing_baselines": missing,
        "results": results,
        "status": "baseline-pending" if missing and not failures else ("fail" if failures else "pass"),
        "limitations": [
            "A pixel delta detects change, not whether the change is desirable.",
            "Focal-moment review still needs a human or visual model.",
        ],
    }
    (args.output_dir / "visual-regression.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if failures or (missing and not args.allow_missing_baseline):
        for item in failures:
            print("ERROR " + item, file=sys.stderr)
        for item in missing:
            print("ERROR baseline missing: " + item, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
