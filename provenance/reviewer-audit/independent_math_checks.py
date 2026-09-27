"""Reviewer checks built from raw triangle/Ptolemy inequalities.
No imports from the authors' code. LP checks are numerical corroboration;
the dual identities below use exact rational arithmetic at k=13.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json, math
import numpy as np
import scipy.sparse as sparse
from scipy.optimize import linprog
import sympy as sp
import argparse
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--bundle', required=True, type=Path, help='Extracted v0.3 bundle root')
parser.add_argument('--output', required=True, type=Path, help='Directory for the reviewer result')
args = parser.parse_args()
ROOT = args.bundle.resolve()
OUT = args.output.resolve()
if not (ROOT/'certificates/small_duals.json').is_file():
    parser.error('--bundle is not an extracted v0.3 bundle root')
if OUT == ROOT or ROOT in OUT.parents:
    parser.error('--output must be outside the source bundle')
OUT.mkdir(parents=True, exist_ok=True)

def check(condition, message):
    if not condition: raise RuntimeError(message)

def geometry(a,r):
    n=a+r; edges=list(combinations(range(n),2)); pos={e:j for j,e in enumerate(edges)}
    dist={e:2 if e[0]>=a else 1 for e in edges}; rows=[]; metadata=[]
    def edge(i,j): return (min(i,j),max(i,j))
    for tri in combinations(range(n),3):
        for opposite in tri:
            endpoints=tuple(x for x in tri if x!=opposite)
            positive=[edge(opposite,x) for x in endpoints]; negative=edge(*endpoints)
            if sum(dist[x] for x in positive)-dist[negative]==0:
                row=Counter({pos[x]:1 for x in positive}); row[pos[negative]]-=1
                rows.append(dict(row)); metadata.append(('u',tuple(x for x in tri if x<a),tuple(x for x in tri if x>=a)))
    for q in combinations(range(n),4):
        i,j,k,l=q
        products=[((i,j),(k,l)),((i,k),(j,l)),((i,l),(j,k))]
        values=[dist[u]*dist[v] for u,v in products]
        for negative in range(3):
            if sum(values)-2*values[negative]!=0: continue
            row=Counter()
            for t,(u,v) in enumerate(products):
                sign=-1 if t==negative else 1
                row[pos[u]]+=sign*dist[v]; row[pos[v]]+=sign*dist[u]
            rows.append({j:c for j,c in row.items() if c})
            metadata.append(('v',tuple(x for x in q if x<a),tuple(x for x in q if x>=a)))
    rr=[];cc=[];vv=[]
    for i,row in enumerate(rows):
        for j,c in row.items():rr.append(i);cc.append(j);vv.append(c)
    D=sparse.csr_matrix((vv,(rr,cc)),shape=(len(rows),len(edges)),dtype=float)
    w=np.array([int(i<a<=j) for i,j in edges],dtype=float)
    ell=np.asarray(D.sum(axis=0)).ravel()
    expected=np.array([-r*(r-1) if j<a else -a*(a+1)/2 if i>=a else a*(r-1) for i,j in edges])
    check(np.array_equal(ell,expected),'Raw constraints did not give claimed objective')
    check(len(rows)==a*(a+1)//2*(r*(r-1)//2),'Unexpected active-constraint count')
    return edges,pos,rows,metadata,D,w,ell

small={(2,3):F(6,5),(2,4):F(3,2),(3,3):F(9,5),(3,4):F(3),(3,5):F(60,11),(4,4):F(5)}
records=json.loads((ROOT/'certificates/small_duals.json').read_text())
symbolic=json.loads((ROOT/'certificates/symbolic_duals.json').read_text())
check({(z['a'],z['r'],z['typ'],z['sign']) for z in records}=={(a,r,t,s) for a,r in small for t in 'AXB' for s in [-1,1]},'Small certificate coverage')
check({(z['offset'],z['kind'],z['sign']) for z in symbolic}=={(d,t,s) for d in range(3) for t in 'AXB' for s in [-1,1]},'Universal certificate coverage')
cache={}
def geom(a,r):
    if (a,r) not in cache:cache[a,r]=geometry(a,r)
    return cache[a,r]

def exact_dual(rec,a,r,kind,k=None):
    E,ix,rows,meta,_,w,ell=geom(a,r)
    def val(s):
        z=sp.sympify(s)
        if k is not None:z=z.subs(sp.Symbol('k'),k)
        return F(str(z))
    weights={tuple(o):val(v) for o,v in zip(rec['orbits'],rec['values'][:-1])}
    mu=val(rec['values'][-1]); c=val(rec['c']);total=[F(0) for _ in E]
    SA={0,1} if kind=='A' else {0} if kind=='X' else set()
    SB={a,a+1} if kind=='B' else {a} if kind=='X' else set()
    for row,(typ,A,B) in zip(rows,meta):
        o=(typ,len(set(A)&SA),len(set(B)&SB)); eta=weights[o]
        check(eta>=0 and (typ!='v' or eta<=2),'Inadmissible dual weight')
        for j,t in row.items():total[j]+=eta*t
    f=(0,1) if kind=='A' else (0,a) if kind=='X' else (a,a+1)
    for j in range(len(E)):
        check(total[j]+mu*int(w[j])==F(int(ell[j]))-rec['sign']*c*int(j==ix[f]),'Dual identity failed')
    check(c==(small[(a,r)] if (a,r) in small else F(a*a,2) if a==r else F(a*(a+1),2)),'Unexpected c')
    return len(rows)
row_checks=0
for rec in records:row_checks+=exact_dual(rec,rec['a'],rec['r'],rec['typ'])
for rec in symbolic:row_checks+=exact_dual(rec,13,13+rec['offset'],rec['kind'],13)

lp_results=[]
for a,r in list(small)+[(4,5),(4,6),(5,5),(5,6),(5,7),(6,6)]:
    E,ix,rows,meta,D,w,ell=geom(a,r);faces=[]
    for typ,f in [('A',(0,1)),('X',(0,a)),('B',(a,a+1))]:
        unit=np.zeros(len(E));unit[ix[f]]=1
        for sign in [-1,1]:
            res=linprog(ell,A_ub=-D,b_ub=np.zeros(D.shape[0]),A_eq=np.stack([w,unit]),b_eq=[0,sign],bounds=[(-1,1)]*len(E),method='highs')
            check(res.success or res.status==2,f'LP failed unexpectedly {a,r,typ,sign}: {res.message}')
            faces.append({'type':typ,'sign':sign,'feasible':bool(res.success),'minimum':float(res.fun) if res.success else None})
    observed=min(z['minimum'] for z in faces if z['feasible'])
    c=small[(a,r)] if (a,r) in small else F(a*a,2) if a==r else F(a*(a+1),2)
    check(abs(observed-float(c))<1e-8,f'LP sharp constant mismatch {a,r}')
    lp_results.append({'a':a,'r':r,'claimed_c':str(c),'observed_minimum':observed,'faces':faces})

p7=math.log2(F(16,9));p4=math.log2(3)
report={'status':'PASS','certificate_coverage':{'small':len(records),'universal':len(symbolic)},'raw_constraint_exact_dual_checks':{'small_certificates':36,'universal_certificates_at_k13':18,'constraint_rows':row_checks},'independent_numerical_lp':{'face_problems':len(lp_results)*6,'pairs':lp_results},'spot_constants':{'seven_point_p':p7,'seven_point_lower_slope':2*p7/21,'seven_point_upper_slope':16*p7/7,'four_point_quadratic_coefficient':p4*(2*p4-3)/8},'proof_limits':'The k=13 and floating-point LP checks are corroborative, not proofs for all k. The supplied universal symbolic proof was audited separately.'}
(OUT/'independent_math_results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='independent_numerical_lp'},indent=2));print('Independent LP face problems:',len(lp_results)*6)
