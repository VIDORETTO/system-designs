#!/usr/bin/env python3
"""Score extraction coverage across one or more manifests."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


MATERIAL_KEYS = {"token", "id", "name", "label", "statement", "thesis", "kind", "driver"}


def walk(value: Any):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def score(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    claims = [item for item in walk(data) if isinstance(item, dict) and MATERIAL_KEYS.intersection(item)]
    with_basis = [item for item in claims if item.get("basis")]
    with_evidence = [item for item in claims if item.get("evidence_ids")]
    sections = ("experience", "foundations", "responsive", "motion", "components", "media", "effects", "accessibility", "patterns")
    present = [section for section in sections if data.get(section)]
    return {
        "manifest": str(path),
        "schema_version": (data.get("meta") or {}).get("schema_version", 1),
        "claims": len(claims),
        "basis_coverage": round(len(with_basis) / len(claims), 3) if claims else 0,
        "evidence_coverage": round(len(with_evidence) / len(claims), 3) if claims else 0,
        "sections_present": present,
        "section_coverage": round(len(present) / len(sections), 3),
        "media_assets": len((data.get("media") or {}).get("assets", [])) if isinstance(data.get("media"), dict) else 0,
        "motion_patterns": len((data.get("motion") or {}).get("patterns", [])) if isinstance(data.get("motion"), dict) else 0,
        "gaps": len(data.get("gaps") or []),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", nargs="*", type=Path)
    parser.add_argument("--corpus", type=Path, help="representative-corpus.json")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    manifests = list(args.manifest)
    if args.corpus:
        corpus = json.loads(args.corpus.read_text(encoding="utf-8"))
        manifests.extend(Path(item["manifest"]) for item in corpus.get("manifests", []) if item.get("manifest"))
    if not manifests:
        parser.error("provide at least one manifest or --corpus")
    result = {"schema_version": 2, "manifests": [score(path) for path in manifests]}
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
