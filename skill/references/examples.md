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
