#!/usr/bin/env python3
"""Compare two authorized visual evidence files with an honest fallback."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reference", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--focal", help="optional focal ROI as x,y,width,height")
    args = parser.parse_args()
    for path in (args.reference, args.candidate):
        if not path.is_file():
            print(json.dumps({"error": f"File not found: {path}"}), file=sys.stderr)
            return 2
    args.output_dir.mkdir(parents=True, exist_ok=True)

    tool = shutil.which("compare") or shutil.which("magick")
    diff_path = args.output_dir / "visual-diff.png"
    pixel_diff = False
    command = None
    notes = []
    if tool:
        if Path(tool).name == "magick":
            command = [tool, "compare", "-metric", "AE", str(args.reference), str(args.candidate), str(diff_path)]
        else:
            command = [tool, "-metric", "AE", str(args.reference), str(args.candidate), str(diff_path)]
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        pixel_diff = diff_path.is_file()
        notes.append({"tool": tool, "metric": (result.stderr or result.stdout).strip(), "returncode": result.returncode})
    else:
        notes.append("ImageMagick compare/magick unavailable; only hashes and metadata were compared.")

    report = {
        "schema_version": 2,
        "tool": "compare_visual_evidence",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "reference": {"path": str(args.reference), "sha256": sha256(args.reference), "bytes": args.reference.stat().st_size},
        "candidate": {"path": str(args.candidate), "sha256": sha256(args.candidate), "bytes": args.candidate.stat().st_size},
        "same_bytes": sha256(args.reference) == sha256(args.candidate),
        "pixel_diff_available": pixel_diff,
        "diff_path": str(diff_path) if pixel_diff else None,
        "focal_roi": args.focal,
        "notes": notes,
        "limitations": [
            "A pixel diff does not explain whether a difference is intentional.",
            "Focal-moment review still requires a human or visual model to judge hierarchy, legibility and timing.",
        ],
    }
    output = args.output_dir / "visual-diff.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
