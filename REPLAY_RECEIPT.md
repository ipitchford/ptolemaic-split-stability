# Local replay receipt — 0.3.1-candidate

27 September 2026. Current exact, symbolic and numerical verifiers pass locally. Exact reports retain their original hashes. Numerical reports are corroborative, not a universal proof or a cross-platform byte-identity promise.

- Standard-library exact checks: 36 small certificates, 72 selected general-formula evaluations, 155,436 rows, 40 sharp directions, 125,064 ordered triangle and 182,856 oriented Ptolemy inequalities.
- Universal symbolic checks: all 18 rational-function dual families and shifted coefficient nonnegativity over their full parameter ranges.
- Numerical experiment: 182 trials over 13 split pairs, 78 critical-root calculations, plus 70-digit selected checks. Directions mix the lower extremiser and inward upper direction; not general cone sampling.
- Supplied separate checker, rerun locally: 54 certificates, 150,810 reconstructed constraint rows, 72 finite LP face checks; no imports from the author's geometry implementation.
- Optimisation controls: normal, -O, -OO, PYTHONOPTIMIZE=1 and =2. Twenty valid and fifty corrupted-input controls passed. Mutation manifests are rehashed, so rejection tests mathematics, not a stale checksum.
- The original reviewer fault injection now rejects in normal and optimised modes.

Current receipts are results/REVIEWER_REPLAY.json, results/REVIEWER_FAULT_FIXED.json and results/MODE_CONTROL_REPORT.json. Absolute working paths are redacted in shipped copies; retained private logs preserve raw receipts. Historical supplied results under provenance/reviewer-audit record the original defect and are intentionally unchanged.

Reproduce with python -B replay.py --mode full --output ../replay, and python -B code/test_verifier_modes.py --output ../mode-controls. The final archive also receives a clean-extraction normal/optimised preflight retained in its public release assets. These are producer-side checks, not external peer review, independent reproduction or formal verification of all analytic arguments. Nested historical archives were not modified or rerun in this revision; their original replay receipts remain provenance.
