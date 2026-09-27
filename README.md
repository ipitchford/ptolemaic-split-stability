# Sharp local stability and critical-exponent sensitivity of Ptolemaic split metrics

Anonymous · 0.3.1-candidate · 27 September 2026 · **Unrefereed candidate**

[Version DOI](https://doi.org/10.5281/zenodo.23000081) · [Manuscript](paper/rigidity.pdf) · [AI index](AI_INDEX.md) · [Claims](CLAIMS.json)

This companion release determines attained local stability constants at specified Ptolemaic split metrics, with universal certificates and nonlinear realisation. It does not re-claim the predecessor's global threshold theorem.

## Read and check
- [Paper](paper/rigidity.pdf), [TeX](paper/rigidity.tex), [editable Markdown](RESEARCH_NOTE.md).
- [Complete certificate tables](CERTIFICATE_TABLES.md), [small certificates](certificates/small_duals.json), [universal certificates](certificates/symbolic_duals.json). These are indispensable proof supplements.
- [Review response](review/REVISION_RESPONSE_V031.md), [assurance](ASSURANCE.md), [sources](SOURCES.md), [replay receipt](REPLAY_RECEIPT.md).

Install Python 3.13 and the pinned requirements, then run:

```sh
python -m pip install -r requirements.txt
python -B replay.py --mode full --output ../ptolemaic-replay
python -OO -B replay.py --mode exact --output ../ptolemaic-optimized
python -B code/test_verifier_modes.py --output ../ptolemaic-controls
```

Outputs must be outside the package. Exact reports must match the shipped bytes; numerical outputs may vary across platforms and are corroboration only. All currently supported proof-critical checks use explicit exceptions, not assertions. The historical v0.2 archive is retained unchanged and is not retroactively hardened.

## Limits
- Unrefereed candidate; no formal proof-assistant verification, authenticated external specialist endorsement or journal peer review.
- Producer-coordinated replay and separately implemented reviewer code do not establish unaffiliated reproduction.
- Local split theorems do not require the companion universal threshold theorem; complete global equality interpretation does.
- The five-point classification, general four-point quadratic stability, explicit global separated-class constant and sharp dimension-uniform second-order remainder remain open here.
- Bounded prior-art checking does not establish exhaustive novelty or priority.

Original prose/data CC0-1.0; original code MIT. Retained historical archives and reviewer audit retain their upstream terms or NOASSERTION: see [LICENSES.md](LICENSES.md).
