import numpy as np
from scipy.optimize import linprog
from itertools import combinations
from fractions import Fraction

def cone(a,r):
 m=a+r; E=list(combinations(range(m),2)); ix={e:k for k,e in enumerate(E)}; rows=[];names=[]
 for b,c in combinations(range(a,m),2):
  for i in range(a):
   d={(i,b):1,(i,c):1,(b,c):-1}; v=np.zeros(len(E));
   for e,q in d.items():v[ix[e]]=q
   rows.append(v);names.append(('u',i,b,c))
  for i,j in combinations(range(a),2):
   d={(i,b):1,(i,c):1,(j,b):1,(j,c):1,(i,j):-2,(b,c):-1};v=np.zeros(len(E))
   for e,q in d.items():v[ix[e]]=q
   rows.append(v);names.append(('v',i,j,b,c))
 D=np.array(rows); w=np.array([int(i<a<=j) for i,j in E]);return E,ix,D,w,names

def run(a,r):
 E,ix,D,w,names=cone(a,r); obj=D.sum(axis=0)
 result=[]
 for typ,e in [('A',(0,1)),('X',(0,a)),('B',(a,a+1))]:
  for s in (1,-1):
   row=np.zeros(len(E));row[ix[e]]=s
   opt=linprog(obj,A_ub=-D,b_ub=np.zeros(len(D)),A_eq=np.array([w,row]),b_eq=[0,1],bounds=[(-1,1)]*len(E),method='highs')
   result.append((typ,s, str(Fraction(float(opt.fun)).limit_denominator(100000)) if opt.success else opt.message))
 print(a,r,result,flush=True)
 return result
if __name__=='__main__':
 for a in range(2,9):
  for r in range(max(3,a),a+3): run(a,r)
