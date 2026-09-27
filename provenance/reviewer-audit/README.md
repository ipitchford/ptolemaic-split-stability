# Reviewer audit: Ptolemaic rigidity v0.3

Review date: 27 September 2026.

## Evidence
- `v03_replay_receipt.json`: supplied full replay passed, 46 manifest entries; all four regenerated reports byte-identical.
- `v02_with_baseline_replay_receipt.json`: nested v0.2 full replay and companion exact replay passed. The equality-search summary differs only in three elapsed-time values; trial records match.
- `independent_math_results.json`: separately implemented raw-constraint geometry; 36 small exact dual checks, 18 universal dual checks evaluated at k=13, and 72 floating-point LP face problems over 12 pairs. The sampled exact evaluations and numerical LPs do not prove all-cardinality validity.
- `assert_safety_results.json`: a deliberately invalid certificate is rejected under ordinary Python but accepted when PYTHONOPTIMIZE=1. The mutation was made only in a disposable copy. Its file checksum was updated to test mathematical validation rather than file-integrity checking. This does not indicate that any shipped mathematical certificate is false.

## Reproduction
Python with NumPy, SciPy and SymPy is required. See `audit_metadata.json` for the environment used.

Run the independent tests after extracting the original user-supplied archive:

```sh
python independent_math_checks.py --bundle /path/to/ptolemaic_rigidity_v0_3 --output /path/to/reviewer-math-results
python test_assert_safety.py --bundle /path/to/ptolemaic_rigidity_v0_3 --output /path/to/new-fault-test-directory
```

The second command requires a fresh output directory and creates its disposable copy there. It does not edit the original bundle. The scripts here are parameterised copies of the scripts used in the review; only path handling was changed, and the copies were syntax checked. No theorem or manuscript was patched by this audit.

## Limits
This is a computational audit plus supporting receipts, not a formal proof-assistant verification, authenticated independent specialist endorsement, or an exhaustive literature search. The analytic and universal rational-function proofs require mathematical scrutiny independently of sampled tests.
