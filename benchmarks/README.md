# Representative benchmark corpus

The corpus is intentionally small and safe to run in CI. It covers a legacy
SaaS extraction and a media/experience extraction with normal and reduced-motion
rules.

Run coverage:

    python3 skill/scripts/benchmark_coverage.py templates/saas/alethe-design-system/design-system.json templates/media/experience-layer/design-system.json

Add external sites only with authorization and keep their live capture config
outside the repository. A benchmark result is not permission to redistribute
their content or media.
