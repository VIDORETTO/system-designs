# Living report specification

## Contents

1. Purpose
2. Information architecture
3. Self-demonstration rule
4. Interaction and motion lab
5. Responsive behavior
6. Accessibility
7. Evidence communication
8. Technical delivery
9. Acceptance checklist

## 1. Purpose

Build a page that explains the extracted design system by embodying it. The report is both documentation and a specimen. It must remain clear where the source system ends and the report author's recommendations begin.

## 2. Information architecture

Use a sticky or compact navigation appropriate to the extracted system. Recommended sections:

- overview and system DNA;
- source coverage and confidence;
- foundations;
- responsive behavior;
- motion lab;
- components and states;
- compositions/page patterns;
- accessibility/content behavior;
- evidence, exceptions, gaps, and additional findings;
- implementation exports.

Show a short “how to read this” legend for basis and confidence.

## 3. Self-demonstration rule

Bind report CSS variables to extracted semantic tokens. Use extracted typography, spacing, radii, borders, shadows, grid tendencies, and motion tiers throughout the shell. If a token is missing or unsafe for documentation readability:

1. use an explicit report fallback;
2. label it as a fallback;
3. do not add it to the extracted system.

Do not imitate protected brand marks or copy site text. Use neutral specimen content that tests realistic lengths, wrapping, errors, and empty states.

For each token, show semantic name, value, role, basis, confidence, and evidence links/IDs. Allow copying values where practical.

## 4. Interaction and motion lab

Provide controls to replay, pause, and slow motion patterns. Include a reduced-motion mode or explain if source behavior is unavailable. Motion samples should display trigger, delay/duration/easing, animated properties, enter/exit relationship, choreography/stagger, and evidence/confidence.

Avoid autoplaying distracting loops. Respect system `prefers-reduced-motion` by default.

Component specimens should expose keyboard-reachable controls for variants and states. Do not fake native focus with a static picture when an interactive example is feasible.

## 5. Responsive behavior

Use real responsive layout, not scaled desktop screenshots. Document transformations such as reflow, hide/show, order change, replacement, density shift, and container changes.

When useful, provide matched before/after specimens for the same component. Label breakpoint values as exact only when source/runtime evidence supports them; otherwise show an observed range.

## 6. Accessibility

The report should meet a practical documentation baseline:

- semantic landmarks and heading order;
- keyboard access and visible focus;
- controls with accessible names;
- sufficient report-level contrast or disclosed source contrast failures;
- text alternatives for meaningful evidence images;
- no color-only status encoding;
- reduced-motion support;
- readable zoom/reflow at 200% where feasible.

Do not silently “fix” source accessibility inside extracted examples. Clearly label source behavior and separately label recommendations.

## 7. Evidence communication

Use visual badges or labels for Observed, Computed, Inferred, and Recommended. Also show High/Medium/Low confidence without relying only on color. Allow users to trace a finding to an evidence ID and source context. Include capture limitations and inaccessible states.

## 8. Technical delivery

Default to a self-contained `report.html` when the user does not request a framework. Avoid external runtime dependencies unless necessary. Embed small data/assets; keep large evidence images as sibling files.

For a project output, provide a clear entry point, token files, component specimens, and build commands. Reuse the user's existing stack when editing a repository.

Do not claim the report is production-ready solely because it renders. Validate responsive layout, keyboard navigation, console errors, reduced motion, and data completeness.

## 9. Acceptance checklist

- The page visually feels derived from the extracted system.
- All major token families have usable specimens.
- Components expose variants, states, and content stress cases.
- Motion can be controlled and reduced.
- Mobile and desktop layouts are functional.
- Evidence and uncertainty are legible.
- Recommendations cannot be confused with observations.
- Token/code exports are copyable or downloadable.
- Source logos, copy, photos, and personal data are omitted unless authorized.
- No important section contains unlabeled invented values.
