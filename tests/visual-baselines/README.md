# Visual baselines

Browser capture writes one screenshot per target, viewport and reduced-motion
state. Authorized teams can promote a reviewed capture into this directory
using the exact filename from the capture manifest.

The CI job allows missing baselines and reports baseline-pending so a first
run produces reviewable artifacts without silently claiming pixel parity. Once
the baseline set is reviewed, remove the allow-missing-baseline flag from the
workflow or change it to a protected release workflow.

Baseline policy:

- review desktop and mobile together;
- include normal and reduced-motion states;
- never commit screenshots containing credentials or protected content;
- update a baseline only with a reason and a visual review note.
