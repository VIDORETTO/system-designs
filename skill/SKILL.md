---
name: extract-web-design-system
description: Extract, infer, audit, and document a website's complete visual and interaction design system from a live URL, browser/computer-use session, screenshots, screen recordings, or source files, then build a responsive self-demonstrating web page that uses the extracted system. Use for design-system archaeology, website style audits, UI inventories, brand/token extraction, motion and interaction analysis, responsive behavior reconstruction, accessibility-informed visual documentation, screenshot-to-design-system work, or recreating a reference site's design language without copying protected content.
---

# Extract Web Design System

Reconstruct the system behind a website, not merely the appearance of one screenshot. Produce traceable evidence, reusable tokens, behavior rules, component anatomy, confidence levels, and a living specimen page that explains the system by using it.

## Operating principles

1. Separate **observed**, **computed**, **inferred**, and **recommended** facts. Never present an inference as source truth.
2. Prefer repeated patterns over isolated values. A design system is a grammar, not a dump of every CSS declaration.
3. Capture time, state, viewport, and context. Static screenshots cannot prove hover, focus, animation, or breakpoint behavior.
4. Preserve provenance. Every important claim must point to a URL, screenshot, DOM/CSS inspection, recording interval, or source file.
5. Assign `high`, `medium`, or `low` confidence and explain low-confidence gaps.
6. Respect authorization, privacy, robots/access controls, trademarks, and copyright. Extract rules and patterns; do not clone proprietary copy, imagery, logos, or hidden data unless explicitly authorized.
7. Allow emergent findings. Add an `additional_findings` section for meaningful patterns outside the expected taxonomy.

## Select the acquisition route

Use every user-supplied source and combine routes when possible:

| Input | Primary method | Important limitation |
| --- | --- | --- |
| Live public URL | Browser inspection, screenshots, computed styles, interaction sampling | Inspect representative routes and states, not only the home page |
| Authenticated or stateful site | Computer use with user-approved session | Do not expose secrets or take irreversible actions |
| Screenshots | Visual measurement and cross-image comparison | Mark behavior, fonts, breakpoints, and off-screen structure as inferred |
| Screen recording | Frame/timeline analysis plus screenshots | Measure durations from frames; account for capture frame rate |
| Source repository/build | Static analysis plus local rendering | Runtime may differ from source; verify in browser |
| Design files or style guide | Token/component inspection plus implementation comparison | Document divergence between specification and production |

Read [acquisition-playbook.md](references/acquisition-playbook.md) before capturing a live site, using screenshots, or operating a browser. It contains the coverage matrix, motion protocol, evidence rules, and stop conditions.

## Execute the workflow

### 1. Define scope and fidelity

Record:

- target URLs or supplied artifacts;
- intended output stack: single HTML by default, or the user's framework;
- target viewports, themes, routes, locales, and logged-in states;
- whether the goal is documentation, implementation guidance, migration, or visual comparison;
- inaccessible areas and assumptions.

If scope is underspecified, choose a representative minimum: home/landing, one content/list page, one detail/form page, navigation open/closed, and mobile/desktop. Expand when the site exposes materially different patterns.

### 2. Build a capture plan

Inventory route families and choose pages that maximize unique components and states. Define a matrix across:

- viewports: narrow mobile, wide mobile, tablet, desktop, wide desktop where relevant;
- themes and modes;
- default, hover, focus-visible, active, selected, disabled, loading, empty, error, success, open, and scrolled states;
- navigation, overlays, forms, content density, and media behavior;
- motion start, intermediate, end, interruption, and reduced-motion behavior.

Do not browse randomly. Capture each matrix cell with an evidence ID.

### 3. Acquire evidence

Collect, when available:

- full-page and component screenshots with viewport dimensions and device scale;
- DOM hierarchy, accessibility roles/names, pseudo-elements, computed styles, and CSS custom properties;
- loaded font families, files, weights, variable axes, fallbacks, icons, and image treatment;
- layout dimensions, gaps, max widths, alignment anchors, grids, stacking contexts, and overflow;
- interactions, transitions, keyframes, easing, delays, stagger, scroll behavior, and reduced-motion response;
- responsive changes across matched elements, not just separate screenshots;
- console/runtime warnings relevant to UI behavior.

Never bypass access controls. When computer use is required, avoid submitting forms, purchases, deletions, messages, or other consequential actions unless the user explicitly requested them.

### 4. Normalize into a design grammar

Cluster near-duplicate raw values into semantic tokens while retaining raw values in evidence. Infer:

- foundations: color roles, typography, spacing, sizing, grids, radii, borders, shadows, opacity, z-index, iconography, imagery;
- responsive rules: breakpoints, container behavior, fluid/clamped values, reflow/hide/reorder/substitute rules;
- motion: duration tiers, easing families, choreography, triggers, interruption, and reduced-motion alternatives;
- components: anatomy, variants, sizes, states, content constraints, composition rules, and accessibility behavior;
- page patterns: shell, sections, density, hierarchy, and recurring templates;
- voice/content style only when enough evidence exists.

Prefer semantic names such as `color.surface.elevated` over source-specific names such as `gray-50`. Preserve aliases when source variables are visible.

### 5. Reconcile contradictions

When values conflict:

1. Check whether the difference is state, theme, breakpoint, component variant, or one-off exception.
2. Prefer repeated runtime evidence over a single declaration.
3. Keep intentional exceptions explicit.
4. If unresolved, retain both observations and lower confidence; do not average unrelated values.

### 6. Write the extraction contract

Create `design-system.json` following [extraction-schema.md](references/extraction-schema.md). Keep the manifest machine-readable and include evidence IDs, confidence, gaps, and `additional_findings`.

Run:

```bash
python3 scripts/validate_design_system.py design-system.json
```

Fix errors. Treat warnings as review prompts, not automatic failures.

### 7. Build the living design-system page

Read [report-spec.md](references/report-spec.md). Build a responsive page that both documents and visibly uses the extracted system. Default sections:

1. Executive summary, scope, fidelity, confidence, and source coverage
2. Brand/visual principles and design DNA
3. Color, typography, spacing, sizing, grid, radii, borders, shadows, and icons
4. Responsive rules with matched examples
5. Motion lab with replay, pause, slow mode, and reduced-motion demonstration
6. Component gallery with variants and interactive states
7. Page patterns/composition examples
8. Accessibility and content behavior
9. Evidence, uncertainties, exceptions, and additional findings
10. Copyable CSS variables and optional framework tokens

The report must use extracted tokens in its own CSS. Do not make a neutral documentation shell that merely displays swatches. Visually distinguish observed facts from inferences and recommendations.

For a fast single-file artifact, run:

```bash
python3 scripts/render_design_system_report.py design-system.json report.html
```

Use the generated page as a baseline, then enrich it when the user's stack or fidelity requires custom components.

### 8. Verify

Render and inspect the final page at the target viewports. Verify:

- no overflow, clipping, broken contrast, missing fonts, or unusable controls;
- token examples match their labels and values;
- interactive states work by keyboard and pointer;
- animations expose controls and honor `prefers-reduced-motion`;
- claims map to evidence and uncertainty is visible;
- the page itself follows the extracted layout, type, color, shape, and motion grammar;
- protected source content has not been copied unnecessarily.

If a reference and output can be rendered at matching dimensions, perform a visual comparison. Describe material differences rather than claiming pixel perfection without evidence.

## Required deliverables

Unless the user narrows scope, produce:

- `design-system.json`: normalized system plus evidence and confidence;
- `report.html` or a framework project: living documentation page;
- `evidence/`: screenshots or references used, when permissible;
- concise handoff: coverage, strongest findings, unresolved gaps, and how to rerun.

Do not fabricate missing assets. Use labeled placeholders or abstract specimens when source imagery/logos cannot be reused.
For source-only work, provenance inside `design-system.json` is sufficient; create `evidence/` only when there are separate screenshots, recordings, extracts, or other permissible evidence files to preserve.

## Quality gates

Do not call the extraction complete unless:

- at least two materially different viewports were rendered and assessed, or the limitation is explicit. Source-defined media/container ranges may support responsive rules but do not count as rendered viewport assessment;
- interactive claims come from interaction/recording/source evidence;
- colors include roles and contrast context, not just hex values;
- typography includes family, weight, size, line height, tracking, and usage roles where observable;
- spacing and sizing identify a scale or explicitly state that no consistent scale exists;
- motion includes trigger, duration, easing, properties, and reduced-motion handling where observable;
- components include anatomy, variants, states, and content behavior;
- major claims carry evidence and confidence;
- the report uses the extracted system and survives responsive/keyboard/reduced-motion checks.

## Examples and edge cases

Read [examples.md](references/examples.md) for trigger examples, screenshot-only behavior, authenticated flows, contradictory values, and expected outputs.


## Experience Layer: identity, elements, media, effects

For expressive, editorial, product-storytelling, or cinematic sites, add an Experience Layer before normalizing tokens. It prevents a generic component inventory from erasing the reason the site feels distinctive.

Capture:

- identity lock: one concise thesis, sensory words, anti-generic constraints, and supporting evidence;
- focal moment: the first impression or reveal that carries the experience;
- signature elements: material, anatomy, role, layer relationship, and protection rules;
- named rules: reusable rules such as “media behind the reading plane” or “one focal gesture”;
- media assets: kind, role, locator, crop, object position, scrim, blend, text-safe zone, playback, fallback, performance, and evidence;
- effects: grain, blur, blend, gradient, canvas, shader, parallax, pointer response, and the driver/job/fallback for each;
- motion jobs: feedback, continuity, hierarchy, atmosphere, navigation, state, or delight.

Use the static candidate probe for source files:

    python3 skill/scripts/probe_media_inventory.py SOURCE --output inventory.json

Use skill/scripts/runtime_media_probe.js in an authorized browser session to record current DOM media, computed composition, playback state, resource timing, active Web Animations, canvas signals, and limitations. A runtime snapshot does not prove trigger semantics; sample load, scroll, pointer, focus, open/close, and reduced-motion states separately.

When an authorized video file is available, use:

    python3 skill/scripts/extract_video_frames.py VIDEO OUTPUT_DIR --count 6

Treat frame extraction as computed evidence. It helps inspect crop, focal stability, loop continuity, and text-safe zones; it does not prove every playback state.

### Background video policy

A background video is valid only when its purpose is explicit and the contract records:

- autoplay, muted, loop, playsinline and preload;
- poster and reduced-motion/static fallback;
- no essential information baked only into frames;
- text-safe composition, crop/object-position, scrim/overlay and layer order;
- offscreen pause/release strategy and a weight/format target;
- mobile/data-saver behavior;
- evidence ID plus whether playback was observed, inferred, or recommended.

The report must not autoplay remote or protected media. It can preview local authorized evidence, otherwise it shows a neutral placeholder and the metadata.

### Schema v2 and compatibility

meta.schema_version: 2 enables the optional experience, elements, media, and effects sections. Legacy manifests remain valid when those sections are absent. Run skill/scripts/validate_design_system.py before rendering; P0/P1 quality issues block handoff, while P2/P3 items become explicit follow-up work.

The living report now includes identity, signature elements, media composition, effects, motion controls, component specimens, accessibility/content, evidence, gaps, and JSON export. Use the report as a specimen, not as a license to copy protected assets or copy.


## Production browser gate

The browser layer is now executable, not only a console recipe.

Use the pinned Playwright runner:

    npm install
    npx playwright install chromium
    npm run capture:browser
    npm run validate:browser
    npm run visual:regression

The runner captures every configured target at desktop/mobile and normal/reduced-motion states, writes screenshots, records page/request errors, and evaluates runtime_media_probe.js in the page context. Keep live-site configs private and authorized.

The GitHub workflow in .github/workflows/design-system-quality.yml runs static validation, renderer smoke checks, browser capture and visual-regression reporting. The checked-in experience-layer fixture has a reviewed desktop/mobile normal/reduced-motion baseline; new targets may report baseline-pending only during an authorized bootstrap and are never treated as pixel parity.

