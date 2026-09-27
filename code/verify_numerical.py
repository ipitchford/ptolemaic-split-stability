#!/usr/bin/env python3
"""Seeded corroboration; no numerical calculation is a proof premise."""
import argparse, json, math
from pathlib import Path
import numpy as np
import mpmath as mp
from scipy.optimize import brentq
from verify_exact import primal, SMALL

def helmert(m):
    Q = np.zeros((m, m - 1))
    for j in range(1, m):
        Q[:j, j - 1] = 1 / math.sqrt(j * (j + 1))
        Q[j, j - 1] = -j / math.sqrt(j * (j + 1))
    return Q

def array(a, r, e, t):
    m = a + r
    d = np.zeros((m, m))
    j = 0
    for i in range(m):
        for k in range(i + 1, m):
            val = (2 if i >= a else 1) + t * float(e[j]) - 4 * t * t * int(k < a or i >= a)
            d[i, k] = d[k, i] = val
            j += 1
    return d

def gap(d, p, Q):
    return float(np.linalg.eigvalsh(-Q.T @ np.power(d, p) @ Q)[0])

def main(out):
    rng = np.random.default_rng(270926)
    records = []
    max_excess = 0.0
    high = []
    cases = [(2, 3), (2, 4), (3, 3), (3, 4), (3, 5), (4, 4), (4, 5), (4, 6), (5, 5), (5, 6), (6, 6), (7, 8), (9, 11)]
    for a, r in cases:
        m = a + r
        T = r * (a + 1) / (a * (r - 1))
        p = math.log2(T)
        Q = helmert(m)
        c = float(SMALL.get((a, r), min(a * r / 2, a * (a + 1) / 2)))
        A = 2 * p * c / (m * a * (r - 1))
        U = p * r * (3 * a - 1) / (2 * m)
        b0 = p * (m - 1) + 18 * p * p * (m - 1) ** 2
        B = b0 + 3 * p * r * (a - 1) / m
        mode = 'small' if (a, r) in SMALL else 'upper' if a == r else 'single'
        E, v, _ = primal(a, r, mode)
        _, w, _ = primal(a, r, 'inward')
        for label, e in [('lower', v), ('upper', w)]:
            for t in [0.001, 0.0001, 1e-05]:
                d = array(a, r, e, t)
                base = array(a, r, [0] * len(E), 0)
                h = float(np.max(np.abs(d - base)))
                delta = gap(d, p, Q)
                lo = A * h - B * h * h
                hi = U * h + p * (m - 1) * h * h
                ex = max(lo - delta, delta - hi, 0)
                max_excess = max(max_excess, ex)
                if not ex < 1e-10:
                    raise ValueError('Verification failed: ex < 1e-10')
                rho = min(0.125, 1 / (12 * p * (m - 1)))
                if not h < rho:
                    raise ValueError('Verification failed: h < rho')
                crit = brentq(lambda x: gap(d, x, Q), p - 1e-07, p + 0.2, xtol=1e-13)
                lam = r * (a + 1) * math.log(2) / m
                records.append(dict(a=a, r=r, family=label, t=t, h=h, gap=delta, gap_over_h=delta / h, sharp_lower=A, sharp_upper=U, lower_bound=lo, upper_bound=hi, critical_exponent=crit, exponent_displacement=crit - p, first_prediction=delta / lam))
        for _ in range(8):
            z = float(rng.random())
            e = [z * float(x) + (1 - z) * float(y) for x, y in zip(v, w)]
            t = 10 ** float(rng.uniform(-5, -3))
            d = array(a, r, e, t)
            h = float(np.max(np.abs(d - array(a, r, [0] * len(E), 0))))
            delta = gap(d, p, Q)
            ex = max(A * h - B * h * h - delta, delta - U * h - p * (m - 1) * h * h, 0)
            if not ex < 1e-10:
                raise ValueError('Verification failed: ex < 1e-10')
            max_excess = max(max_excess, ex)
            records.append(dict(a=a, r=r, family='convex_mix', t=t, h=h, gap=delta, excess=ex))
    mp.mp.dps = 70
    for a, r in [(3, 4), (4, 5), (5, 5), (4, 6)]:
        m = a + r
        p = mp.log(mp.mpf(r) * (a + 1) / (a * (r - 1)), 2)
        mode = 'small' if (a, r) in SMALL else 'upper' if a == r else 'single'
        E, e, _ = primal(a, r, mode)
        t = mp.mpf('0.00001')
        D = mp.matrix(m)
        H = mp.matrix(m, m - 1)
        for j in range(1, m):
            den = mp.sqrt(j * (j + 1))
            for i in range(j):
                H[i, j - 1] = 1 / den
            H[j, j - 1] = -j / den
        for idx, (i, j) in enumerate(E):
            ev = mp.mpf(e[idx].numerator) / e[idx].denominator
            D[i, j] = D[j, i] = (2 if i >= a else 1) + t * ev - 4 * t * t * int(j < a or i >= a)

        def fg(x):
            return mp.eigsy(-H.T * D.apply(lambda z: z ** x) * H, eigvals_only=True)[0]
        delta = fg(p)
        crit = mp.findroot(fg, (p, p + mp.mpf('.01')))
        high.append(dict(a=a, r=r, gap=mp.nstr(delta, 60), critical_displacement=mp.nstr(crit - p, 60), predicted_first_order=mp.nstr(delta / (mp.mpf(r) * (a + 1) * mp.log(2) / m), 60)))
    p = mp.log(3, 2)
    coeff = p * (2 * p - 3) / 8
    four = []
    H = mp.matrix(4, 3)
    for j in range(1, 4):
        for i in range(j):
            H[i, j - 1] = 1 / mp.sqrt(j * (j + 1))
        H[j, j - 1] = -j / mp.sqrt(j * (j + 1))
    for ts in ['0.01', '0.001', '0.0001', '0.00001']:
        t = mp.mpf(ts)
        L = [1 + t, 1 - t, mp.mpf(1)]
        D = mp.matrix(4)
        for i in range(1, 4):
            D[0, i] = D[i, 0] = L[i - 1]
        for i in range(1, 4):
            for j in range(i + 1, 4):
                D[i, j] = D[j, i] = L[i - 1] + L[j - 1]
        v = mp.eigsy(-H.T * D.apply(lambda z: z ** p) * H, eigvals_only=True)[0]
        four.append({'t': ts, 'gap_over_t_squared': mp.nstr(v / t ** 2, 60), 'limit': mp.nstr(coeff, 60)})
    out.mkdir(parents=True, exist_ok=True)
    (out / 'numerical_trials.json').write_text(json.dumps(records, indent=2, sort_keys=True) + '\n')
    (out / 'numerical_results.json').write_text(json.dumps({'status': 'PASS', 'trials': len(records), 'max_bound_excess': max_excess, 'tolerance': 1e-10, 'precision_digits': 70, 'high_precision': high, 'four_point_quadratic': four, 'proof_role': 'corroboration only'}, indent=2, sort_keys=True) + '\n')
    print('PASS:', len(records), 'corroborative trials;', len(high) + len(four), 'high-precision examples')
if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    main(ap.parse_args().output)
