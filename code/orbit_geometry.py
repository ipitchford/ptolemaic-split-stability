"""Direct combinatorial orbit counts; no interpolation, optimisation or generated formulas."""
from collections import Counter
from itertools import combinations
import sympy as sp

def choose(x, j):
    if j == 0: return sp.Integer(1)
    if j == 1: return x
    if j == 2: return x*(x-1)/2
    return sp.Integer(0)

def orbit_matrix(a, r, kind):
    """Rows: edge orbits. Columns: constraint orbits, then cross-normalisation."""
    sa, sb = {'A': (2, 0), 'X': (1, 1), 'B': (0, 2)}[kind]
    def count(side, length, special):
        ns, total = (sa, a) if side == 'A' else (sb, r)
        return choose(sp.Integer(ns), special)*choose(total-ns, length-special)
    def vertices(side, length, special):
        return [(side,1,i) for i in range(special)]+[(side,0,i) for i in range(length-special)]
    def edge_type(x,y):
        if x[0] == y[0]:
            return (x[0],x[1]+y[1],0) if x[0]=='A' else ('B',0,x[1]+y[1])
        if x[0] != 'A': x,y=y,x
        return ('X',x[1],y[1])
    edge_sizes={}
    for j in range(3):
        for side in ['A','B']:
            z=sp.factor(count(side,2,j))
            if z!=0:edge_sizes[(side,j,0) if side=='A' else (side,0,j)]=z
    for i in range(2):
        for j in range(2):
            z=sp.factor(count('A',1,i)*count('B',1,j))
            if z!=0:edge_sizes[('X',i,j)]=z
    edge_orbits=sorted(edge_sizes)
    data=[]
    for typ, na in [('u',1),('v',2)]:
        for i in range(na+1):
            for j in range(3):
                mult=sp.factor(count('A',na,i)*count('B',2,j))
                if mult==0: continue
                av=vertices('A',na,i);bv=vertices('B',2,j)
                terms=[]
                for x in av:
                    for y in bv:terms.append((edge_type(x,y),1))
                terms.append((edge_type(*bv),-1))
                if typ=='v':terms.append((edge_type(*av),-2))
                cs=Counter()
                for o,z in terms:cs[o]+=z
                data.append(((typ,i,j),mult,cs))
    data.sort(key=lambda z:z[0]); rows=[]
    for o in edge_orbits:
        rows.append([sp.cancel(mult*cs[o]/edge_sizes[o]) for _,mult,cs in data]+[sp.Integer(o[0]=='X')])
    M=sp.Matrix(rows)
    target={'A':('A',2,0),'X':('X',1,1),'B':('B',0,2)}[kind]
    indicator=sp.Matrix([int(o==target) for o in edge_orbits])
    return M,[o for o,_,_ in data],edge_orbits,indicator,[mult for _,mult,_ in data]
