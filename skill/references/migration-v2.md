# Schema v2 migration guide

Schema v2 is additive. Existing manifests continue to validate and render.

## Minimum migration

1. Add meta.schema_version: 2.
2. Keep every v1 top-level key.
3. Add experience when the site has a distinctive identity or focal moment.
4. Add media.assets for image/video/audio/canvas candidates.
5. Add effects for visual effects and interaction drivers.
6. Add reduced-motion/fallback/performance notes before calling media or motion
   production-ready.
7. Preserve source IDs and evidence limitations.

## Compatibility table

| Legacy area | v2 extension | Compatibility |
| --- | --- | --- |
| foundations.imagery | media.assets[] | Keep both when imagery tokens and concrete assets are different claims. |
| motion.patterns[] | driver, job, performance, reduced_motion | Existing patterns remain valid; enrich progressively. |
| patterns[] | experience.focal_moment, named_rules | Do not move page patterns; add the experience interpretation. |
| generated_assets | media.sidecar.json | Keep generated outputs separate from source media claims. |

Run the validator and regression runner before publishing:

    python3 skill/scripts/validate_design_system.py DESIGN_SYSTEM.json
    python3 skill/scripts/validate_design_system.py DESIGN_SYSTEM.json
