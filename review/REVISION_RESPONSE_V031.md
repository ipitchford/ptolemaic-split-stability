# Response to the two supplied v0.3 reviews

27 September 2026. This is a producer-side response, not external peer review. Both supplied reviews and the separately supplied audit informed the revision. The received audit identifies the exact original ZIP by SHA-256; its original files are preserved in provenance/reviewer-audit without rewriting their historical results.

| Review point | Action and evidence | Disposition |
| --- | --- | --- |
| Assertions disappear under Python optimisation | Replaced proof-critical assertions in all three current verifiers with explicit exceptions; replay propagates -O and -OO. Added certificate identity, coverage and parameter-range checks. | Fixed |
| Rehashed negative weight accepted under optimisation | Replayed the reviewer's original fault test: both modes reject. New controls cover negative weights and identity corruption in small and symbolic certificates, with updated disposable manifests. | Fixed |
| Broader optimisation modes and wrapper | code/test_verifier_modes.py exercises normal, -O, -OO, PYTHONOPTIMIZE=1 and =2; 20 valid controls and 50 semantic rejection controls pass. | Fixed |
| Sánchez and Li–Weston contextual comparison | Section 6 cites the finite-metric matrix criterion and existing quantitative exponent extension. It distinguishes the exact split-specific directional constants and the L2 gap from simplex/rooted-Gramian normalisations. | Added |
| Durable complete certificates | All 18 symbolic families, 36 small duals, expanded tables, corrected code and pinned dependencies are included. Section 4.1 and reference SUPP name version DOI 10.5281/zenodo.23000081. | Included |
| Geometric meaning of exceptions | Section 4 explains small-cardinality compensating directions, the (3,5) exception and the stable balanced/unbalanced constructions; no uniqueness claim for minimisers. | Added |
| Normalisation next to parity formula | Mean cross-distance one and infinity-norm perturbation are stated next to the formula. | Added |
| Numerical cone coverage | Section 9 explicitly restricts the experiment to mixtures of the lower extremiser and inward upper direction, not arbitrary cone sampling. | Clarified |
| Local/global dependencies | Local cone and spectral arguments are separated from the companion equality classification, small-cardinality sources and collision-limit premises. | Clarified |
| Extra nonsymmetric numerical sampling | Optional and not needed for the universal algebraic argument. No claim to have sampled the full cone has been retained. | Not added; scope explicit |
| Abstract transferable framework and a second family | Worth a separate research project. The present release contains the corrected concrete theorem, not an unproved generalisation. | Future work |

The separate audit reconstructs constraints without importing the author's geometry code: all 54 certificates, 150,810 reconstructed constraint rows and 72 finite LP face checks passed locally. Its implementation diversity is useful evidence, but running supplied review code inside the producer workflow is not unaffiliated reproduction. The analytic proofs remain written arguments, not proof-assistant-checked theorems.
