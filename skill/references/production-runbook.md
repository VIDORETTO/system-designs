# Production runbook

## Static quality

Run the deterministic contract, fixture, renderer and anti-pattern checks:

    python3 skill/scripts/test_design_system.py
    python3 skill/scripts/audit_design_system.py templates/media/experience-layer/design-system.json
    python3 skill/scripts/benchmark_coverage.py templates/saas/alethe-design-system/design-system.json templates/media/experience-layer/design-system.json

## Browser quality

Install the pinned Playwright dependency and Chromium:

    npm install
    npx playwright install chromium

Capture desktop/mobile and normal/reduced-motion states:

    npm run capture:browser
    npm run validate:browser
    npm run visual:regression

The browser runner accepts public URLs, local files, or an external private
config. Use authorized sessions only. It records request failures as evidence;
do not turn off those records to make a run green.

## Baseline promotion

1. Run capture against the approved route set.
2. Inspect all screenshots and the runtime probe manifest.
3. Promote only reviewed screenshots into tests/visual-baselines/.
4. Record why the baseline changed.
5. Keep missing-baseline failures enabled in the protected quality workflow;
   use `--allow-missing-baseline` only while bootstrapping a new reviewed
   target, then promote its captures and remove the temporary exception.

## Release gate

Do not release when:

- the validator reports errors or P0/P1 issues;
- normal/reduced-motion coverage is missing;
- a page has unexpected runtime errors;
- a visual baseline changes without review;
- media is protected, unauthorized, or essential content is only inside frames.
