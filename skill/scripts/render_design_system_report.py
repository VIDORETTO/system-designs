#!/usr/bin/env python3
"""Render a self-contained living design-system report from the extraction JSON."""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path
from typing import Any


def esc(value: Any) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def seq(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        return [{"token": key, "value": item} for key, item in value.items()]
    return []


def scalar(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def badge(item: dict[str, Any]) -> str:
    basis = esc(item.get("basis", "unspecified"))
    confidence = esc(item.get("confidence", "unspecified"))
    return f'<span class="badge basis-{basis}">{basis}</span><span class="badge confidence">{confidence} confidence</span>'


def evidence(item: dict[str, Any]) -> str:
    ids = item.get("evidence_ids") or []
    return "" if not ids else f'<div class="evidence">Evidence: {esc(", ".join(map(str, ids)))}</div>'


def list_cards(items: Any, title_key: str = "name") -> str:
    cards = []
    for index, raw in enumerate(seq(items)):
        item = raw if isinstance(raw, dict) else {"value": raw}
        title = item.get(title_key) or item.get("label") or item.get("token") or item.get("id") or f"Item {index + 1}"
        ignored = {title_key, "label", "token", "id", "basis", "confidence", "evidence_ids"}
        rows = "".join(
            f'<dt>{esc(key.replace("_", " "))}</dt><dd>{esc(scalar(value))}</dd>'
            for key, value in item.items() if key not in ignored and value not in (None, "", [], {})
        )
        cards.append(f'<article class="card"><h3>{esc(title)}</h3><div class="badges">{badge(item)}</div><dl>{rows}</dl>{evidence(item)}</article>')
    return "".join(cards) or '<p class="empty">No supported evidence was captured for this section.</p>'


def css_var_name(token: str) -> str:
    return "--ds-" + re.sub(r"[^a-z0-9-]+", "-", token.lower().replace(".", "-")).strip("-")


def first_token(items: Any, fallback: str, contains: tuple[str, ...] = ()) -> str:
    candidates = seq(items)
    for raw in candidates:
        if not isinstance(raw, dict):
            continue
        name = str(raw.get("token", "")).lower()
        value = raw.get("value")
        if value and (not contains or any(part in name for part in contains)):
            return str(value)
    return fallback


def best_token(items: Any, fallback: str, preferred: tuple[str, ...]) -> str:
    """Select by ordered semantic phrase, avoiding broad matches such as text.primary."""
    candidates = [item for item in seq(items) if isinstance(item, dict) and item.get("value")]
    for phrase in preferred:
        for item in candidates:
            name = str(item.get("token", "")).lower()
            if phrase in name:
                return str(item["value"])
    return fallback


def render(data: dict[str, Any]) -> str:
    meta = data.get("meta", {})
    foundations = data.get("foundations", {})
    colors = seq(foundations.get("colors", []))
    primary = best_token(colors, "#5B5BD6", ("action.primary", "accent.primary", "brand.primary", "color.accent", "color.brand", "color.action"))
    background = best_token(colors, "#F7F7FA", ("background.page", "background", "canvas", "page"))
    surface = best_token(colors, "#FFFFFF", ("surface.card", "surface.elevated", "surface"))
    text = best_token(colors, "#18181B", ("text.primary", "foreground", "ink"))
    muted = best_token(colors, "#666672", ("text.secondary", "text.muted", "muted", "subtle"))
    border = best_token(colors, "#DEDEE6", ("border.default", "border", "outline"))
    radius = first_token(foundations.get("radii", []), "14px")
    shadow = first_token(foundations.get("shadows", []), "0 12px 32px rgba(0,0,0,.08)")
    font_family = first_token(foundations.get("typography", []), "Inter, ui-sans-serif, system-ui, sans-serif")

    token_vars = []
    for item in colors + seq(foundations.get("spacing", [])) + seq(foundations.get("radii", [])):
        if isinstance(item, dict) and item.get("token") and item.get("value") is not None:
            token_vars.append(f'{css_var_name(str(item["token"]))}: {item["value"]};')

    swatches = []
    for item in colors:
        if not isinstance(item, dict):
            continue
        value = item.get("value", "transparent")
        swatches.append(
            f'<article class="swatch card"><div class="swatch-color" style="--swatch:{esc(value)}"></div>'
            f'<h3>{esc(item.get("token", item.get("label", "Color")))}</h3><code>{esc(value)}</code>'
            f'<div class="badges">{badge(item)}</div>{evidence(item)}</article>'
        )

    source_rows = []
    for source in data.get("sources", []):
        if not isinstance(source, dict):
            continue
        source_rows.append(
            f'<tr><th scope="row">{esc(source.get("id"))}</th><td>{esc(source.get("source_type"))}</td>'
            f'<td>{esc(source.get("locator"))}</td><td>{esc(scalar(source.get("context", {})))}</td></tr>'
        )

    css_export = ":root {\n  " + "\n  ".join(token_vars) + "\n}"
    raw_json = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    title = esc(meta.get("name", "Extracted Design System"))
    summary = esc(meta.get("method_summary", "No method summary supplied."))

    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>
:root{{--report-primary:{esc(primary)};--report-bg:{esc(background)};--report-surface:{esc(surface)};--report-text:{esc(text)};--report-muted:{esc(muted)};--report-border:{esc(border)};--report-radius:{esc(radius)};--report-shadow:{esc(shadow)};--report-font:{esc(font_family)};{''.join(token_vars)}}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;background:var(--report-bg);color:var(--report-text);font-family:var(--report-font);line-height:1.55}}
a{{color:inherit}}button{{font:inherit}}.layout{{display:grid;grid-template-columns:240px minmax(0,1fr);min-height:100vh}}nav{{position:sticky;top:0;height:100vh;padding:24px;border-right:1px solid var(--report-border);background:color-mix(in srgb,var(--report-surface) 92%,transparent);overflow:auto}}nav strong{{display:block;margin-bottom:20px}}nav a{{display:block;padding:8px 10px;border-radius:8px;text-decoration:none;color:var(--report-muted)}}nav a:hover,nav a:focus-visible{{background:color-mix(in srgb,var(--report-primary) 12%,transparent);color:var(--report-text);outline:2px solid transparent}}main{{min-width:0}}.hero{{padding:clamp(48px,8vw,112px) clamp(24px,6vw,88px);background:linear-gradient(135deg,color-mix(in srgb,var(--report-primary) 20%,var(--report-bg)),var(--report-bg))}}.eyebrow{{font-size:.78rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--report-primary)}}h1{{font-size:clamp(2.3rem,6vw,5.5rem);line-height:.98;letter-spacing:-.045em;max-width:13ch;margin:.2em 0}}h2{{font-size:clamp(1.7rem,3vw,2.6rem);letter-spacing:-.025em}}h3{{margin:.2rem 0 .8rem}}.lede{{font-size:1.15rem;max-width:65ch;color:var(--report-muted)}}.section{{padding:56px clamp(24px,6vw,88px);border-top:1px solid var(--report-border)}}.section-head{{max-width:72ch;margin-bottom:24px}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:18px}}.card{{background:var(--report-surface);border:1px solid var(--report-border);border-radius:var(--report-radius);padding:20px;box-shadow:var(--report-shadow)}}.swatch-color{{height:118px;margin:-20px -20px 16px;border-radius:var(--report-radius) var(--report-radius) 0 0;background:var(--swatch);border-bottom:1px solid var(--report-border)}}.badges{{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0}}.badge{{font-size:.72rem;padding:3px 8px;border:1px solid var(--report-border);border-radius:999px;background:var(--report-bg)}}.basis-observed{{border-color:var(--report-primary)}}.basis-inferred{{border-style:dashed}}.basis-recommended{{background:color-mix(in srgb,#f59e0b 14%,var(--report-bg))}}dl{{display:grid;grid-template-columns:minmax(90px,.35fr) 1fr;gap:7px 12px;font-size:.9rem}}dt{{font-weight:700;text-transform:capitalize}}dd{{margin:0;overflow-wrap:anywhere;color:var(--report-muted)}}.evidence,.empty{{font-size:.82rem;color:var(--report-muted);margin-top:12px}}code,pre{{font-family:ui-monospace,SFMono-Regular,Consolas,monospace}}pre{{padding:20px;border-radius:var(--report-radius);background:#111118;color:#f5f5f7;overflow:auto}}table{{width:100%;border-collapse:collapse;background:var(--report-surface)}}th,td{{padding:12px;text-align:left;border-bottom:1px solid var(--report-border);vertical-align:top;overflow-wrap:anywhere}}.motion-stage{{display:grid;place-items:center;min-height:180px;background:var(--report-surface);border:1px solid var(--report-border);border-radius:var(--report-radius)}}.motion-dot{{width:72px;height:72px;border-radius:28%;background:var(--report-primary)}}.motion-stage.play .motion-dot{{animation:specimen 700ms cubic-bezier(.2,.8,.2,1)}}@keyframes specimen{{0%{{opacity:.2;transform:translateY(24px) scale(.9)}}100%{{opacity:1;transform:none}}}}.toolbar{{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0}}.toolbar button{{border:1px solid var(--report-border);background:var(--report-surface);color:var(--report-text);border-radius:999px;padding:8px 14px;cursor:pointer}}.toolbar button:focus-visible{{outline:3px solid color-mix(in srgb,var(--report-primary) 50%,transparent);outline-offset:2px}}.reduced *{{animation-duration:.001ms!important;animation-iteration-count:1!important;transition-duration:.001ms!important}}@media(max-width:800px){{.layout{{display:block}}nav{{position:relative;height:auto;border-right:0;border-bottom:1px solid var(--report-border)}}nav .links{{display:flex;gap:4px;overflow:auto}}nav a{{white-space:nowrap}}.section{{padding-block:42px}}}}@media(prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}*,*::before,*::after{{animation-duration:.001ms!important;animation-iteration-count:1!important;transition-duration:.001ms!important}}}}
</style></head><body><div class="layout"><nav aria-label="Report sections"><strong>{title}</strong><div class="links"><a href="#overview">Overview</a><a href="#colors">Colors</a><a href="#foundations">Foundations</a><a href="#motion">Motion</a><a href="#components">Components</a><a href="#evidence">Evidence</a><a href="#export">Export</a></div></nav><main>
<header class="hero" id="overview"><div class="eyebrow">Living design-system extraction</div><h1>{title}</h1><p class="lede">{summary}</p><div class="badges"><span class="badge">{esc(meta.get('overall_confidence','unknown'))} overall confidence</span><span class="badge">{esc(meta.get('fidelity_target','unspecified'))} fidelity</span></div></header>
<section class="section"><div class="section-head"><div class="eyebrow">Design DNA</div><h2>Principles</h2></div><div class="grid">{list_cards(data.get('principles',[]),'label')}</div></section>
<section class="section" id="colors"><div class="section-head"><div class="eyebrow">Foundations</div><h2>Color system</h2><p>Semantic roles and extracted values. The report shell uses these tokens where safe.</p></div><div class="grid">{''.join(swatches) or '<p class="empty">No colors documented.</p>'}</div></section>
<section class="section" id="foundations"><div class="section-head"><div class="eyebrow">System grammar</div><h2>Type, spacing, shape, and depth</h2></div>{''.join(f'<h3>{esc(key.replace("_"," ").title())}</h3><div class="grid">{list_cards(foundations.get(key,[]),"token")}</div>' for key in ('typography','spacing','sizing','grid','radii','borders','shadows','iconography','imagery'))}</section>
<section class="section" id="motion"><div class="section-head"><div class="eyebrow">Behavior over time</div><h2>Motion lab</h2><p>This baseline demonstrates the controls; enrich it to reproduce each extracted pattern when exact implementation fidelity is required.</p></div><div class="toolbar"><button type="button" id="replay">Replay specimen</button><button type="button" id="pause" aria-pressed="false">Pause motion</button><button type="button" id="slow" aria-pressed="false">Slow motion</button><button type="button" id="reduce" aria-pressed="false">Reduce motion</button></div><div class="motion-stage" id="stage"><div class="motion-dot" aria-label="Motion specimen"></div></div><div class="grid" style="margin-top:18px">{list_cards(data.get('motion',{}).get('patterns',[]),'name')}</div></section>
<section class="section" id="components"><div class="section-head"><div class="eyebrow">Reusable interface</div><h2>Components</h2></div><div class="grid">{list_cards(data.get('components',[]),'name')}</div></section>
<section class="section"><div class="section-head"><div class="eyebrow">Composition</div><h2>Responsive and page patterns</h2></div><h3>Responsive rules</h3><div class="grid">{list_cards(data.get('responsive',{}).get('rules',[]),'element')}</div><h3>Page patterns</h3><div class="grid">{list_cards(data.get('patterns',[]),'name')}</div></section>
<section class="section" id="evidence"><div class="section-head"><div class="eyebrow">Provenance</div><h2>Evidence and uncertainty</h2></div><div style="overflow:auto"><table><thead><tr><th>ID</th><th>Type</th><th>Locator</th><th>Context</th></tr></thead><tbody>{''.join(source_rows)}</tbody></table></div><h3>Gaps</h3><div class="grid">{list_cards(data.get('gaps',[]))}</div><h3>Exceptions</h3><div class="grid">{list_cards(data.get('exceptions',[]))}</div><h3>Additional findings</h3><div class="grid">{list_cards(data.get('additional_findings',[]),'label')}</div></section>
<section class="section" id="export"><div class="section-head"><div class="eyebrow">Implementation</div><h2>Token export</h2></div><button type="button" id="copy" class="badge">Copy CSS</button><pre id="css-export">{esc(css_export)}</pre></section>
</main></div><script type="application/json" id="design-system-data">{raw_json}</script><script>
const stage=document.getElementById('stage');document.getElementById('replay').addEventListener('click',()=>{{stage.classList.remove('play');requestAnimationFrame(()=>requestAnimationFrame(()=>stage.classList.add('play')))}});
document.getElementById('pause').addEventListener('click',e=>{{const target=stage.querySelector('.motion-dot');const on=target.style.animationPlayState!=='paused';target.style.animationPlayState=on?'paused':'running';e.currentTarget.setAttribute('aria-pressed',String(on));e.currentTarget.textContent=on?'Resume motion':'Pause motion'}});
document.getElementById('slow').addEventListener('click',e=>{{const target=stage.querySelector('.motion-dot');const on=target.style.animationDuration!=='2100ms';target.style.animationDuration=on?'2100ms':'';e.currentTarget.setAttribute('aria-pressed',String(on));e.currentTarget.textContent=on?'Normal speed':'Slow motion'}});
document.getElementById('reduce').addEventListener('click',e=>{{const on=document.body.classList.toggle('reduced');e.currentTarget.setAttribute('aria-pressed',String(on));e.currentTarget.textContent=on?'Restore motion':'Reduce motion'}});
document.getElementById('copy').addEventListener('click',async e=>{{try{{await navigator.clipboard.writeText(document.getElementById('css-export').textContent);e.currentTarget.textContent='Copied'}}catch{{e.currentTarget.textContent='Select CSS below'}}}});
</script></body></html>'''


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: render_design_system_report.py DESIGN_SYSTEM.json REPORT.html", file=sys.stderr)
        return 2
    input_path, output_path = map(Path, sys.argv[1:])
    try:
        data = json.loads(input_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    if not isinstance(data, dict):
        print("ERROR: manifest root must be an object", file=sys.stderr)
        return 1
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render(data), encoding="utf-8")
    print(f"Rendered {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
