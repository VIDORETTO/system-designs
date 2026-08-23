#!/usr/bin/env python3
"""Extract representative video frames and a small provenance manifest.

Requires ffprobe and ffmpeg on PATH. It never uploads or embeds the source
video; the output is intended for local evidence review and report generation.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=False, capture_output=True, text=True)


def probe(video: Path) -> dict[str, Any]:
    result = run([
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration:stream=codec_name,width,height,avg_frame_rate",
        "-of", "json", str(video),
    ])
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "ffprobe failed")
    return json.loads(result.stdout or "{}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--count", type=int, default=6)
    parser.add_argument("--prefix", default="frame")
    args = parser.parse_args()

    if not args.video.is_file():
        print(json.dumps({"error": f"Video not found: {args.video}"}), file=sys.stderr)
        return 2
    if args.count < 1 or args.count > 60:
        print(json.dumps({"error": "--count must be between 1 and 60"}), file=sys.stderr)
        return 2
    missing = [tool for tool in ("ffprobe", "ffmpeg") if shutil.which(tool) is None]
    if missing:
        print(json.dumps({
            "error": "Required media tools are missing",
            "missing": missing,
            "next_step": "Install ffmpeg/ffprobe or provide screenshots/recording evidence instead.",
        }, indent=2), file=sys.stderr)
        return 3

    try:
        metadata = probe(args.video)
    except (OSError, RuntimeError, json.JSONDecodeError) as error:
        print(json.dumps({"error": str(error)}), file=sys.stderr)
        return 4

    duration = float((metadata.get("format") or {}).get("duration") or 0)
    if duration <= 0:
        print(json.dumps({"error": "Video duration is unavailable; no frames extracted."}), file=sys.stderr)
        return 5

    args.output_dir.mkdir(parents=True, exist_ok=True)
    fps = args.count / duration
    pattern = args.output_dir / f"{args.prefix}-%02d.jpg"
    result = run([
        "ffmpeg", "-y", "-v", "error", "-i", str(args.video),
        "-vf", f"fps={fps:.8f},scale=960:-2:force_original_aspect_ratio=decrease",
        "-frames:v", str(args.count), "-q:v", "3", str(pattern),
    ])
    if result.returncode != 0:
        print(json.dumps({"error": result.stderr.strip() or "ffmpeg failed"}), file=sys.stderr)
        return 6

    frames = sorted(path.name for path in args.output_dir.glob(f"{args.prefix}-*.jpg"))
    manifest = {
        "schema_version": 2,
        "tool": "extract_video_frames",
        "generated_at": now(),
        "source": str(args.video),
        "output_dir": str(args.output_dir),
        "requested_count": args.count,
        "frames": frames,
        "metadata": metadata,
        "basis": "computed",
        "confidence": "high",
        "notes": "Representative frames are evidence aids; they do not prove all playback states.",
    }
    (args.output_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
