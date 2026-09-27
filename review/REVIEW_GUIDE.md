# Guide for independent review

The new supplement should be reviewed independently of the favourable assessments recorded in previous archives.

## Most important proof checks

1. Verify the row enumeration in Section 3 and the mean-cross normalisation. It is needed in both the linear functional and the sharp constants.
2. Check certificate (C) for one representative edge of each type and sign. The orbit formula counts all labelled rows. Review the positive coefficient expansions after k=k0+x, including the upper bound of two on Ptolemy weights.
3. Check every primal direction is in the cone, and the universal inward quadratic correction really preserves all inactive as well as active inequalities. This links LP sharpness to geometric sharpness.
4. Check the restricted eigenvalue convention, the Taylor remainder, the scalar Schur estimate, and the unit-vector bound. The general constants are conservative but explicit.
5. Check that the local exponent zero is the actual supremal negative-type exponent, not just a zero of one eigenvalue. The strict-descent step supplies that distinction.
6. For four-point equality, check the scalar equality condition and the transported nonzero potential. For the four-point deformation, verify the second-order eigenvector correction, not just the Rayleigh quotient.

## Scope tests

- No claim of a five-point equality classification is made.
- No explicit numerical global C_eta is claimed.
- No uniform-in-cardinality O(h^2) remainder is claimed.
- Sampling more dimensions is not the proof of the infinite families.
- The analytic supplement depends on exact certificate data but not on a numerical LP solver.

Run `python replay.py --mode full --output <an external directory>`. To review the input, extract `provenance/ptolemaic_rigidity_v0_2.zip`; its original files have not been changed.
