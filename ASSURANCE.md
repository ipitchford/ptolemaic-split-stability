# Assurance boundaries

| Dimension | Scope |
| --- | --- |
| Exact statements | CLAIMS.json and numbered manuscript statements, with normalisation |
| Analytic proof | Producer-side reading of tangent-cone realisation, Schur estimate, critical-root argument and small/collision cases; not formal verification |
| Universal certificates | 18 rational-function families; symbolic identities and coefficient positivity over their stated domains |
| Finite exact checks | 36 small certificates, 72 sampled generic evaluations, primal directions and metric inequalities |
| Numerical checks | Selected extremisers and their convex mixtures; not the entire cone |
| Reviewer implementation | Raw-constraint reconstruction with no author-code imports; 54 exact certificate evaluations and 72 numerical LP faces; model-audit provenance |
| Independent reproduction | No authenticated unaffiliated rerun |
| Human specialist/editorial review | Not established |
| Formal verification | Not established |
| Novelty/priority | Bounded primary-source comparison only |

## Dependencies
Sections 3--5 are local and do not require the companion all-size threshold. Section 6 imports strict descent and endpoint facts. Section 7 imports public small endpoints and Ercan's transport. Section 8's quotient interpretation imports threshold premises; full global equality interpretation also uses retained v0.2 classification. Prior archives are preserved, not certified afresh merely by being bundled.

The current verifiers are hardened under optimisation. Historical nested code retains its original scope and limitations. Numerical replay is not promised byte-identical across platforms; exact and symbolic reports are. Full execution details and source hashes are in REPLAY_RECEIPT.md.
