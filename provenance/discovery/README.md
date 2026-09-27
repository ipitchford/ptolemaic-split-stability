# Exploratory history — not required to verify the theorems

These files record numerical linear-programming exploration, symmetry reduction and rational-function discovery. They retain their original working-directory references. They are historical records, not portable production scripts and not proof premises. In particular, the interpolated discovery matrices in `dual_symbolic.py` are superseded by the direct combinatorial orbit construction in `code/orbit_geometry.py`. No pickle file is included or loaded by the release verifiers.

The proof evidence consists of the explicit JSON certificates and the independent exact/symbolic reconstructions in `code/`. Every universal identity is verified as a rational function; nonnegativity is established by positive coefficient expansions after shifting the integer parameter. No solver or finite-dimensional fit is used in those verifications.
