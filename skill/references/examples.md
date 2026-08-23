# Usage examples and edge cases

## Live site, full audit

Prompt: “Analyze these three product routes and make a page documenting the complete design system.”

Expected behavior: map route families; capture desktop/mobile plus safe states; inspect computed styles, variables, fonts, components, motion, and accessibility; normalize tokens with evidence/confidence; generate the manifest and living report; state inaccessible states.

## Screenshot-only extraction

Prompt: “I only have these four screenshots. Extract everything possible and create the system page.”

Expected behavior: measure visible colors, hierarchy, spacing, grids, radii, shadows, imagery, and matched responsive differences; describe hover/focus/motion/font identity as unknown or candidate; label scale-dependent measurements as estimates; do not fabricate hidden states.

## Computer-use flow

Prompt: “Use the logged-in staging site and inspect the dashboard, filters, modal, and settings.”

Expected behavior: navigate only within authorization; avoid save/delete/send/purchase; capture open/closed, focus, validation-before-submit, loading if safely reachable, and responsive states; redact private/customer data from evidence.

## Recording supplied for motion

Prompt: “These clips show the interactions. Reconstruct the motion language.”

Expected behavior: use frame/timestamp evidence to estimate start, delay, duration, settle, stagger, and reversal; distinguish measured ranges from exact CSS timing; create replay/pause/slow/reduced-motion specimens.

## Source and production disagree

Preserve `specified` source tokens and `implemented` runtime values. Identify overrides, stale tokens, or experiments only when evidenced. Make the living report default to implemented behavior unless the user requests the intended specification.

## Inconsistent spacing

Do not force every gap onto an 8 px scale. Cluster repeated values, preserve optical exceptions, and explicitly conclude that no consistent scale exists when evidence supports it.

## Protected brand content

Extract layout, color roles, typography characteristics, component grammar, and motion. Replace logos, marketing copy, product photos, and proprietary illustrations with neutral labeled specimens unless reuse is authorized.

## Useful extra findings

The taxonomy is a floor. Add localization expansion behavior, cursor language, haptics-equivalent feedback, skeleton rhythm, data-visualization grammar, editorial image direction, density modes, theme transition strategy, or performance-related visual compromises under `additional_findings` when they materially explain the system.


## 9. Experience/media examples

### Background video observed

~~~json
{
  "id": "media-hero-loop",
  "kind": "video",
  "role": "hero-background",
  "playback": {
    "autoplay": true,
    "muted": true,
    "loop": true,
    "playsinline": true
  },
  "fallback": {
    "poster": "./evidence/hero-poster.jpg",
    "reduced_motion": "poster only"
  },
  "basis": "observed",
  "confidence": "medium",
  "evidence_ids": ["E-runtime-hero-media-001"]
}
~~~

This supports “the video element was observed in this state.” It does not prove that every viewport autoplays or that the same behavior persists offscreen.

### Background video recommended

~~~json
{
  "id": "media-mobile-poster",
  "kind": "video",
  "role": "hero-background",
  "fallback": {
    "low_bandwidth": "poster only",
    "data_saver": "poster only"
  },
  "basis": "recommended",
  "confidence": "low",
  "rationale": "Protect battery, bandwidth and text legibility on small screens."
}
~~~

Keep the recommendation separate from extracted source truth.

### Canvas/pointer effect with fallback

~~~json
{
  "id": "effect-cursor-glow",
  "kind": "cursor-glow",
  "target": "hero",
  "driver": "pointer",
  "fallback": "static radial gradient",
  "performance": "requestAnimationFrame-throttled",
  "basis": "inferred",
  "confidence": "low",
  "evidence_ids": ["E-source-runtime-probe-001"]
}
~~~

A runtime snapshot can reveal canvas or event hints; interaction sampling is still required to establish the trigger.

### Screenshot-only and recording-only

- Screenshot-only evidence can support crop, hierarchy, color, spacing and apparent composition. It cannot prove playback, hover, focus, scroll trigger, DOM semantics or exact font loading.
- Recording-only evidence can support timing, loop continuity, sequence and visible trigger context. It may not prove source tokens, full route coverage, keyboard behavior or offscreen performance.

### Media inaccessible

If the media URL is blocked, protected, cross-origin inaccessible or unavailable:

1. record the URL/locator as metadata;
2. preserve the limitation in sources[].limitations and gaps[];
3. use a local poster/still only when authorized;
4. never replace observed media with a guessed asset;
5. keep playback, crop and performance claims at low confidence until new evidence exists.

