# Evidence index

This folder documents the evidence used by design-system.json.

## Captures

- E-live-home-desktop-001 — initial live page at 1363x936, DPR 1.
- E-live-fullpage-desktop-002 — full-page visual capture, approximately 5034px tall.
- E-dom-css-desktop-003 — same-origin stylesheet, DOM/accessibility snapshot, computed styles, font declarations, media rules, keyframes, CSS variables, and layout measurements.
- E-live-theme-004 — all 11 theme controls activated and checked through data-theme, --accent, and --accent-dim.
- E-live-usecase-005 — Caçar bug use-case selected; aria-pressed, prompt text, and agent-card content changed.
- E-live-hover-006 — first feature cell hovered; the cell darkened and the mock translated upward by 8px.
- E-live-keyboard-007 — Tab moved focus to the next use-case chip; focus ring measured as 2px accent outline with 2px offset.
- E-skill-contract-008 — requested extraction skill read from GitHub and applied as the evidence/quality contract.

The source page's brand artwork, wordmark image, product screenshot, avatar, and third-party tool logos are intentionally not copied into the living report. The report uses neutral CSS/SVG specimens to demonstrate the extracted rules.

## Coverage note

The cloud browser exposed a desktop viewport but did not expose direct viewport resizing. Responsive behavior is therefore represented by deployed media/container rules and clearly marked as source-observed or inferred in the manifest. The report itself contains a responsive viewport specimen and is designed to be tested at narrow widths in a local browser.
