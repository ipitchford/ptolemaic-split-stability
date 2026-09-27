# AI index — Ptolemaic split stability

## Identity and status
Sharp local stability and critical-exponent sensitivity of Ptolemaic split metrics. Anonymous, 0.3.1-candidate. Version DOI: https://doi.org/10.5281/zenodo.23000081. Unrefereed candidate, not an externally verified theorem.

## Entry points
- [Claims](CLAIMS.json): content-derived claim identifiers, exact scope, normalisation and dependencies.
- [Paper PDF](paper/rigidity.pdf), [TeX](paper/rigidity.tex), [Markdown](RESEARCH_NOTE.md).
- [Complete certificate tables](CERTIFICATE_TABLES.md), [small duals](certificates/small_duals.json), [symbolic duals](certificates/symbolic_duals.json).
- [Assurance](ASSURANCE.md), [status](STATUS.md), [review response](review/REVISION_RESPONSE_V031.md).
- [Sources](SOURCES.md), [citation audit](CITATION_AUDIT.md), [replay receipt](REPLAY_RECEIPT.md), [environment](ENVIRONMENT.txt).
- [Provenance](PROVENANCE.md), [licences](LICENSES.md), [manifest](SHA256SUMS).

## Claim map
- **LOCAL**, Theorem 2.1; all pairs and constants in Section 2: At every specified split CS(a,r), in mean-cross-distance-one normalisation with h=||d-s||_infinity <= min(1/8,1/(12p(m-1))), A*h-b*h^2 <= Delta_p(d) <= U*h+p(m-1)*h^2. A and U are the exact attained lower and upper first-order rates. Evidence: Direct geometry, exact certificates, written spectral argument.
- **CONE**, Lemma 3.1 and Theorem 4.1: The normalised Ptolemaic tangent cone is exactly D e >= 0, w^T e=0: every direction of infinity norm at most one is realised by s+t e+4t^2 e_in for 0<t<=1/20. Evidence: Written nonlinear realisation and universal/small dual certificates.
- **EXPONENT**, Theorem 6.1: For each fixed covered split, wp(d)-p=m*Delta_p(d)/(r(a+1)log(2))+O(h^2), with the attained lower and upper directional rates stated in Theorem 6.1. Evidence: Written implicit-function argument plus imported strict descent.
- **FOUR**, Proposition 7.2: At the four-point equal-arm star, arm lengths 1+t,1-t,1 give Delta_p(d_t)=p(2p-3)t^2/8+O(t^4), p=log_2(3). Hence a positive linear lower bound fails there. Evidence: Written expansion plus symbolic check; not a general quadratic lower theorem.
- **SMALL**, Proposition 7.1: The equality metrics at the three-point endpoint are distinct collinear triples; at the four-point endpoint they are similarities of CS(1,3) and CS(2,2). Evidence: Written equality specialisation of cited threshold, strict descent and Ercan transport.
- **COLLISION**, Proposition 8.1: For a diameter-one Ptolemaic pseudometric on m>=6 points with N<m zero-distance classes, the restricted kernel at p_m is the class-sum-zero space of dimension m-N, under the stated threshold premises. Evidence: Conditional quotient argument; companion threshold premises retained.
- **DESCENT**, Proposition 8.2: For N>=2, q-negative type, minimum distance eta>0 and 0<p<q, Delta_p(d)>=eta^p/[2 Gamma(1-p/q) log(2(N-1))^(p/q)]. Evidence: Written Gaussian-kernel integral and diagonal-dominance bound.

## Replay
Install [requirements.txt](requirements.txt). Run `python -B replay.py --mode full --output ../replay`; normal and optimised Python are supported. [Mode controls](code/test_verifier_modes.py) test valid and corrupted inputs directly and through replay with freshly updated disposable manifests. Exact symbolic and rational reports must match; floating-point numerical reports are corroborative and platform-sensitive.

## Safe reuse and trust boundary
Use Sections 3--5 without importing the global companion theorem. To assert completeness of the equality family, include retained v0.2 and its threshold premises. Do not substitute the L2-normalised restricted eigenvalue gap for the differently normalised Li--Weston or rooted-Gramian gap. Do not promote sampled k values or numerical LP faces into the universal proof.

Five-point global equality, a general four-point quadratic lower theorem, explicit global separated-class constants and uniform sharp second-order estimates remain open. The proposed transferable framework with a second extremal family is a future project. The statement fingerprint identifies text, not a proof of mathematical equivalence.
