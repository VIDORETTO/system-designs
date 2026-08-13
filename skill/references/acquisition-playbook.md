# Acquisition playbook

## Contents

1. Evidence model
2. Coverage planning
3. Live-site procedure
4. Screenshot procedure
5. Recording and motion procedure
6. Source/design-file procedure
7. Measurement heuristics
8. Stop conditions

## 1. Evidence model

Give each source an ID such as `E-live-home-desktop-001` or `E-shot-mobile-nav-open-002`. Record:

- source type and locator;
- capture time;
- URL/route or filename;
- viewport width, height, DPR, zoom, theme, locale, auth state;
- UI state and interaction used to reach it;
- crop/component identity;
- tool/method;
- notes and limitations.

For every claim, set `basis`:

- `observed`: directly visible or inspected;
- `computed`: derived deterministically from evidence, such as contrast or measured duration;
- `inferred`: best explanation of multiple observations;
- `recommended`: proposed improvement, never attributed to the source.

Confidence rubric:

- `high`: repeated direct evidence, source token, or matched runtime measurement;
- `medium`: consistent across limited samples or strongly supported inference;
- `low`: screenshot estimate, single occurrence, inaccessible state, or ambiguous cause.

## 2. Coverage planning

Select routes by component diversity rather than traffic guesses. Seek:

- global shell and navigation;
- dense list/table/card collection;
- detail/editor/form;
- overlay/dialog/drawer/menu;
- empty/error/loading/success feedback;
- footer and long-content behavior;
- mobile substitution patterns.

Minimum viewport set when not specified:

- 390×844 mobile;
- 768×1024 tablet when layout visibly changes;
- 1440×900 desktop.

Probe around suspected breakpoints. A breakpoint is supported when the same element changes at bounded widths; it is not proven merely because two screenshots differ.
Source-defined media/container queries are exact implementation evidence, but do not prove the rendered result. Record them as source observations and keep runtime verification as a gap until the relevant widths are rendered.

## 3. Live-site procedure

1. Capture the initial page before interaction.
2. Record page title, URL, viewport, theme, and visible route landmarks.
3. Inspect root/body variables, font loading, page container, primary grid, and global focus style.
4. Traverse representative components and record computed styles for matched states.
5. Exercise safe interactions: hover, focus, open/close, tabs, accordions, carousels, validation without submission, and scroll.
6. Capture pseudo-elements and portaled overlays; they are commonly missed by DOM-local inspection.
7. Repeat representative pages at matched viewports.
8. Test keyboard traversal and reduced motion if controllable.
9. Record inaccessible or unstable states as gaps.

When CSS custom properties exist, preserve original names and resolved values. Do not assume every source variable is a public semantic token; classify aliases and one-off implementation variables separately.

## 4. Screenshot procedure

Calibrate using known viewport dimensions or stable browser chrome when available. For each screenshot:

- identify likely viewport and crop status;
- sample colors away from antialiased edges, shadows, and compression artifacts;
- estimate typography from cap height, line box, and repeated hierarchy—not a single glyph;
- measure repeated gaps and cluster them rather than forcing a scale;
- distinguish actual borders from shadow edges and compression halos;
- note occluded, clipped, or below-fold content;
- compare matched components across images.

Never claim exact font family, CSS breakpoint, duration, easing, hover, focus, or DOM semantics from a single static screenshot. Provide candidates or observed appearance with low/medium confidence.

## 5. Recording and motion procedure

Record or inspect at a known frame rate. Mark trigger frame, first changed frame, settling frame, and any overshoot. Capture:

- trigger and target;
- delay and duration range;
- changed properties;
- likely easing shape;
- entering/exiting asymmetry;
- parent/child stagger;
- scroll linkage;
- interruption/reversal behavior;
- reduced-motion alternative.

Prefer transforms and opacity descriptions only when the evidence supports them. A visual fade may also include blur, color, clipping, or mask changes.

Do not repeatedly trigger flashing or high-motion effects. Stop if interaction could cause a purchase, submission, destructive mutation, or account change.

## 6. Source/design-file procedure

Search for:

- CSS variables, theme objects, token packages, Tailwind/theme config;
- font declarations and assets;
- animation/keyframe definitions;
- component variants and state selectors;
- breakpoint/media/container queries;
- icon libraries and image pipelines;
- accessibility helpers and reduced-motion branches.

Render representative runtime pages because dead styles, overrides, experiments, and route-specific bundles may misrepresent actual use. When a design file and production disagree, document both as `specified` and `implemented`.

## 7. Measurement heuristics

- Color: cluster perceptually similar values only when their role and contexts agree.
- Spacing: seek a small generating scale plus documented exceptions; do not round away real optical adjustments.
- Typography: separate text style roles from raw font sizes.
- Radius: classify by component role; pills often use a semantic full radius rather than the numeric scale.
- Shadow: record x/y, blur, spread, color/opacity, and elevation context.
- Grid: distinguish viewport gutters, content max width, columns, tracks, and component-local grids.
- Motion: report measured ranges when frame timing or throttling introduces uncertainty.
- Components: use repeated anatomy and behavior, not class names alone.

## 8. Stop conditions

Pause and report a gap when:

- authentication or permission is missing;
- a CAPTCHA, paywall, or access control blocks progress;
- safe interaction cannot reach a required state;
- evidence conflicts materially and no route can resolve it;
- requested extraction would expose private data or copy protected content beyond the user's authorization;
- the available screenshots cannot support the requested fidelity.

Continue with accessible evidence and clearly bound conclusions instead of inventing missing details.
