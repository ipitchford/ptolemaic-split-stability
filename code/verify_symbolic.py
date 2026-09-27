#!/usr/bin/env python3
"""Universal certificate verification by exact symbolic orbit counting.
Not a proof assistant: analytic spectral and geometric arguments are in the note.
"""
import argparse, json
from pathlib import Path
import sympy as s
from orbit_geometry import orbit_matrix
from certificate_contract import load_certificates
ROOT = Path(__file__).resolve().parents[1]

def nonnegative_fraction(expr, k, k0):
    x = s.symbols('x', nonnegative=True)
    num, den = s.fraction(s.factor(expr.subs(k, k0 + x)))
    pn, pd = (s.Poly(num, x), s.Poly(den, x))
    if not all((c >= 0 for c in pn.all_coeffs())):
        raise ValueError((expr, num))
    if not (all((c >= 0 for c in pd.all_coeffs())) and pd.eval(0) > 0):
        raise ValueError((expr, den))
    return {'numerator': str(pn.as_expr()), 'denominator': str(pd.as_expr())}

def main(out):
    k = s.symbols('k', integer=True, positive=True)
    checks = []
    for rec in load_certificates('symbolic'):
        r = k + rec['offset']
        M, ro, eo, ind, mult = orbit_matrix(k, r, rec['kind'])
        if not [list(o) for o in ro] == rec['orbits']:
            raise ValueError("Verification failed: [list(o) for o in ro] == rec['orbits']")
        vals = s.Matrix([s.sympify(z, locals={'k': k}) for z in rec['values']])
        c = s.sympify(rec['c'], locals={'k': k})
        expected_c = k*k/2 if rec['offset'] == 0 else k*(k+1)/2
        if s.cancel(c - expected_c) != 0:
            raise ValueError('Certificate does not bind the claimed universal constant')
        rhs = M[:, :-1] * s.ones(len(ro), 1) - rec['sign'] * c * ind
        if not all((s.cancel(x) == 0 for x in M * vals - rhs)):
            raise ValueError('Verification failed: all((s.cancel(x) == 0 for x in M * vals - rhs))')
        cert = []
        for j, o in enumerate(ro):
            z = nonnegative_fraction(vals[j], k, rec['k_min'])
            if o[0] == 'v':
                z['upper_two'] = nonnegative_fraction(2 - vals[j], k, rec['k_min'])
            cert.append(z)
        checks.append({'offset': rec['offset'], 'kind': rec['kind'], 'sign': rec['sign'], 'nonnegativity_certificates': cert})
    a, r, p = s.symbols('a r p', positive=True)
    m = a + r
    T = r * (a + 1) / (a * (r - 1))
    derivative_y = -2 * p * r / (a * m)
    derivative_t = -p * a * T / (r * m)
    gamma = 2 * p / (m * a * (r - 1))
    if not s.simplify(derivative_y + gamma * r * (r - 1)) == 0:
        raise ValueError('Verification failed: s.simplify(derivative_y + gamma * r * (r - 1)) == 0')
    if not s.simplify(derivative_t + gamma * a * (a + 1) / 2) == 0:
        raise ValueError('Verification failed: s.simplify(derivative_t + gamma * a * (a + 1) / 2) == 0')
    ellmax = a * r * (r - 1) * (3 * a - 1) / 4
    if not s.simplify(gamma * ellmax - p * r * (3 * a - 1) / (2 * m)) == 0:
        raise ValueError('Verification failed: s.simplify(gamma * ellmax - p * r * (3 * a - 1) / (2 * m)) == 0')
    if not s.simplify(a * (r - 1) * T / m - r * (a + 1) / m) == 0:
        raise ValueError('Verification failed: s.simplify(a * (r - 1) * T / m - r * (a + 1) / m) == 0')
    u, Y = s.symbols('u Y')
    v = -2 * u / (r - 2)
    g = u + v
    ell = N = a * (a + 1) / 2
    expr = -r * (r - 1) * a * (a - 1) / 2 * Y - N * (-1 + 2 * (r - 2) * (2 * g - 2 * Y) + (r - 2) * (r - 3) / 2 * (2 * v))
    upper = s.factor(expr.subs({u: -(r - 2) / (4 * (r - 1)), Y: 1 / (2 * (r - 1))}))
    if not s.simplify(upper - a * r / 2) == 0:
        raise ValueError('Verification failed: s.simplify(upper - a * r / 2) == 0')
    expr2 = -r * (r - 1) * a * (a - 1) / 2 * Y - N * (-1 + 2 * (r - 2) * g + (r - 2) * (r - 3) / 2 * (2 * v))
    lower = s.factor(expr2.subs({u: -(r - 2) / (3 * r - 4), Y: -(r - 4) / (2 * (3 * r - 4))}))
    expected = a * r * ((a - 1) * (r - 2) * (r - 3) + 4) / (4 * (3 * r - 4))
    if not s.simplify(lower - expected) == 0:
        raise ValueError('Verification failed: s.simplify(lower - expected) == 0')
    rr = s.symbols('r', positive=True)
    uu = -(rr - 2) / (4 * (rr - 1))
    vv = yy = 1 / (2 * (rr - 1))
    tt1 = -(rr - 2) / (2 * (rr - 1))
    tt2 = 1 / (rr - 1)
    primal_slacks = [2 * vv - tt2, uu + vv - tt1, 2 * uu + 1, 4 * vv - 2 * yy - tt2, 2 * (uu + vv) - 2 * yy - tt1, 4 * uu - 2 * yy + 1]
    for value in primal_slacks:
        nonnegative_fraction(s.factor(value), rr, 5)
    for value in [uu, vv, yy, tt1, tt2]:
        nonnegative_fraction(s.factor(1 - value), rr, 5)
        nonnegative_fraction(s.factor(1 + value), rr, 5)
    z = s.Matrix([3, -1, -1, -1])
    Pi = s.eye(4) - s.ones(4) / 4
    D0 = s.Matrix([[0, 1, 1, 1], [1, 0, 2, 2], [1, 2, 0, 2], [1, 2, 2, 0]])
    e = s.Matrix([[0, 1, -1, 0], [1, 0, 0, 1], [-1, 0, 0, -1], [0, 1, -1, 0]])
    L = s.zeros(4)
    Q = s.zeros(4)
    for i in range(4):
        for j in range(4):
            if i != j:
                fac = 1 if D0[i, j] == 1 else s.Rational(3, 2)
                fac2 = 1 if D0[i, j] == 1 else s.Rational(3, 4)
                L[i, j] = -p * fac * e[i, j]
                Q[i, j] = -p * (p - 1) * fac2 * e[i, j] ** 2 / 2
    b = Pi * L * z
    if not ((z.T * L * z)[0] == 0 and (s.ones(1, 4) * b)[0] == 0):
        raise ValueError('Verification failed: (z.T * L * z)[0] == 0 and (s.ones(1, 4) * b)[0] == 0')
    coefficient = s.simplify((z.T * Q * z)[0] / 12 - (b.T * b)[0] / 36)
    if not s.simplify(coefficient - p * (2 * p - 3) / 8) == 0:
        raise ValueError('Verification failed: s.simplify(coefficient - p * (2 * p - 3) / 8) == 0')
    summary = {'status': 'PASS', 'symbolic_certificate_families': len(checks), 'all_size_derivative': 'verified', 'sharp_primal_formulas': 'verified, including universal balanced feasibility', 'four_point_quadratic_coefficient': str(coefficient), 'universal_certificate_details': checks, 'formal_proof_assistant': False}
    out.mkdir(parents=True, exist_ok=True)
    (out / 'symbolic_results.json').write_text(json.dumps(summary, indent=2, sort_keys=True) + '\n')
    print('PASS: 18 universal rational families and spectral identities')
if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    main(ap.parse_args().output)
