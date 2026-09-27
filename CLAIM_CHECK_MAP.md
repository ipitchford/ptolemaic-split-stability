# Claim-to-check map

| Claim | Mathematical basis | Executable evidence | Limit |
|---|---|---|---|
| Sharp all-size tangent constant | Sections 3–4; explicit dual identities and primal directions | `symbolic_duals.json`, `small_duals.json`, both exact verifiers | SymPy verifies polynomial identities, not all analytic prose |
| Positivity in every dimension | Nonnegative numerator/denominator coefficients after shifting k | Complete expansions in `symbolic_results.json` | Not inferred from sampled dimensions |
| Exact tangent-cone realisability | Lemma 3.1 with inward t^2 correction | Fraction Ptolemy and triangle checks | Analytic estimates supply universal t/direction coverage |
| Explicit spectral bound | Section 5 Taylor estimates and scalar Schur equation | Symbolic first derivative, seeded spectra, high precision | Numerical perturbations are corroborative only |
| Critical exponent | Theorem 6.1, implicit function theorem and strict descent | 78 bracketing computations, four 70-digit root checks | O(h^2) is at fixed cardinality, not uniform in m |
| Three-/four-point classification | Section 7, external endpoint and attributed Ercan transport | Exact small split examples, symbolic direction | Priority not established; five points not classified |
| Four-point quadratic coefficient | Proposition 7.2, second-order eigenvalue expansion | Direct independent symbolic reconstruction and four 70-digit samples | Does not prove a global quadratic lower bound |
| Collision kernel | Quotient argument and smaller-size strictness | Mathematical argument | Depends on companion/source global thresholds |
| Explicit subcritical gap | Gaussian PSD integral and Gershgorin tail | Mathematical argument; no finite-data theorem surrogate | Does not give a full global C_eta |
| Existing v0.2 assertions | Received v0.2 paper and its dependencies | Full six-job replay with nested five-job companion exact run | Replay is not authenticated independent peer review |
