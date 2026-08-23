# Extraction contract

## Contents

1. Contract rules
2. Top-level shape
3. Evidence and claims
4. Foundations
5. Responsive and motion
6. Components and patterns
7. Minimal example

## 1. Contract rules

Use JSON. Keep stable IDs. Store normalized token values separately from evidence. Every material token family, component, responsive rule, and motion pattern should have `basis`, `confidence`, and `evidence_ids` directly or through a parent claim.

Allowed enums:

- `basis`: `observed`, `computed`, `inferred`, `recommended`
- `confidence`: `high`, `medium`, `low`
- `source_type`: `live`, `screenshot`, `recording`, `source`, `design-file`, `user-note`

Use `null` for unknown scalar values and `[]` for known-empty collections. Do not encode guesses as exact values.

## 2. Top-level shape

```json
{
  "meta": {},
  "sources": [],
  "principles": [],
  "foundations": {},
  "responsive": {},
  "motion": {},
  "components": [],
  "patterns": [],
  "accessibility": {},
  "content_style": {},
  "exceptions": [],
  "gaps": [],
  "additional_findings": [],
  "generated_assets": {}
}
```

Required `meta` fields: `name`, `source_name`, `generated_at`, `scope`, `fidelity_target`, `overall_confidence`, and `method_summary`.

Each `sources[]` item should include `id`, `source_type`, `locator`, `captured_at`, `context`, and `limitations`.

## 3. Evidence and claims

Reusable claim shape:

```json
{
  "id": "claim-color-primary",
  "label": "Primary action color",
  "value": "#5B5BD6",
  "basis": "observed",
  "confidence": "high",
  "evidence_ids": ["E-live-home-desktop-001"],
  "notes": "Repeated on primary buttons and active navigation."
}
```

Evidence references must resolve to `sources[].id`. Recommendations may have no source evidence but must explain their rationale and must not be mixed into extracted tokens.

## 4. Foundations

Recommended collections:

- `foundations.colors`: semantic token, raw value, modes, usage, contrast pairs
- `foundations.typography`: families, files/candidates, axes, styles, roles, fallbacks
- `foundations.spacing`: primitive scale, semantic aliases, exceptions
- `foundations.sizing`: control heights, icon sizes, content widths
- `foundations.grid`: viewport gutters, max widths, columns/tracks, gaps
- `foundations.radii`, `borders`, `shadows`, `opacity`, `z_index`
- `foundations.iconography`: library/candidate, stroke/fill, sizes, alignment
- `foundations.imagery`: ratio, crop, treatment, overlays, illustration/photo language

Token example:

```json
{
  "token": "color.action.primary",
  "value": "#5B5BD6",
  "modes": {"dark": "#7C7CF0"},
  "usage": ["primary button", "active link"],
  "basis": "observed",
  "confidence": "high",
  "evidence_ids": ["E-live-home-desktop-001"]
}
```

Typography styles should include `family`, `weight`, `size`, `line_height`, `letter_spacing`, `transform`, and `usage` when observable.

## 5. Responsive and motion

`responsive` should include observed ranges or breakpoint candidates, container behavior, per-element transformations, and fluid values. Keep inferred `clamp()` expressions separate from proven media/container queries.

`motion` should include duration tiers and raw measurements; easing families or candidates; transition trigger, properties, delay, duration, easing, choreography; interruption/reversal behavior; reduced-motion behavior; and performance observations.

Never encode `ease-out` as observed from screenshots alone.

## 6. Components and patterns

Each component should include `id`, `name`, `role`, `anatomy`, `variants`, `sizes`, `states`, `tokens_used`, `content_rules`, `responsive_behavior`, `interaction`, `accessibility`, and provenance fields.

Each page pattern should include shell/regions, hierarchy, density, composition rules, responsive transformation, and representative evidence.

Use `exceptions` for intentional one-offs and contradictions. Use `gaps` for unavailable states or unsupported conclusions. Use `additional_findings` for important patterns not represented elsewhere.

`generated_assets` should identify the report filename, framework, and any token/code outputs.

## 7. Minimal example

```json
{
  "meta": {
    "name": "Example UI System",
    "source_name": "Example product",
    "generated_at": "2026-08-13T12:00:00Z",
    "scope": ["landing", "navigation"],
    "fidelity_target": "system-level",
    "overall_confidence": "medium",
    "method_summary": "Two screenshots and one live desktop route"
  },
  "sources": [{
    "id": "E-live-home-001",
    "source_type": "live",
    "locator": "https://example.com/",
    "captured_at": "2026-08-13T11:00:00Z",
    "context": {"viewport": "1440x900", "theme": "light"},
    "limitations": []
  }],
  "principles": [],
  "foundations": {
    "colors": [{
      "token": "color.action.primary",
      "value": "#5B5BD6",
      "usage": ["primary button"],
      "basis": "observed",
      "confidence": "high",
      "evidence_ids": ["E-live-home-001"]
    }],
    "typography": [], "spacing": [], "sizing": [], "grid": [],
    "radii": [], "borders": [], "shadows": [], "opacity": [],
    "z_index": [], "iconography": [], "imagery": []
  },
  "responsive": {"rules": []},
  "motion": {"patterns": [], "reduced_motion": null},
  "components": [], "patterns": [], "accessibility": {},
  "content_style": {}, "exceptions": [],
  "gaps": ["Mobile interaction states not supplied"],
  "additional_findings": [],
  "generated_assets": {"report": "report.html", "framework": "single-html"}
}
```


## 8. Schema v2: Experience Layer

The v1 contract remains valid. Add meta.schema_version: 2 when using the optional experience layer.

~~~json
{
  "meta": {
    "schema_version": 2
  },
  "experience": {
    "surface_mode": "experience",
    "identity_lock": {
      "summary": "Calm, tactile, cinematic product confidence.",
      "thesis": "A quiet studio where the interface feels like a material object coming into focus.",
      "sensory_words": ["calm", "tactile", "precise"],
      "anti_generic": ["Do not flatten the focal media into a generic gradient."],
      "basis": "inferred",
      "confidence": "medium",
      "evidence_ids": ["E-live-home-desktop-001"]
    },
    "focal_moment": {
      "name": "Hero reveal",
      "description": "The headline becomes legible as the background loop settles.",
      "basis": "observed",
      "confidence": "medium",
      "evidence_ids": ["E-runtime-hero-media-001"]
    },
    "signature_elements": [],
    "named_rules": [],
    "dos": [],
    "donts": [],
    "recommendations": []
  },
  "elements": [],
  "media": {
    "policy": {},
    "assets": []
  },
  "effects": []
}
~~~

### Media asset shape

~~~json
{
  "id": "media-hero-loop",
  "label": "Hero atmospheric loop",
  "kind": "video",
  "role": "hero-background",
  "url": "media/hero-loop.webm",
  "poster": "./evidence/hero-poster.svg",
  "playback": {
    "autoplay": true,
    "muted": true,
    "loop": true,
    "playsinline": true,
    "preload": "metadata",
    "pause_when_offscreen": true
  },
  "composition": {
    "layer": "behind-content",
    "object_fit": "cover",
    "object_position": "62% 44%",
    "scrim": "linear-gradient(...)",
    "safe_text_zone": "left 42%"
  },
  "fallback": {
    "poster": "./evidence/hero-poster.svg",
    "reduced_motion": "static poster",
    "low_bandwidth": "poster only"
  },
  "performance": {
    "max_bytes_target": 2400000,
    "offscreen": "pause and release decoder"
  },
  "basis": "observed",
  "confidence": "medium",
  "evidence_ids": ["E-runtime-hero-media-001"]
}
~~~

Do not put essential content only in video frames. A background asset must have a poster or static fallback, and autoplay must be muted and inline. Capture remote URLs as metadata; preview only local authorized evidence in the report.

### Effect and motion shape

~~~json
{
  "id": "effect-pointer-glow",
  "kind": "cursor-glow",
  "target": "hero",
  "driver": "pointer",
  "job": "atmosphere",
  "fallback": "static radial gradient",
  "performance": "requestAnimationFrame-throttled",
  "basis": "recommended",
  "confidence": "low"
}
~~~

Motion patterns should include trigger, driver, job, properties, duration/easing when known, performance, and a reduced_motion alternative. observed, inferred, and recommended media/effects must remain distinct.

### Migration notes

- v1 consumers can ignore the new optional fields.
- v2 consumers should show a P2 quality issue when experience is absent.
- media.assets[] is the canonical media inventory; generated_assets remains for report/evidence outputs.
- Use gaps[] when a browser state, asset, trigger, or reduced-motion capture is unavailable.
