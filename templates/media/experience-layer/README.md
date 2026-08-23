# Experience Layer · media and motion fixture

This neutral fixture shows the expanded extraction contract for a site whose
identity depends on a cinematic hero, background video, effects and motion.

## Files

- design-system.json — schema v2 manifest with experience, elements, media,
  effects, motion fallbacks and provenance.
- report.html — self-contained specimen using a local poster/still.
- evidence/ — neutral SVG aids and an evidence map. The source video is not
  embedded.

## Validate and render

Run:

    python3 skill/scripts/validate_design_system.py templates/media/experience-layer/design-system.json

    python3 skill/scripts/render_design_system_report.py templates/media/experience-layer/design-system.json templates/media/experience-layer/report.html

The report renderer only previews local/data-image assets by default. Remote
media URLs remain metadata until an authorized local evidence copy is supplied.
