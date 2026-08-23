# Visual baselines

Browser capture writes one screenshot per target, viewport and reduced-motion
state. This directory contains the reviewed baseline for the neutral
`experience-layer` fixture, promoted from CI run `32615582636` after checking
desktop/mobile normal and reduced-motion states.

CI fails when a checked-in capture is missing or changes beyond the configured
pixel threshold. New targets should be introduced through a review branch;
the temporary `--allow-missing-baseline` option is reserved for that bootstrap
step and is not part of the protected quality workflow.

Baseline policy:

- review desktop and mobile together;
- include normal and reduced-motion states;
- never commit screenshots containing credentials or protected content;
- update a baseline only with a reason and a visual review note.
