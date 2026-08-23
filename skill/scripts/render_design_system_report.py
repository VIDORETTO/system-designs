#!/usr/bin/env python3
"""Render a self-contained, accessible living design-system report."""

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


def safe_css(value: Any, fallback: str) -> str:
    raw = str(value or "").strip()
    if not raw or len(raw) > 140 or re.search(r"[<>{};]", raw) or chr(96) in raw:
        return fallback
    return raw


def safe_href(value: Any) -> str:
    raw = str(value or "").strip()
    if raw.startswith("//"):
        return ""
    if raw.startswith(("./", "../", "/", "data:image/")):
        return esc(raw)
    return ""


def badge(item: dict[str, Any]) -> str:
    basis = esc(item.get("basis", "unspecified"))
    confidence = esc(item.get("confidence", "unspecified"))
    return f'<span class="badge basis-{basis}">{basis}</span><span class="badge confidence">{confidence} confidence</span>'


def evidence(item: dict[str, Any]) -> str:
    ids = item.get("evidence_ids") or []
    if not ids:
        return ""
    return f'<div class="evidence">Evidence: {esc(", ".join(map(str, ids)))}</div>'


def title_for(item: dict[str, Any], index: int, preferred: tuple[str, ...] = ()) -> str:
    for key in (*preferred, "name", "label", "token", "id"):
        if item.get(key):
            return str(item[key])
    return f"Item {index + 1}"


def detail_rows(item: dict[str, Any], ignored: set[str] | None = None) -> str:
    ignored = ignored or set()
    rows: list[str] = []
    for key, value in item.items():
        if key in ignored or value in (None, "", [], {}):
            continue
        rows.append(f"<dt>{esc(key.replace('_', ' '))}</dt><dd>{esc(scalar(value))}</dd>")
    return "".join(rows)


def cards(items: Any, title_keys: tuple[str, ...] = ()) -> str:
    rendered: list[str] = []
    for index, raw in enumerate(seq(items)):
        item = raw if isinstance(raw, dict) else {"value": raw}
        rendered.append(
            '<article class="card">'
            f"<h3>{esc(title_for(item, index, title_keys))}</h3>"
            f'<div class="badges">{badge(item)}</div>'
            f"<dl>{detail_rows(item, {'name', 'label', 'token', 'id', 'basis', 'confidence', 'evidence_ids'})}</dl>"
            f"{evidence(item)}</article>"
        )
    return "".join(rendered) or '<p class="empty">Nenhuma evidência estruturada disponível.</p>'


def first_value(items: Any, fallback: str, contains: tuple[str, ...] = ()) -> str:
    candidates = [item for item in seq(items) if isinstance(item, dict) and item.get("value")]
    for item in candidates:
        token = str(item.get("token", "")).lower()
        if not contains or any(part in token for part in contains):
            return str(item["value"])
    return fallback


def first_token(items: Any, fallback: str, preferred: tuple[str, ...]) -> str:
    candidates = [item for item in seq(items) if isinstance(item, dict) and item.get("value")]
    for phrase in preferred:
        for item in candidates:
            if phrase in str(item.get("token", "")).lower():
                return str(item["value"])
    return first_value(items, fallback)


def token_cards(items: Any, mode_key: str = "value") -> str:
    rendered: list[str] = []
    for index, raw in enumerate(seq(items)):
        item = raw if isinstance(raw, dict) else {"value": raw}
        value = item.get(mode_key, item.get("value"))
        token = title_for(item, index, ("token",))
        sample = ""
        if value and isinstance(value, str) and (value.startswith("#") or value.startswith("rgb") or value.startswith("hsl")):
            sample = f'<span class="swatch" style="background:{safe_css(value, "transparent")}"></span>'
        rendered.append(
            f'<article class="token-card">{sample}<div><strong>{esc(token)}</strong>'
            f'<code>{esc(scalar(value))}</code><div class="badges">{badge(item)}</div>'
            f"{evidence(item)}</div></article>"
        )
    return "".join(rendered) or '<p class="empty">Nenhum token encontrado.</p>'


def list_block(value: Any, empty: str = "—") -> str:
    if isinstance(value, list):
        return "".join(f"<li>{esc(scalar(item))}</li>" for item in value) or f"<li>{esc(empty)}</li>"
    if value:
        return f"<li>{esc(scalar(value))}</li>"
    return f"<li>{esc(empty)}</li>"


def section_intro(label: str, title: str, text: str) -> str:
    return f'<div class="section-intro"><p class="eyebrow">{esc(label)}</p><h2>{esc(title)}</h2><p>{esc(text)}</p></div>'


def experience_section(data: dict[str, Any]) -> str:
    experience = data.get("experience") or {}
    identity = experience.get("identity_lock") or {}
    focal = experience.get("focal_moment") or {}
    signature = experience.get("signature_elements") or []
    rules = experience.get("named_rules") or []
    dos = experience.get("dos") or experience.get("do") or []
    donts = experience.get("donts") or experience.get("dont") or []
    recommendations = experience.get("recommendations") or []
    identity_rows = detail_rows(identity, {"basis", "confidence", "evidence_ids"})
    focal_rows = detail_rows(focal, {"basis", "confidence", "evidence_ids"})
    return (
        '<section id="identity" class="section">'
        + section_intro("01 · Experience layer", "Identidade antes do token", "A camada que preserva a sensação, a intenção e o centro de gravidade da experiência.")
        + '<div class="hero-grid">'
        + f'<article class="feature-card"><span class="kicker">Identity lock</span><h3>{esc(identity.get("thesis") or identity.get("statement") or "Sem tese registrada")}</h3><dl>{identity_rows}</dl>{badge(identity)}{evidence(identity)}</article>'
        + f'<article class="feature-card focal-card"><span class="kicker">Focal moment</span><h3>{esc(focal.get("name") or focal.get("label") or "Momento focal")}</h3><p>{esc(focal.get("description") or focal.get("why") or "Descreva o instante que deve carregar a primeira impressão.")}</p><dl>{focal_rows}</dl>{badge(focal)}{evidence(focal)}</article>'
        + "</div>"
        + '<div class="subsection"><h3>Signature elements</h3><div class="grid three">'
        + cards(signature, ("name", "label", "element"))
        + "</div></div>"
        + '<div class="subsection"><h3>Named rules</h3><div class="grid three">'
        + cards(rules, ("name", "rule", "label"))
        + "</div></div>"
        + '<div class="grid two"><article class="card"><h3>Do</h3><ul class="plain-list">'
        + list_block(dos, "Use the extracted hierarchy and focal moment.")
        + '</ul></article><article class="card"><h3>Don’t</h3><ul class="plain-list">'
        + list_block(donts, "Não neutralize a identidade em componentes genéricos.")
        + "</ul></article></div>"
        + ('<div class="subsection"><h3>Recommendations</h3><div class="grid three">' + cards(recommendations) + "</div></div>" if recommendations else "")
        + "</section>"
    )


def media_preview(item: dict[str, Any], index: int) -> str:
    kind = str(item.get("kind") or "unknown").lower()
    source_href = safe_href(item.get("preview_url") or item.get("source_url"))
    poster_href = safe_href(item.get("poster") or item.get("fallback_poster"))
    asset_id = esc(item.get("id") or f"media-{index + 1}")
    if kind in {"image", "svg"} and (source_href or poster_href):
        visual = f'<img src="{source_href or poster_href}" alt="{esc(item.get("alt") or "Evidence preview")}" loading="lazy" />'
    elif kind == "video" and source_href:
        poster = f' poster="{poster_href}"' if poster_href else ""
        visual = f'<video id="video-{asset_id}" controls muted loop playsinline preload="metadata"{poster}><source src="{source_href}" /></video>'
    elif poster_href:
        visual = f'<img src="{poster_href}" alt="{esc(item.get("alt") or "Poster fallback")}" loading="lazy" />'
    else:
        visual = f'<div class="media-placeholder"><span>{esc(kind)}</span><strong>{esc(item.get("label") or item.get("url") or "No local preview")}</strong><small>Preview bloqueado até haver evidência local autorizada.</small></div>'
    action = ""
    if kind == "video" and source_href:
        action = f'<button class="quiet-button" type="button" data-media-toggle="video-{asset_id}">Play / pause</button>'
    return (
        '<article class="media-card">'
        f'<div class="media-visual">{visual}</div>'
        f'<div class="media-meta"><div class="badges">{badge(item)}</div><h3>{esc(item.get("label") or item.get("id") or f"Asset {index + 1}")}</h3>'
        f'<p>{esc(item.get("role") or "media")} · {esc(item.get("kind") or "unknown")}</p>'
        f'<dl>{detail_rows(item, {"label", "id", "basis", "confidence", "evidence_ids", "kind", "role", "preview_url", "poster", "fallback_poster"})}</dl>{evidence(item)}{action}</div>'
        "</article>"
    )


def media_section(data: dict[str, Any]) -> str:
    media = data.get("media") or {}
    assets = media.get("assets") if isinstance(media, dict) else []
    resources = media.get("resources") if isinstance(media, dict) else []
    policy = media.get("policy") if isinstance(media, dict) else {}
    policy_text = (
        f'<div class="policy-note"><strong>Media policy</strong><p>{esc(policy.get("summary") or "Use motion to establish atmosphere and hierarchy; preserve a static, accessible fallback.")}</p>'
        f'<dl>{detail_rows(policy, {"summary"})}</dl></div>'
        if policy else ""
    )
    resource_cards = cards(resources, ("url", "name", "initiator"))
    return (
        '<section id="media" class="section">'
        + section_intro("06 · Media layer", "Vídeo, imagem e textura como composição", "A mídia não é só um arquivo: registre papel, recorte, overlay, fallback, playback, peso e o que realmente foi observado.")
        + policy_text
        + '<div class="grid two">'
        + "".join(media_preview(item, index) for index, item in enumerate(seq(assets)))
        + ('<p class="empty">Nenhum asset de mídia foi catalogado.</p>' if not seq(assets) else "")
        + "</div>"
        + '<div class="subsection"><h3>Network/media resources</h3><div class="grid three">'
        + resource_cards
        + "</div></div></section>"
    )


def motion_stage(item: dict[str, Any], index: int) -> str:
    duration = safe_css(item.get("duration") or item.get("duration_ms") or "700ms", "700ms")
    easing = safe_css(item.get("easing") or "cubic-bezier(.22,1,.36,1)", "cubic-bezier(.22,1,.36,1)")
    trigger = item.get("trigger") or item.get("driver") or "manual"
    motion_class = "motion-pulse" if "pulse" in str(item.get("name", "")).lower() else "motion-float"
    return (
        '<article class="motion-card">'
        f'<div class="motion-stage"><div class="motion-object {motion_class}" style="--motion-duration:{esc(duration)};--motion-easing:{esc(easing)}" aria-label="Motion specimen"></div></div>'
        f'<div class="motion-meta"><span class="kicker">Pattern {index + 1}</span><h3>{esc(item.get("name") or item.get("label") or "Motion pattern")}</h3>'
        f'<p><strong>Trigger:</strong> {esc(trigger)} · <strong>Job:</strong> {esc(item.get("job") or item.get("purpose") or "continuity")}</p>'
        f'<dl>{detail_rows(item, {"name", "label", "trigger", "driver", "job", "purpose", "basis", "confidence", "evidence_ids"})}</dl><div class="badges">{badge(item)}</div>{evidence(item)}</div>'
        "</article>"
    )


def motion_section(data: dict[str, Any]) -> str:
    motion = data.get("motion") or {}
    patterns = motion.get("patterns") if isinstance(motion, dict) else []
    reduced = motion.get("reduced_motion") if isinstance(motion, dict) else {}
    controls = (
        '<div class="lab-controls" role="group" aria-label="Motion controls">'
        '<button type="button" data-motion-action="replay">Replay</button>'
        '<button type="button" data-motion-action="pause">Pause</button>'
        '<button type="button" data-motion-action="slow">Slow</button>'
        '<button type="button" data-motion-action="reduce">Reduce motion</button></div>'
    )
    return (
        '<section id="motion" class="section">'
        + section_intro("07 · Motion", "Ritmo com trabalho claro", "Toda animação precisa de gatilho, papel, custo e fallback. O laboratório abaixo é interativo e respeita redução de movimento.")
        + controls
        + '<div class="grid two">'
        + "".join(motion_stage(item, index) for index, item in enumerate(seq(patterns)))
        + ('<p class="empty">Nenhum padrão de motion foi capturado.</p>' if not seq(patterns) else "")
        + "</div>"
        + f'<div class="policy-note"><strong>Reduced motion</strong><p>{esc(scalar(reduced) if reduced else "Desative deslocamentos decorativos, preserve feedback e mantenha continuidade por mudança de estado.")}</p></div>'
        + "</section>"
    )


def effect_section(data: dict[str, Any]) -> str:
    effects = data.get("effects") or []
    if isinstance(effects, dict):
        effects = effects.get("patterns") or effects.get("signals") or []
    rendered = []
    for index, raw in enumerate(seq(effects)):
        item = raw if isinstance(raw, dict) else {"label": raw}
        driver = item.get("driver") or item.get("trigger") or item.get("signal") or "static"
        rendered.append(
            '<article class="effect-card">'
            f'<div class="effect-stage effect-{index % 3}"><span>{esc(item.get("name") or item.get("label") or item.get("signal") or "Effect")}</span></div>'
            f'<h3>{esc(item.get("name") or item.get("label") or item.get("signal") or f"Effect {index + 1}")}</h3>'
            f'<p><strong>Driver:</strong> {esc(driver)}</p><dl>{detail_rows(item, {"name", "label", "signal", "driver", "trigger", "basis", "confidence", "evidence_ids"})}</dl><div class="badges">{badge(item)}</div>{evidence(item)}</article>'
        )
    return (
        '<section id="effects" class="section">'
        + section_intro("08 · Effects", "Atmosfera, profundidade e resposta", "Grain, blur, blend, gradients, canvas e parallax devem ter função perceptível e fallback para baixo consumo, acessibilidade e reduced motion.")
        + '<div class="grid three">'
        + "".join(rendered)
        + ('<p class="empty">Nenhum efeito foi catalogado.</p>' if not rendered else "")
        + "</div></section>"
    )


def component_preview(item: dict[str, Any]) -> str:
    name = str(item.get("name") or item.get("label") or "component").lower()
    if "button" in name or "cta" in name:
        return '<div class="component-demo"><button class="demo-primary" type="button">Primary action</button><button class="demo-secondary" type="button">Secondary</button></div>'
    if "nav" in name or "menu" in name:
        return '<nav class="component-demo demo-nav" aria-label="Navigation specimen"><a href="#overview">Overview</a><a href="#media">Media</a><a href="#motion">Motion</a></nav>'
    if "input" in name or "field" in name or "form" in name:
        return '<div class="component-demo"><label>Search<input type="search" placeholder="Type to filter" /></label></div>'
    if "card" in name or "tile" in name:
        return '<div class="component-demo demo-card"><span class="kicker">Specimen</span><strong>Useful content with a clear focal point.</strong><small>States and content limits belong in the contract.</small></div>'
    return '<div class="component-demo demo-generic"><span>Default state</span><span class="demo-dot"></span></div>'


def components_section(data: dict[str, Any]) -> str:
    rendered: list[str] = []
    for index, raw in enumerate(seq(data.get("components"))):
        item = raw if isinstance(raw, dict) else {"name": raw}
        rendered.append(
            '<article class="component-card">'
            f'<div class="badges">{badge(item)}</div><h3>{esc(title_for(item, index))}</h3>{component_preview(item)}'
            f'<div class="component-detail"><strong>Anatomy</strong><ul>{list_block(item.get("anatomy"))}</ul><strong>States</strong><ul>{list_block(item.get("states"))}</ul></div>'
            f"{evidence(item)}</article>"
        )
    return "".join(rendered) or '<p class="empty">Nenhum componente catalogado.</p>'


def foundations_section(data: dict[str, Any]) -> str:
    foundations = data.get("foundations") or {}
    colors = foundations.get("colors") or []
    typography = foundations.get("typography") or []
    spacing = foundations.get("spacing") or []
    sizing = foundations.get("sizing") or []
    grid = foundations.get("grid") or {}
    return (
        '<section id="foundations" class="section">'
        + section_intro("03 · Foundations", "Tokens com função", "Valores só entram quando carregam papel semântico, contexto e evidência.")
        + '<div id="colors" class="subsection"><h3>Colors</h3><div class="token-grid">'
        + token_cards(colors)
        + '</div></div><div class="grid two"><article class="card"><h3>Typography</h3><dl>'
        + detail_rows(typography if isinstance(typography, dict) else {"styles": typography})
        + '</dl></article><article class="card"><h3>Spacing & sizing</h3><dl>'
        + detail_rows({"spacing": spacing, "sizing": sizing})
        + '</dl></article></div><div class="card"><h3>Grid & container</h3><dl>'
        + detail_rows(grid if isinstance(grid, dict) else {"value": grid})
        + '</dl></div>'
        + "</section>"
    )


def responsive_section(data: dict[str, Any]) -> str:
    responsive = data.get("responsive") or {}
    rules = responsive.get("rules") if isinstance(responsive, dict) else responsive
    comparison = responsive.get("comparison") if isinstance(responsive, dict) else []
    if not comparison:
        comparison = [
            {
                "label": "Desktop",
                "viewport": "1440px",
                "summary": "Full navigation, wide reading plane and ambient media.",
            },
            {
                "label": "Mobile",
                "viewport": "390px",
                "summary": "Stacked hierarchy, tighter crop and poster/data-saver fallback.",
            },
        ]
    comparison_html = "".join(
        f'<article class="viewport-frame"><span class="kicker">{esc(item.get("label") or "Viewport")}</span><strong>{esc(item.get("viewport") or item.get("width") or "unknown")}</strong><p>{esc(item.get("summary") or item.get("change") or "Observed transformation")}</p></article>'
        for item in comparison if isinstance(item, dict)
    )
    return (
        '<section id="responsive" class="section">'
        + section_intro("04 · Responsive", "Mudança de regra, não escala", "Registre reflow, substituição, densidade e limites de container com faixas observadas.")
        + f'<div class="responsive-compare" aria-label="Responsive comparison">{comparison_html}</div>'
        + '<div class="grid three">'
        + cards(rules, ("name", "label", "change", "viewport"))
        + "</div></section>"
    )


def accessibility_section(data: dict[str, Any]) -> str:
    accessibility = data.get("accessibility") or {}
    content = data.get("content_style") or {}
    return (
        '<section id="accessibility" class="section">'
        + section_intro("10 · Accessibility & content", "Comportamento que sustenta a experiência", "A auditoria inclui foco, contraste, teclado, redução de movimento, linguagem e conteúdo realista.")
        + '<div class="grid two"><article class="card"><h3>Accessibility</h3><dl>'
        + detail_rows(accessibility)
        + '</dl></article><article class="card"><h3>Content style</h3><dl>'
        + detail_rows(content)
        + "</dl></article></div></section>"
    )


def evidence_section(data: dict[str, Any]) -> str:
    sources = data.get("sources") or []
    gaps = data.get("gaps") or []
    exceptions = data.get("exceptions") or []
    findings = data.get("additional_findings") or []
    return (
        '<section id="evidence" class="section">'
        + section_intro("11 · Provenance", "O que sabemos e o que ainda falta", "O relatório separa fatos observados, cálculos, inferências e recomendações para manter o handoff auditável.")
        + '<div class="subsection"><h3>Sources</h3><div class="grid three">'
        + cards(sources, ("id", "locator", "source_type"))
        + '</div></div><div class="grid three"><article class="card"><h3>Gaps</h3><ul class="plain-list">'
        + list_block(gaps)
        + '</ul></article><article class="card"><h3>Exceptions</h3><ul class="plain-list">'
        + list_block(exceptions)
        + '</ul></article><article class="card"><h3>Additional findings</h3><ul class="plain-list">'
        + list_block(findings)
        + "</ul></article></div></section>"
    )


def render(data: dict[str, Any], source_path: str = "design-system.json") -> str:
    meta = data.get("meta") or {}
    foundations = data.get("foundations") or {}
    colors = foundations.get("colors") or []
    primary = first_token(colors, "#6d5dfc", ("action.primary", "brand", "accent", "primary"))
    background = first_token(colors, "#101114", ("background", "surface.canvas", "surface.base"))
    foreground = first_token(colors, "#f7f8fb", ("text.primary", "foreground", "content.primary"))
    muted = first_token(colors, "#a8adbd", ("text.secondary", "muted", "content.secondary"))
    border = first_token(colors, "rgba(255,255,255,.14)", ("border", "line", "outline"))
    typography = foundations.get("typography") or {}
    family = typography.get("family") if isinstance(typography, dict) else None
    family = family or first_value(typography, "Inter, ui-sans-serif, system-ui")
    raw_json = esc(json.dumps(data, ensure_ascii=False, indent=2))
    title = meta.get("name") or "Extracted Design System"
    subtitle = meta.get("source_name") or meta.get("scope") or "Evidence-first specimen"
    css = """
      :root{--ds-primary:PRIMARY;--ds-bg:BACKGROUND;--ds-fg:FOREGROUND;--ds-muted:MUTED;--ds-border:BORDER;--ds-font:FAMILY;--ds-radius:18px;--ds-shadow:0 24px 80px rgba(0,0,0,.18);color-scheme:dark}
      *{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:radial-gradient(circle at 85% -10%,color-mix(in srgb,var(--ds-primary) 16%,transparent),transparent 36rem),var(--ds-bg);color:var(--ds-fg);font-family:var(--ds-font);line-height:1.55}a{color:inherit}button,input{font:inherit}button{cursor:pointer}.skip-link{position:fixed;left:1rem;top:-4rem;background:var(--ds-fg);color:var(--ds-bg);padding:.65rem 1rem;border-radius:999px;z-index:10}.skip-link:focus{top:1rem}.site-header{position:sticky;top:0;z-index:5;background:color-mix(in srgb,var(--ds-bg) 84%,transparent);backdrop-filter:blur(18px);border-bottom:1px solid var(--ds-border)}.header-inner{max-width:1320px;margin:auto;padding:1rem 1.4rem;display:flex;gap:1.2rem;align-items:center;justify-content:space-between}.brand{font-weight:800;letter-spacing:-.03em;text-decoration:none}.brand small{display:block;color:var(--ds-muted);font-weight:500;font-size:.7rem;letter-spacing:.02em}.nav{display:flex;gap:.6rem;overflow:auto}.nav a{color:var(--ds-muted);font-size:.78rem;text-decoration:none;white-space:nowrap;padding:.45rem .65rem;border-radius:999px}.nav a:hover,.nav a:focus-visible{color:var(--ds-fg);background:color-mix(in srgb,var(--ds-primary) 18%,transparent)}main{max-width:1320px;margin:auto;padding:0 1.4rem}.section{padding:6rem 0 1rem;scroll-margin-top:5rem}.section-intro{max-width:760px;margin-bottom:2rem}.eyebrow,.kicker{color:var(--ds-primary);font-size:.72rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase}.section h2{font-size:clamp(2rem,4vw,4.8rem);line-height:1.02;letter-spacing:-.06em;margin:.4rem 0 1rem}.section-intro p:last-child{color:var(--ds-muted);font-size:1.05rem}.hero{padding:7rem 0 3rem;display:grid;grid-template-columns:minmax(0,1.4fr) minmax(280px,.6fr);gap:2rem;align-items:end}.hero h1{font-size:clamp(3rem,8vw,8rem);line-height:.88;letter-spacing:-.09em;margin:1rem 0}.hero p{color:var(--ds-muted);max-width:650px;font-size:1.1rem}.hero-meta{border:1px solid var(--ds-border);border-radius:var(--ds-radius);padding:1.2rem;background:color-mix(in srgb,var(--ds-fg) 5%,transparent);box-shadow:var(--ds-shadow)}.hero-meta dl,.card dl,.media-meta dl,.motion-meta dl{display:grid;grid-template-columns:130px 1fr;gap:.45rem .8rem;margin:0}.hero-meta dt,.card dt,.media-meta dt,.motion-meta dt{color:var(--ds-muted);font-size:.76rem;text-transform:capitalize}.hero-meta dd,.card dd,.media-meta dd,.motion-meta dd{margin:0;overflow-wrap:anywhere}.grid{display:grid;gap:1rem}.grid.two{grid-template-columns:repeat(2,minmax(0,1fr))}.grid.three{grid-template-columns:repeat(3,minmax(0,1fr))}.card,.feature-card,.component-card,.media-card,.motion-card,.effect-card,.policy-note{border:1px solid var(--ds-border);border-radius:var(--ds-radius);background:color-mix(in srgb,var(--ds-fg) 5%,transparent);padding:1.25rem;box-shadow:0 12px 40px rgba(0,0,0,.08)}.card h3,.feature-card h3,.component-card h3,.media-card h3,.motion-card h3,.effect-card h3{margin:.35rem 0 .8rem;letter-spacing:-.03em}.feature-card{min-height:240px}.focal-card{background:linear-gradient(135deg,color-mix(in srgb,var(--ds-primary) 22%,transparent),color-mix(in srgb,var(--ds-fg) 5%,transparent))}.hero-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem}.subsection{margin-top:2.4rem}.subsection>h3{font-size:1.25rem}.badges{display:flex;gap:.4rem;flex-wrap:wrap;margin:.3rem 0 .8rem}.badge{display:inline-flex;border-radius:999px;padding:.18rem .52rem;font-size:.68rem;line-height:1.2;border:1px solid var(--ds-border);color:var(--ds-muted)}.basis-observed{color:#a9f1c4;border-color:#3c8d5b}.basis-computed{color:#9ed9ff;border-color:#3b78a0}.basis-inferred{color:#ffd28d;border-color:#9b6c2a}.basis-recommended{color:#f8a7e9;border-color:#995082}.confidence{color:var(--ds-fg)}.evidence{margin-top:1rem;color:var(--ds-muted);font-size:.72rem}.token-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:.8rem}.token-card{display:flex;gap:.8rem;align-items:flex-start;border:1px solid var(--ds-border);border-radius:14px;padding:.9rem;background:color-mix(in srgb,var(--ds-fg) 4%,transparent)}.token-card strong,.token-card code{display:block}.token-card code{font-size:.8rem;color:var(--ds-muted);margin:.25rem 0}.swatch{width:3rem;height:3rem;border-radius:12px;flex:none;border:1px solid var(--ds-border)}.plain-list{padding-left:1.2rem;color:var(--ds-muted)}.empty{border:1px dashed var(--ds-border);border-radius:14px;padding:1rem;color:var(--ds-muted)}.lab-controls{display:flex;flex-wrap:wrap;gap:.55rem;margin:1rem 0}.lab-controls button,.quiet-button,.demo-primary,.demo-secondary{border:1px solid var(--ds-border);border-radius:999px;padding:.55rem .8rem;background:transparent;color:var(--ds-fg)}.lab-controls button:hover,.lab-controls button:focus-visible,.quiet-button:hover,.quiet-button:focus-visible,.demo-secondary:hover,.demo-secondary:focus-visible{border-color:var(--ds-primary)}.demo-primary{background:var(--ds-primary);border-color:var(--ds-primary);color:white}.motion-card{overflow:hidden}.motion-stage{min-height:190px;display:grid;place-items:center;border-radius:14px;background:radial-gradient(circle at 30% 30%,color-mix(in srgb,var(--ds-primary) 35%,transparent),transparent 45%),color-mix(in srgb,var(--ds-bg) 72%,var(--ds-fg));margin-bottom:1rem}.motion-object{width:64px;height:64px;border-radius:22px;background:var(--ds-primary);box-shadow:0 18px 50px color-mix(in srgb,var(--ds-primary) 45%,transparent);animation-duration:var(--motion-duration);animation-timing-function:var(--motion-easing);animation-iteration-count:infinite;animation-direction:alternate}.motion-float{animation-name:ds-float}.motion-pulse{animation-name:ds-pulse}.is-paused .motion-object{animation-play-state:paused}.is-slow .motion-object{animation-duration:calc(var(--motion-duration) * 2)}.is-reduced .motion-object{animation:none;transform:none}.effect-stage{height:130px;border-radius:14px;display:grid;place-items:center;overflow:hidden;margin-bottom:1rem;background:linear-gradient(115deg,color-mix(in srgb,var(--ds-primary) 36%,transparent),transparent),color-mix(in srgb,var(--ds-bg) 80%,var(--ds-fg));position:relative}.effect-stage:after{content:"";position:absolute;inset:-30%;background:repeating-linear-gradient(45deg,transparent 0 8px,color-mix(in srgb,var(--ds-fg) 14%,transparent) 9px 10px);mix-blend-mode:screen;animation:ds-drift 8s linear infinite}.effect-1:after{filter:blur(12px);transform:rotate(20deg)}.effect-2:after{background:radial-gradient(circle,color-mix(in srgb,var(--ds-primary) 40%,transparent),transparent 58%);animation:ds-pulse 3s ease-in-out infinite alternate}.effect-stage span{z-index:1;font-weight:800}.is-static .effect-stage:after,.is-reduced .effect-stage:after{animation:none}.media-card{display:grid;grid-template-columns:minmax(160px,.8fr) minmax(0,1.2fr);gap:1rem}.media-visual{min-height:190px;border-radius:14px;overflow:hidden;background:color-mix(in srgb,var(--ds-bg) 80%,var(--ds-fg));display:grid;place-items:center}.media-visual img,.media-visual video{display:block;width:100%;height:100%;min-height:190px;object-fit:cover}.media-placeholder{padding:1.2rem;color:var(--ds-muted);display:grid;gap:.45rem}.media-placeholder span{color:var(--ds-primary);font-size:.72rem;text-transform:uppercase;letter-spacing:.12em}.component-card{display:grid;gap:1rem}.component-demo{min-height:120px;border-radius:14px;padding:1rem;display:flex;gap:.6rem;align-items:center;background:color-mix(in srgb,var(--ds-bg) 80%,var(--ds-fg));flex-wrap:wrap}.component-demo label{display:grid;gap:.4rem;width:100%;color:var(--ds-muted);font-size:.8rem}.component-demo input{border:1px solid var(--ds-border);border-radius:10px;padding:.7rem;background:transparent;color:var(--ds-fg);max-width:320px}.demo-nav{justify-content:flex-start}.demo-nav a{color:var(--ds-muted);text-decoration:none}.demo-card{display:grid;justify-items:start}.demo-card small{color:var(--ds-muted)}.demo-generic{justify-content:space-between}.demo-dot{width:22px;height:22px;border-radius:50%;background:var(--ds-primary)}.component-detail{border-top:1px solid var(--ds-border);padding-top:1rem;color:var(--ds-muted);font-size:.85rem}.component-detail ul{margin:.3rem 0 1rem;padding-left:1.2rem}.json-export{background:#0b0d10;color:#e8edf4;border:1px solid var(--ds-border);border-radius:14px;padding:1rem;max-height:520px;overflow:auto;font-size:.72rem}.copy-button{float:right}.footer{padding:4rem 0 6rem;color:var(--ds-muted);font-size:.8rem;border-top:1px solid var(--ds-border);margin-top:5rem}.fallback-note{color:var(--ds-muted);font-size:.75rem}button:focus-visible,a:focus-visible,input:focus-visible{outline:3px solid color-mix(in srgb,var(--ds-primary) 75%,white);outline-offset:3px}@keyframes ds-float{from{transform:translate3d(-16px,8px,0) rotate(-5deg)}to{transform:translate3d(16px,-14px,0) rotate(5deg)}}@keyframes ds-pulse{from{transform:scale(.78);border-radius:22px}to{transform:scale(1.18);border-radius:50%}}@keyframes ds-drift{from{transform:translate3d(-8%,0,0) rotate(0)}to{transform:translate3d(8%,0,0) rotate(12deg)}}@media(max-width:850px){.hero,.hero-grid,.grid.two{grid-template-columns:1fr}.grid.three{grid-template-columns:repeat(2,minmax(0,1fr))}.nav{max-width:48vw}.section{padding-top:4rem}}@media(max-width:560px){main{padding:0 1rem}.header-inner{padding:.8rem 1rem}.header-inner small{display:none}.nav{max-width:60vw}.grid.three{grid-template-columns:1fr}.media-card{grid-template-columns:1fr}.hero{padding-top:5rem}.hero h1{font-size:clamp(3.4rem,17vw,6rem)}}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}.motion-object,.effect-stage:after{animation:none!important}.motion-stage,.effect-stage{transition:none!important}}
    """
    css += ".responsive-compare{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem;margin:1rem 0 2rem}.viewport-frame{border:1px solid var(--ds-border);border-radius:var(--ds-radius);padding:1.2rem;min-height:150px;background:linear-gradient(135deg,color-mix(in srgb,var(--ds-primary) 14%,transparent),color-mix(in srgb,var(--ds-fg) 5%,transparent))}.viewport-frame strong{display:block;font-size:2rem;letter-spacing:-.05em}.viewport-frame p{color:var(--ds-muted)}@media(max-width:560px){.responsive-compare{grid-template-columns:1fr}}"
    css = css.replace("PRIMARY", safe_css(primary, "#6d5dfc")).replace("BACKGROUND", safe_css(background, "#101114")).replace("FOREGROUND", safe_css(foreground, "#f7f8fb")).replace("MUTED", safe_css(muted, "#a8adbd")).replace("BORDER", safe_css(border, "rgba(255,255,255,.14)")).replace("FAMILY", safe_css(family, "Inter, ui-sans-serif, system-ui"))
    raw_css = esc(css)
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="description" content="{esc(title)} — living design-system report" />
  <title>{esc(title)} · Design System Report</title>
  <style>{css}</style>
</head>
<body id="overview">
  <a class="skip-link" href="#main">Pular para o conteúdo</a>
  <header class="site-header"><div class="header-inner">
    <a class="brand" href="#overview">{esc(title)}<small>{esc(subtitle)}</small></a>
    <nav class="nav" aria-label="Report sections">
      <a href="#identity">Identity</a><a href="#foundations">Foundations</a><a href="#responsive">Responsive</a><a href="#media">Media</a><a href="#motion">Motion</a><a href="#effects">Effects</a><a href="#components">Components</a><a href="#evidence">Evidence</a>
    </nav>
  </div></header>
  <main id="main">
    <section class="hero"><div><p class="eyebrow">Living design-system report · schema {esc((meta.get("schema_version") or 1))}</p><h1>{esc(title)}</h1><p>{esc(meta.get("method_summary") or "Um espécime vivo para entender identidade, tokens, estados, mídia, motion e evidências.")}</p><p class="fallback-note">Fonte: {esc(source_path)} · fallback do relatório é explicitamente separado da extração.</p></div>
      <aside class="hero-meta"><dl>{detail_rows(meta)}</dl><div class="badges"><span class="badge basis-observed">evidence-first</span><span class="badge confidence">{esc(meta.get("overall_confidence") or "unknown")} confidence</span></div></aside>
    </section>
    {experience_section(data)}
    {foundations_section(data)}
    {responsive_section(data)}
    <section id="patterns" class="section">{section_intro("05 · Patterns", "Composições que se repetem", "Shell, templates e hierarquia de página tornam o sistema reconhecível antes de qualquer componente.")}<div class="grid three">{cards(data.get("patterns"), ("name", "label", "template"))}</div></section>
    {media_section(data)}
    {motion_section(data)}
    {effect_section(data)}
    <section id="components" class="section">{section_intro("09 · Components", "Anatomia, estados e conteúdo", "Cada componente deve carregar suas variantes, limites, estados acessíveis e evidências.")}<div class="grid three">{components_section(data)}</div></section>
    {accessibility_section(data)}
    {evidence_section(data)}
    <section id="export" class="section">{section_intro("12 · Export", "Contract payload", "O JSON continua sendo a fonte de verdade para design-to-code e auditoria.")}<button class="lab-controls copy-button" type="button" data-copy-json>Copy JSON</button><pre class="json-export"><code>{raw_json}</code></pre><h3>Report CSS fallback</h3><button class="lab-controls copy-button" type="button" data-copy-css>Copy CSS</button><pre class="json-export"><code>{raw_css}</code></pre></section>
  </main>
  <footer class="footer"><div class="header-inner"><span>Generated by Extract Web Design System.</span><span>Observed · computed · inferred · recommended.</span></div></footer>
  <script>
    (() => {{
      const body = document.body;
      const replay = () => {{
        body.classList.remove("is-paused");
        document.querySelectorAll(".motion-object").forEach((node) => {{
          node.style.animation = "none";
          void node.offsetWidth;
          node.style.animation = "";
        }});
      }};
      document.querySelectorAll("[data-motion-action]").forEach((button) => button.addEventListener("click", () => {{
        const action = button.dataset.motionAction;
        if (action === "replay") replay();
        if (action === "pause") body.classList.toggle("is-paused");
        if (action === "slow") body.classList.toggle("is-slow");
        if (action === "reduce") body.classList.toggle("is-reduced");
      }}));
      document.querySelectorAll("[data-media-toggle]").forEach((button) => button.addEventListener("click", () => {{
        const video = document.getElementById(button.dataset.mediaToggle);
        if (!video) return;
        if (video.paused) video.play().catch(() => {{}}); else video.pause();
      }}));
      document.querySelectorAll(".effect-card").forEach((card) => card.addEventListener("dblclick", () => body.classList.toggle("is-static")));
      const copy = document.querySelector("[data-copy-json]");
      if (copy) copy.addEventListener("click", async () => {{
        await navigator.clipboard?.writeText(document.querySelector(".json-export").innerText);
        copy.textContent = "Copied";
        setTimeout(() => copy.textContent = "Copy JSON", 1300);
      }});
      const copyCss = document.querySelector("[data-copy-css]");
      if (copyCss) copyCss.addEventListener("click", async () => {{
        const blocks = document.querySelectorAll(".json-export");
        await navigator.clipboard?.writeText(blocks[blocks.length - 1].innerText);
        copyCss.textContent = "Copied";
        setTimeout(() => copyCss.textContent = "Copy CSS", 1300);
      }});
    }})();
  </script>
</body>
</html>
"""


def main() -> int:
    if len(sys.argv) not in (2, 3):
        print("Usage: render_design_system_report.py DESIGN_SYSTEM.json [OUTPUT.html]")
        return 2
    source = Path(sys.argv[1])
    if not source.is_file():
        print(f"ERROR: file not found: {source}", file=sys.stderr)
        return 2
    try:
        data = json.loads(source.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        print(f"ERROR: invalid JSON: {error}", file=sys.stderr)
        return 2
    output = render(data, str(source))
    if len(sys.argv) == 3:
        Path(sys.argv[2]).write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
