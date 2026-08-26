# Evidence index · Ruben Marcus portfolio

The manifest contains the full claim-to-source map. This index keeps the public
template portable and intentionally does not redistribute screenshots, video
frames, source imagery, logos, or private local paths.

## Sources

| ID | Source | Context | Limitation |
| --- | --- | --- | --- |
| `E-live-portfolio-desktop-001` | public portfolio URL | 1440×900, dark, pt-BR, top of route | browser screenshot capture became unstable after the first desktop capture; DOM/computed inspection remained available |
| `E-live-portfolio-mobile-002` | public portfolio URL | 390×844, compact header, single-column cards | mobile visual screenshot timed out; live DOM/computed layout was inspected |
| `E-live-portfolio-filter-003` | public portfolio URL + `#g=ai` | safe filter click, selected state, result status | one representative taxonomy filter sampled |
| `E-live-portfolio-hover-focus-004` | public portfolio URL | linked-card hover and filter-button keyboard focus | highlighted static card intentionally differs from linked-card hover |
| `E-live-portfolio-menu-005` | public portfolio URL | mobile menu open/close, dialog semantics | overlay links were not followed |
| `E-live-portfolio-scroll-006` | public portfolio URL | fixed header scrolled state | only the header state was required; smooth-scroll delta was limited |
| `E-live-portfolio-css-007` | runtime CSS/DOM inspection | root variables, font-face rules, media rules, keyframes | shared bundle may include route-adjacent rules; claims are selector-scoped |
| `E-recording-001` | user-supplied screen recording | 122.99s, 1862×908, 30fps, site-wide walkthrough | source recording and frames are not redistributed in this public package |
| `E-recording-storyboard-002` | sampled user-supplied recording | 1 fps sample of first 12s for pacing/context | no storyboard image is committed; refer to the supplied recording locally |
| `E-computed-contrast-008` | deterministic calculation | WCAG relative luminance from runtime colors over black | translucent borders/textures are not treated as body-text pairs |

## Asset policy

The live reference includes personal imagery, brand marks, third-party logos,
external widgets and source copy. The package describes their treatment as
design-system patterns and uses neutral specimens in `report.html` instead of
shipping those assets.

## Reproduction note

The original recording was available locally during extraction but is not part
of this repository. If an authorized copy is available, compare it at 30fps and
keep any derived frames outside the public package unless redistribution rights
are confirmed.
