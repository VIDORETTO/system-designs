#!/usr/bin/env python3
"""Export a manifest to DESIGN.md plus a media/evidence sidecar."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def scalar(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def bullets(items: Any) -> str:
    if not items:
        return "- None recorded"
    if isinstance(items, list):
        return "\n".join(f"- {scalar(item)}" for item in items)
    return f"- {scalar(items)}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    meta = data.get("meta") or {}
    experience = data.get("experience") or {}
    identity = experience.get("identity_lock") or {}
    focal = experience.get("focal_moment") or {}
    media = data.get("media") or {}
    assets = media.get("assets") if isinstance(media, dict) else []
    lines = [
        f"# {meta.get('name', 'Design system')}",
        "",
        f"> Generated {datetime.now(timezone.utc).replace(microsecond=0).isoformat()} from {args.manifest}.",
        "",
        "## Identity lock",
        "",
        identity.get("summary") or identity.get("thesis") or "No identity lock recorded.",
        "",
        "## Focal moment",
        "",
        focal.get("description") or focal.get("name") or "No focal moment recorded.",
        "",
        "## Signature rules",
        "",
        bullets(experience.get("named_rules")),
        "",
        "## Foundations",
        "",
        bullets([f"{key}: {scalar(value)}" for key, value in (data.get("foundations") or {}).items()]),
        "",
        "## Motion",
        "",
        bullets([item.get("name") or item.get("id") for item in (data.get("motion") or {}).get("patterns", [])]),
        "",
        "## Accessibility",
        "",
        bullets((data.get("accessibility") or {}).items()),
        "",
        "## Evidence and gaps",
        "",
        bullets(data.get("gaps")),
    ]
    (args.output_dir / "DESIGN.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    sidecar = {
        "schema_version": 2,
        "source_manifest": str(args.manifest),
        "media_assets": assets,
        "generated_assets": data.get("generated_assets") or {},
        "sources": data.get("sources") or [],
    }
    (args.output_dir / "media.sidecar.json").write_text(json.dumps(sidecar, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"design": str(args.output_dir / "DESIGN.md"), "sidecar": str(args.output_dir / "media.sidecar.json")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
