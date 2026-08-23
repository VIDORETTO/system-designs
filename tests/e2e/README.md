# Browser E2E capture

The capture runner uses Playwright when an authorized browser environment is
available. It captures:

- desktop and mobile viewports;
- normal and reduced-motion states;
- screenshot, page metadata, console/page errors and failed requests;
- runtime media/effects/motion inventory from runtime_media_probe.js.

Run locally:

    npm install
    npx playwright install chromium
    npm run capture:browser
    npm run validate:browser
    npm run visual:regression

For a live site, create a private config outside the repository or pass a
config file with authorized URLs. Do not commit credentials, session state,
private URLs or protected screenshots.
