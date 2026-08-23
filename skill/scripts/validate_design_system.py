#!/usr/bin/env python3
"""Validate an extracted web design-system manifest using only the standard library."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


TOP_LEVEL = {
    "meta",
    "sources",
    "principles",
    "experience",
    "foundations",
    "responsive",
    "motion",
    "components",
    "elements",
    "media",
    "effects",
    "patterns",
    "accessibility",
    "content_style",
    "exceptions",
    "gaps",
    "additional_findings",
    "generated_assets",
}
META_REQUIRED = {
    "name",
    "source_name",
    "generated_at",
    "scope",
    "fidelity_target",
    "overall_confidence",
    "method_summary",
}
FOUNDATION_GROUPS = {
    "colors",
    "typography",
    "spacing",
    "sizing",
    "grid",
    "radii",
    "borders",
    "shadows",
    "opacity",
    "z_index",
    "iconography",
    "imagery",
}
BASIS = {"observed", "computed", "inferred", "recommended"}
CONFIDENCE = {"high", "medium", "low"}
SOURCE_TYPES = {"live", "screenshot", "recording", "source", "design-file", "user-note"}
SURFACE_MODES = {"persuade", "operate", "read", "experience"}
MEDIA_KINDS = {"image", "video", "audio", "canvas", "svg", "lottie", "shader", "iframe", "texture", "unknown"}
MEDIA_ROLES = {
    "hero-background",
    "ambient-background",
    "content",
    "decorative",
    "product-demo",
    "brand-mark",
    "icon",
    "illustration",
    "texture",
    "unknown",
}
EFFECT_DRIVERS = {"time", "scroll", "pointer", "gesture", "state", "load", "unknown"}
MOTION_DRIVERS = {"time", "scroll", "pointer", "gesture", "state", "load", "unknown"}
MOTION_JOBS = {"feedback", "continuity", "hierarchy", "atmosphere", "navigation", "state", "delight", "unknown"}
HEX_COLOR = re.compile(r"^#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")
SEVERITIES = {"P0", "P1", "P2", "P3"}


def add(bucket: list[str], path: str, message: str) -> None:
    bucket.append(f"{path}: {message}")


def add_issue(issues: list[dict[str, str]], severity: str, path: str, message: str) -> None:
    issues.append({"severity": severity, "path": path, "message": message})


def seq(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        return [{"token": key, "value": item} for key, item in value.items()]
    return []


def walk(value: Any, path: str = "$"):
    yield path, value
    if isinstance(value, dict):
        for key, child in value.items():
            yield from walk(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk(child, f"{path}[{index}]")


def validate_claim_fields(
    value: dict[str, Any],
    path: str,
    source_ids: set[str],
    errors: list[str],
    warnings: list[str],
) -> None:
    if "basis" in value and value["basis"] not in BASIS:
        add(errors, f"{path}.basis", f"must be one of {sorted(BASIS)}")
    if "confidence" in value and value["confidence"] not in CONFIDENCE:
        add(errors, f"{path}.confidence", f"must be one of {sorted(CONFIDENCE)}")
    evidence_ids = value.get("evidence_ids")
    if evidence_ids is not None:
        if not isinstance(evidence_ids, list) or not all(isinstance(item, str) for item in evidence_ids):
            add(errors, f"{path}.evidence_ids", "must be an array of strings")
        else:
            for source_id in evidence_ids:
                if source_id not in source_ids:
                    add(errors, f"{path}.evidence_ids", f"unknown source ID '{source_id}'")
    looks_like_claim = any(key in value for key in ("token", "anatomy", "trigger", "statement"))
    if looks_like_claim:
        if "basis" not in value:
            add(warnings, path, "claim-like item has no basis")
        if "confidence" not in value:
            add(warnings, path, "claim-like item has no confidence")


def validate_experience(
    experience: Any,
    source_ids: set[str],
    errors: list[str],
    warnings: list[str],
    issues: list[dict[str, str]],
) -> None:
    if experience is None:
        return
    if not isinstance(experience, dict):
        add(errors, "$.experience", "must be an object")
        return
    mode = experience.get("surface_mode")
    if mode is not None and mode not in SURFACE_MODES:
        add(errors, "$.experience.surface_mode", f"must be one of {sorted(SURFACE_MODES)}")
    identity = experience.get("identity_lock")
    if identity is not None:
        if not isinstance(identity, dict):
            add(errors, "$.experience.identity_lock", "must be an object")
        else:
            validate_claim_fields(identity, "$.experience.identity_lock", source_ids, errors, warnings)
            if not identity.get("summary"):
                add_issue(issues, "P2", "$.experience.identity_lock", "identity lock has no summary")
    focal = experience.get("focal_moment")
    if focal is not None:
        if not isinstance(focal, dict):
            add(errors, "$.experience.focal_moment", "must be an object")
        else:
            validate_claim_fields(focal, "$.experience.focal_moment", source_ids, errors, warnings)
    for key in ("signature_elements", "named_rules", "dos", "donts", "recommendations"):
        value = experience.get(key)
        if value is not None and not isinstance(value, list):
            add(errors, f"$.experience.{key}", "must be an array")


def validate_elements(
    elements: Any,
    source_ids: set[str],
    errors: list[str],
    warnings: list[str],
    issues: list[dict[str, str]],
) -> None:
    if elements is None:
        return
    if not isinstance(elements, list):
        add(errors, "$.elements", "must be an array")
        return
    for index, element in enumerate(elements):
        path = f"$.elements[{index}]"
        if not isinstance(element, dict):
            add(errors, path, "must be an object")
            continue
        validate_claim_fields(element, path, source_ids, errors, warnings)
        for field in ("id", "kind", "role"):
            if not element.get(field):
                add(warnings, path, f"missing '{field}'")
        if not element.get("anatomy") and not element.get("material"):
            add_issue(issues, "P2", path, "signature element lacks anatomy or material description")


def media_assets(media: Any) -> list[Any]:
    if isinstance(media, dict):
        assets = media.get("assets", [])
        return assets if isinstance(assets, list) else []
    if isinstance(media, list):
        return media
    return []


def validate_media(
    media: Any,
    source_ids: set[str],
    errors: list[str],
    warnings: list[str],
    issues: list[dict[str, str]],
) -> None:
    if media is None:
        return
    if not isinstance(media, (dict, list)):
        add(errors, "$.media", "must be an object with assets or an array")
        return
    assets = media_assets(media)
    for index, asset in enumerate(assets):
        path = f"$.media.assets[{index}]"
        if not isinstance(asset, dict):
            add(errors, path, "must be an object")
            continue
        validate_claim_fields(asset, path, source_ids, errors, warnings)
        for field in ("id", "kind", "role"):
            if not asset.get(field):
                add(warnings, path, f"missing '{field}'")
        kind = asset.get("kind")
        role = asset.get("role")
        if kind not in MEDIA_KINDS:
            add(errors, f"{path}.kind", f"must be one of {sorted(MEDIA_KINDS)}")
        if role not in MEDIA_ROLES:
            add(errors, f"{path}.role", f"must be one of {sorted(MEDIA_ROLES)}")
        playback = asset.get("playback") if isinstance(asset.get("playback"), dict) else {}
        fallback = asset.get("fallback") if isinstance(asset.get("fallback"), dict) else {}
        performance = asset.get("performance") if isinstance(asset.get("performance"), dict) else {}
        if kind == "video" and playback.get("autoplay") is True:
            if playback.get("muted") is not True:
                add_issue(issues, "P1", f"{path}.playback", "autoplay video should be muted")
            if playback.get("playsinline") is not True:
                add_issue(issues, "P1", f"{path}.playback", "autoplay video should declare playsinline")
            if not fallback.get("poster") and not fallback.get("reduced_motion"):
                add_issue(issues, "P1", f"{path}.fallback", "autoplay video has no poster or reduced-motion fallback")
            if not performance.get("offscreen"):
                add_issue(issues, "P2", f"{path}.performance", "autoplay video has no offscreen pause strategy")
        if role in {"hero-background", "ambient-background"} and not asset.get("composition"):
            add_issue(issues, "P2", path, "background media has no composition/layer description")
        if asset.get("basis") == "recommended" and asset.get("evidence_ids"):
            add_issue(issues, "P2", path, "recommended media should explain rationale; source evidence is optional")


def validate_effects(
    effects: Any,
    source_ids: set[str],
    errors: list[str],
    warnings: list[str],
    issues: list[dict[str, str]],
) -> None:
    if effects is None:
        return
    if not isinstance(effects, list):
        add(errors, "$.effects", "must be an array")
        return
    for index, effect in enumerate(effects):
        path = f"$.effects[{index}]"
        if not isinstance(effect, dict):
            add(errors, path, "must be an object")
            continue
        validate_claim_fields(effect, path, source_ids, errors, warnings)
        driver = effect.get("driver")
        if driver is not None and driver not in EFFECT_DRIVERS:
            add(errors, f"{path}.driver", f"must be one of {sorted(EFFECT_DRIVERS)}")
        for field in ("id", "kind", "target", "driver"):
            if not effect.get(field):
                add(warnings, path, f"missing '{field}'")
        if effect.get("driver") in {"scroll", "pointer"} and not effect.get("fallback"):
            add_issue(issues, "P1", path, "interactive effect has no fallback")


def validate_motion(
    motion: Any,
    source_ids: set[str],
    errors: list[str],
    warnings: list[str],
    issues: list[dict[str, str]],
) -> None:
    if motion is None:
        return
    if not isinstance(motion, dict):
        add(errors, "$.motion", "must be an object")
        return
    reduced = motion.get("reduced_motion")
    if reduced is None and motion.get("patterns"):
        add_issue(issues, "P1", "$.motion", "motion section has no global reduced_motion policy")
    patterns = motion.get("patterns", [])
    if not isinstance(patterns, list):
        add(errors, "$.motion.patterns", "must be an array")
        return
    for index, pattern in enumerate(patterns):
        path = f"$.motion.patterns[{index}]"
        if not isinstance(pattern, dict):
            add(errors, path, "must be an object")
            continue
        validate_claim_fields(pattern, path, source_ids, errors, warnings)
        for field in ("name", "trigger", "properties"):
            if not pattern.get(field):
                add_issue(issues, "P2", path, f"motion pattern missing '{field}'")
        driver = pattern.get("driver")
        if driver is not None and driver not in MOTION_DRIVERS:
            add(errors, f"{path}.driver", f"must be one of {sorted(MOTION_DRIVERS)}")
        if not pattern.get("reduced_motion"):
            add_issue(issues, "P1", path, "motion pattern has no reduced_motion alternative")
        if not pattern.get("performance"):
            add_issue(issues, "P2", path, "motion pattern has no performance note")


def validate_components(
    components: Any,
    source_ids: set[str],
    errors: list[str],
    warnings: list[str],
    issues: list[dict[str, str]],
) -> None:
    if components is None:
        return
    if not isinstance(components, list):
        add(errors, "$.components", "must be an array")
        return
    for index, component in enumerate(components):
        path = f"$.components[{index}]"
        if not isinstance(component, dict):
            add(errors, path, "must be an object")
            continue
        validate_claim_fields(component, path, source_ids, errors, warnings)
        for field in ("id", "name", "anatomy", "states"):
            if not component.get(field):
                add(warnings, path, f"missing '{field}'")
        states = component.get("states")
        if isinstance(states, list) and any(state in {"hover", "focus-visible"} for state in states):
            continue
        if component.get("interaction"):
            add_issue(issues, "P2", path, "interactive component does not document hover/focus-visible states")


def validate(data: Any) -> tuple[list[str], list[str], list[dict[str, str]]]:
    errors: list[str] = []
    warnings: list[str] = []
    issues: list[dict[str, str]] = []
    if not isinstance(data, dict):
        return ["$: root must be a JSON object"], warnings, issues

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
        version = meta.get("schema_version", 1)
        if not isinstance(version, int) or version < 1:
            add(errors, "$.meta.schema_version", "must be a positive integer")
        elif version > 2:
            add(warnings, "$.meta.schema_version", "newer schema version may not be fully supported")
        if meta.get("overall_confidence") not in CONFIDENCE:
            add(errors, "$.meta.overall_confidence", f"must be one of {sorted(CONFIDENCE)}")
        if not isinstance(meta.get("scope"), list) or not meta.get("scope"):
            add(warnings, "$.meta.scope", "should be a non-empty array")
        if version >= 2 and not data.get("experience"):
            add_issue(issues, "P2", "$.experience", "schema version 2 has no Experience Layer")

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
        validate_claim_fields(value, path, source_ids, errors, warnings)
        token = value.get("token")
        raw_value = value.get("value")
        if isinstance(token, str) and token.startswith("color.") and isinstance(raw_value, str):
            if raw_value.startswith("#") and not HEX_COLOR.match(raw_value):
                add(errors, f"{path}.value", "invalid hexadecimal color")

    validate_experience(data.get("experience"), source_ids, errors, warnings, issues)
    validate_elements(data.get("elements"), source_ids, errors, warnings, issues)
    validate_media(data.get("media"), source_ids, errors, warnings, issues)
    validate_effects(data.get("effects"), source_ids, errors, warnings, issues)
    validate_motion(data.get("motion"), source_ids, errors, warnings, issues)
    validate_components(data.get("components"), source_ids, errors, warnings, issues)

    if isinstance(sources, list):
        viewports = {
            str(source.get("context", {}).get("viewport"))
            for source in sources
            if isinstance(source, dict)
            and isinstance(source.get("context"), dict)
            and source.get("context", {}).get("viewport")
        }
        if len(viewports) < 2:
            gaps = " ".join(map(str, data.get("gaps", []))).lower()
            if "viewport" not in gaps and "mobile" not in gaps and "responsive" not in gaps:
                add_issue(issues, "P1", "$.sources", "fewer than two viewports and no responsive limitation in gaps")

    colors = data.get("foundations", {}).get("colors", []) if isinstance(data.get("foundations"), dict) else []
    if not colors:
        add_issue(issues, "P2", "$.foundations.colors", "no color tokens found")
    if not data.get("components"):
        add_issue(issues, "P2", "$.components", "no components documented")
    motion = data.get("motion")
    if not isinstance(motion, dict) or not motion.get("patterns"):
        add_issue(issues, "P2", "$.motion", "no motion patterns; document the evidence gap if unavailable")

    return errors, warnings, issues


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

    errors, warnings, issues = validate(data)
    for item in errors:
        print(f"ERROR {item}")
    for item in warnings:
        print(f"WARN  {item}")
    for issue in issues:
        print(f"ISSUE {issue['severity']} {issue['path']}: {issue['message']}")
    counts = Counter(issue["severity"] for issue in issues)
    count_text = ", ".join(f"{key}={counts.get(key, 0)}" for key in ("P0", "P1", "P2", "P3"))
    print(f"Summary: {len(errors)} error(s), {len(warnings)} warning(s), {len(issues)} issue(s)")
    print(f"Quality: {count_text}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
