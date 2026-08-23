# Baseline and regression reference

The compatibility baseline for this branch is the existing Alethe SaaS
template plus the schema-v2 media fixture.

Run from the repository root:

    python3 skill/scripts/validate_design_system.py templates/saas/alethe-design-system/design-system.json
    python3 skill/scripts/render_design_system_report.py templates/saas/alethe-design-system/design-system.json /tmp/alethe-report.html
    python3 skill/scripts/test_design_system.py templates/media/experience-layer/design-system.json

The first command is the compatibility check for legacy manifests. The second
checks that the renderer can consume a v1 manifest. The third checks v2
experience/media/motion behavior and report markers.
