#!/usr/bin/env python3
"""Build a static media/effects inventory from HTML, CSS, or JavaScript.

This probe is intentionally conservative: it finds candidates and signals, but
does not claim that a runtime state was observed. Merge its output with the
browser probe before promoting a claim to observed runtime behavior.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
from typing import Any


MEDIA_EXTENSIONS = {
    ".avif": "image",
    ".gif": "image",
    ".jpeg": "image",
    ".jpg": "image",
    ".m4v": "video",
    ".mp3": "audio",
    ".ogg": "audio",
    ".png": "image",
    ".svg": "svg",
    ".wav": "audio",
    ".webm": "video",
    ".webp": "image",
    ".mp4": "video",
    ".mov": "video",
}

URL_RE = re.compile(
    r"""(?:url\(\s*['"]?([^'")\s]+)|(?:src|poster|href|data-src|data-video|data-poster)\s*=\s*['"]([^'"]+))""",
    re.IGNORECASE,
)
KEYFRAME_RE = re.compile(r"@(?:-webkit-)?keyframes\s+([a-zA-Z0-9_-]+)", re.IGNORECASE)
ANIMATION_RE = re.compile(r"\banimation(?:-name)?\s*:\s*([^;}{]+)", re.IGNORECASE)
QUOTED_MEDIA_RE = re.compile(
    r"""['"]([^'"]+\.(?:avif|gif|jpe?g|m4v|mp3|ogg|png|svg|wav|webm|webp|mp4|mov)(?:[?#][^'"]*)?)['"]""",
    re.IGNORECASE,
)


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def kind_for_url(url: str) -> str:
    path = urlparse(url).path.lower()
    return MEDIA_EXTENSIONS.get(Path(path).suffix, "unknown")


def clean_url(value: str) -> str:
    return html.unescape(value.strip()).rstrip(";,")


def media_candidate(url: str, origin: str, role: str = "unknown") -> dict[str, Any]:
    stable_id = hashlib.sha1(f"{url}\0{origin}".encode("utf-8")).hexdigest()[:8]
    return {
        "id": "media-static-" + stable_id,
        "url": clean_url(url),
        "kind": kind_for_url(url),
        "role": role,
        "basis": "observed",
        "confidence": "low",
        "evidence_ids": ["E-static-source-001"],
        "source_hint": origin,
        "notes": "Candidato encontrado em fonte estática; confirmar no runtime.",
    }


class MarkupParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.assets: list[dict[str, Any]] = []
        self.signals: list[dict[str, Any]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_map = {key.lower(): value or "" for key, value in attrs}
        tag = tag.lower()
        role = "content"
        if tag == "video":
            role = "hero-background" if "autoplay" in attrs_map else "content"
            self.signals.append({"signal": "video-element", "tag": tag, "basis": "observed"})
        elif tag == "audio":
            role = "content"
            self.signals.append({"signal": "audio-element", "tag": tag, "basis": "observed"})
        elif tag in {"canvas", "iframe"}:
            role = "decorative" if tag == "canvas" else "content"
            self.signals.append({"signal": f"{tag}-element", "tag": tag, "basis": "observed"})
        elif tag in {"img", "picture", "source"}:
            role = "content"

        for key in ("src", "poster", "data-src", "data-video", "data-poster"):
            value = attrs_map.get(key)
            if value and not value.startswith(("data:", "blob:", "#")):
                self.assets.append(media_candidate(value, f"<{tag} {key}>", role))

        srcset = attrs_map.get("srcset", "")
        for candidate in srcset.split(","):
            value = candidate.strip().split(" ")[0]
            if value and not value.startswith(("data:", "blob:", "#")):
                self.assets.append(media_candidate(value, f"<{tag} srcset>", role))

        style = attrs_map.get("style", "")
        for match in URL_RE.finditer(style):
            value = next((part for part in match.groups() if part), "")
            if value and not value.startswith(("data:", "blob:", "#")):
                self.assets.append(media_candidate(value, f"<{tag} style>", "decorative"))


def add_source_urls(text: str, origin: str, assets: list[dict[str, Any]]) -> None:
    for match in URL_RE.finditer(text):
        value = next((part for part in match.groups() if part), "")
        if value and not value.startswith(("data:", "blob:", "#")):
            assets.append(media_candidate(value, origin, "unknown"))
    for match in QUOTED_MEDIA_RE.finditer(text):
        value = match.group(1)
        if not value.startswith(("data:", "blob:", "#")):
            assets.append(media_candidate(value, f"{origin} quoted string", "unknown"))


def unique(items: list[dict[str, Any]], keys: tuple[str, ...]) -> list[dict[str, Any]]:
    seen: set[tuple[Any, ...]] = set()
    result: list[dict[str, Any]] = []
    for item in items:
        key = tuple(item.get(name) for name in keys)
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


def scan(source: Path) -> dict[str, Any]:
    text = source.read_text(encoding="utf-8", errors="replace")
    assets: list[dict[str, Any]] = []
    signals: list[dict[str, Any]] = []
    parser = MarkupParser()

    if source.suffix.lower() in {".html", ".htm", ".xhtml"}:
        parser.feed(text)
        assets.extend(parser.assets)
        signals.extend(parser.signals)

    add_source_urls(text, source.name, assets)

    keyframes = sorted(set(KEYFRAME_RE.findall(text)))
    animations = sorted(set(name.strip() for match in ANIMATION_RE.findall(text) for name in match.split(",")))
    effect_patterns = {
        "backdrop-filter": r"\bbackdrop-filter\s*:",
        "filter": r"(?<![-\w])filter\s*:",
        "mix-blend-mode": r"\bmix-blend-mode\s*:",
        "mask": r"\bmask(?:-image)?\s*:",
        "clip-path": r"\bclip-path\s*:",
        "gradient": r"\b(?:linear|radial|conic)-gradient\s*\(",
        "particle-or-canvas": r"\b(?:canvas|particles?|shader|webgl)\b",
    }
    for label, pattern in effect_patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            signals.append({"signal": label, "basis": "observed", "source_hint": source.name})

    runtime_hints = {
        "scroll": r"\b(?:scroll|scroll-timeline|view-timeline|IntersectionObserver)\b",
        "pointer": r"\b(?:pointermove|mousemove|mouseenter|mouseleave|hover)\b",
        "gesture": r"\b(?:touchstart|touchmove|dragstart|wheel)\b",
        "raf": r"\brequestAnimationFrame\b",
        "view-transition": r"\bstartViewTransition\b",
        "lottie": r"\b(?:lottie|bodymovin)\b",
    }
    for label, pattern in runtime_hints.items():
        if re.search(pattern, text, re.IGNORECASE):
            signals.append({"signal": label, "basis": "observed", "source_hint": source.name})

    if keyframes:
        signals.append({"signal": "keyframes", "names": keyframes, "basis": "observed"})
    if animations:
        signals.append({"signal": "animation-declarations", "names": animations[:50], "basis": "observed"})

    assets = unique(assets, ("url", "source_hint"))
    signals = unique(signals, ("signal", "source_hint"))
    gaps = [
        {
            "id": "gap-runtime-media-state",
            "label": "Runtime media state not verified",
            "basis": "inferred",
            "confidence": "high",
            "notes": "Use runtime_media_probe.js to verify playback, visibility, computed composition and interaction triggers.",
        }
    ]
    return {
        "meta": {
            "schema_version": 2,
            "tool": "probe_media_inventory",
            "generated_at": iso_now(),
            "input": str(source),
            "scope": "static media, effect and motion candidate inventory",
        },
        "sources": [
            {
                "id": "E-static-source-001",
                "source_type": "source",
                "locator": str(source),
                "captured_at": iso_now(),
                "context": "static source scan",
                "limitations": ["does not prove runtime visibility, playback, trigger, or breakpoint behavior"],
            }
        ],
        "media": {"assets": assets},
        "effects": signals,
        "motion": {"signals": signals, "patterns": []},
        "gaps": gaps,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="HTML, CSS or JavaScript file")
    parser.add_argument("--output", type=Path, help="write JSON to this path")
    args = parser.parse_args()
    if not args.source.is_file():
        print(json.dumps({"error": f"Source not found: {args.source}"}), file=sys.stderr)
        return 2
    result = scan(args.source)
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        sys.stdout.write(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
