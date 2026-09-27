#!/usr/bin/env python3
"""Independent standard-library reconstruction of every constraint row and certificate."""
from fractions import Fraction as F
from itertools import combinations, permutations
from pathlib import Path
import ast, argparse, json
from certificate_contract import load_certificates
ROOT = Path(__file__).resolve().parents[1]

def calc(text, k=0):

    def ev(n):
        if isinstance(n, ast.Constant):
            return F(n.value)
        if isinstance(n, ast.Name) and n.id == 'k':
            return F(k)
        if isinstance(n, ast.UnaryOp):
            return -ev(n.operand) if isinstance(n.op, ast.USub) else ev(n.operand)
        if isinstance(n, ast.BinOp):
            x, y = (ev(n.left), ev(n.right))
            if isinstance(n.op, ast.Add):
                return x + y
            if isinstance(n.op, ast.Sub):
                return x - y
            if isinstance(n.op, ast.Mult):
                return x * y
            if isinstance(n.op, ast.Div):
                return x / y
            if isinstance(n.op, ast.Pow):
                if not y.denominator == 1:
                    raise ValueError('Verification failed: y.denominator == 1')
                return x ** int(y)
        raise ValueError('Unsupported expression')
    return ev(ast.parse(text, mode='eval').body)

def geometry(a, r):
    E = list(combinations(range(a + r), 2))
    ix = {e: j for j, e in enumerate(E)}
    rows = []
    for b, c in combinations(range(a, a + r), 2):
        for i in range(a):
            rows.append((('u', i, b, c), {ix[i, b]: 1, ix[i, c]: 1, ix[b, c]: -1}))
        for i, j in combinations(range(a), 2):
            rows.append((('v', i, j, b, c), {ix[i, b]: 1, ix[i, c]: 1, ix[j, b]: 1, ix[j, c]: 1, ix[i, j]: -2, ix[b, c]: -1}))
    return (E, ix, rows)

def check_cert(a, r, kind, sg, c, orbits, vals):
    E, ix, rows = geometry(a, r)
    SA = {0, 1} if kind == 'A' else {0} if kind == 'X' else set()
    SB = {a, a + 1} if kind == 'B' else {a} if kind == 'X' else set()
    target = (0, 1) if kind == 'A' else (0, a) if kind == 'X' else (a, a + 1)
    weights = {tuple(o): z for o, z in zip(orbits, vals[:-1])}
    total = [F(0) for _ in E]
    ell = [F(0) for _ in E]
    for name, row in rows:
        Aidx = name[1:2] if name[0] == 'u' else name[1:3]
        o = (name[0], sum((i in SA for i in Aidx)), sum((i in SB for i in name[-2:])))
        weight = weights[o]
        if not weight >= 0:
            raise ValueError('Verification failed: weight >= 0')
        if name[0] == 'v':
            if not weight <= 2:
                raise ValueError('Verification failed: weight <= 2')
        for idx, q in row.items():
            total[idx] += weight * q
            ell[idx] += q
    for j, (i, l) in enumerate(E):
        total[j] += vals[-1] * int(i < a <= l)
        if not total[j] == ell[j] - sg * c * int((i, l) == target):
            raise ValueError('Verification failed: total[j] == ell[j] - sg * c * int((i, l) == target)')
    return len(rows)

def primal(a, r, form):
    E, ix, rows = geometry(a, r)
    e = [F(0) for _ in E]
    if form == 'inward':
        for j, (i, b) in enumerate(E):
            e[j] = F(-int(b < a or i >= a))
    elif form == 'single':
        e[ix[a, a + 1]] = F(-1)
    else:
        u = -F(r - 2, 3 * r - 4) if form == 'small' else -F(r - 2, 4 * (r - 1))
        v = -2 * u / (r - 2)
        y = -F(r - 4, 2 * (3 * r - 4)) if form == 'small' else F(1, 2 * (r - 1))
        t1 = u + v if form == 'small' else 2 * (u + v) - 2 * y
        for j, (i, b) in enumerate(E):
            if b < a:
                e[j] = y
            elif i < a:
                e[j] = u if b in {a, a + 1} else v
            else:
                cnt = int(i in {a, a + 1}) + int(b in {a, a + 1})
                e[j] = F(-1) if cnt == 2 else t1 if cnt == 1 else 2 * v
    if not max(map(abs, e)) == 1:
        raise ValueError('Verification failed: max(map(abs, e)) == 1')
    if not sum((e[j] for j, (i, b) in enumerate(E) if i < a <= b)) == 0:
        raise ValueError('Verification failed: sum((e[j] for j, (i, b) in enumerate(E) if i < a <= b)) == 0')
    slacks = [sum((F(q) * e[j] for j, q in row.items())) for _, row in rows]
    if not min(slacks) >= 0:
        raise ValueError('Verification failed: min(slacks) >= 0')
    return (E, e, sum(slacks))

def metric_checks(a, r, e, t):
    m = a + r
    E, _, _ = geometry(a, r)
    d = [[F(0) for _ in range(m)] for _ in range(m)]
    for j, (i, b) in enumerate(E):
        s = 2 if i >= a else 1
        inward = -int(b < a or i >= a)
        d[i][b] = d[b][i] = F(s) + t * e[j] + 4 * t * t * inward
    if not all((d[i][j] > 0 for i, j in E)):
        raise ValueError('Verification failed: all((d[i][j] > 0 for i, j in E))')
    triangles = 0
    ptolemy = 0
    for i, j, k in permutations(range(m), 3):
        if not d[i][j] <= d[i][k] + d[k][j]:
            raise ValueError('Verification failed: d[i][j] <= d[i][k] + d[k][j]')
        triangles += 1
    for i, j, k, l in combinations(range(m), 4):
        v = [d[i][j] * d[k][l], d[i][k] * d[j][l], d[i][l] * d[j][k]]
        if not all((2 * x <= sum(v) for x in v)):
            raise ValueError('Verification failed: all((2 * x <= sum(v) for x in v))')
        ptolemy += 3
    return (triangles, ptolemy)
SMALL = {(2, 3): F(6, 5), (2, 4): F(3, 2), (3, 3): F(9, 5), (3, 4): F(3), (3, 5): F(60, 11), (4, 4): F(5)}

def main(out):
    counts = {'small_certificates': 0, 'sampled_generic_certificates': 0, 'constraint_rows': 0, 'primal_directions': 0, 'triangle_checks': 0, 'ptolemy_checks': 0}
    for rec in load_certificates('small'):
        if calc(rec['c']) != SMALL[(rec['a'], rec['r'])]:
            raise ValueError('Certificate does not bind the claimed sharp constant')
        vals = list(map(calc, rec['values']))
        counts['constraint_rows'] += check_cert(rec['a'], rec['r'], rec['typ'], rec['sign'], calc(rec['c']), rec['orbits'], vals)
        counts['small_certificates'] += 1
    for rec in load_certificates('symbolic'):
        for k in sorted({rec['k_min'], rec['k_min'] + 1, 9, 12}):
            vals = [calc(z, k) for z in rec['values']]
            counts['constraint_rows'] += check_cert(k, k + rec['offset'], rec['kind'], rec['sign'], calc(rec['c'], k), rec['orbits'], vals)
            counts['sampled_generic_certificates'] += 1
    cases = list(SMALL) + [(a, a + d) for a in range(4, 9) for d in range(3) if (a, a + d) not in SMALL]
    for a, r in cases:
        c = SMALL.get((a, r), min(F(a * r, 2), F(a * (a + 1), 2)))
        form = 'small' if (a, r) in SMALL else 'upper' if r == a else 'single'
        for mode in [form, 'inward']:
            E, e, ell = primal(a, r, mode)
            counts['primal_directions'] += 1
            expect = F(a * r * (r - 1) * (3 * a - 1), 4) if mode == 'inward' else c
            if not ell == expect:
                raise ValueError((a, r, mode, ell, expect))
            for t in [F(1, 20), F(1, 1000)]:
                x, y = metric_checks(a, r, e, t)
                counts['triangle_checks'] += x
                counts['ptolemy_checks'] += y
    for t in [F(1, 10), F(1, 100), F(1, 1000)]:
        L = [1 + t, 1 - t, F(1)]
        d = [[F(0) for _ in range(4)] for _ in range(4)]
        for i in range(1, 4):
            d[0][i] = d[i][0] = L[i - 1]
        for i, j in combinations(range(1, 4), 2):
            d[i][j] = d[j][i] = L[i - 1] + L[j - 1]
        for i, j, k in permutations(range(4), 3):
            if not d[i][j] <= d[i][k] + d[k][j]:
                raise ValueError('Verification failed: d[i][j] <= d[i][k] + d[k][j]')
        prods = [d[0][1] * d[2][3], d[0][2] * d[1][3], d[0][3] * d[1][2]]
        if not all((2 * z <= sum(prods) for z in prods)):
            raise ValueError('Verification failed: all((2 * z <= sum(prods) for z in prods))')
    out.mkdir(parents=True, exist_ok=True)
    (out / 'exact_results.json').write_text(json.dumps({'status': 'PASS', 'counts': counts, 'universal_claims_are_not_inferred_from_sampled_k': True}, indent=2, sort_keys=True) + '\n')
    print('PASS:', counts)
if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    main(ap.parse_args().output)
