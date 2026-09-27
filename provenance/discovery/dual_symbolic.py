import sympy as S
import numpy as np
from scipy.optimize import linprog
from fractions import Fraction
from itertools import combinations
from explore import cone
k=S.symbols('k',integer=True,positive=True)
def orbit_data(a,r,typ):
 E,ix,D,w,names=cone(a,r)
 SA=set([0,1]) if typ=='A' else set([0]) if typ=='X' else set()
 SB=set([a,a+1]) if typ=='B' else set([a]) if typ=='X' else set()
 def ro(n):
  return (n[0],sum(i in SA for i in (n[1:2] if n[0]=='u' else n[1:3])),sum(i in SB for i in n[-2:]))
 def eo(e):
  i,j=e
  return ('A',sum(t in SA for t in e),0) if j<a else ('B',0,sum(t in SB for t in e)) if i>=a else ('X',int(i in SA),int(j in SB))
 ros=sorted(set(map(ro,names)));eos=sorted(set(map(eo,E)))
 mat=[];target=[]
 for eorb in eos:
  idx=next(i for i,e in enumerate(E) if eo(e)==eorb)
  row=[int(sum(D[j,idx] for j,n in enumerate(names) if ro(n)==o)) for o in ros]+[int(w[idx])]
  mat.append(row)
  er=E[idx]; target.append(int(er==((0,1) if typ=='A' else (a,a+1) if typ=='B' else (0,a))))
 return S.Matrix(mat),ros,eos,S.Matrix(target)

def interpolate(seq,typ):
 pts=list(range(5,10));arr=[]
 for z in pts:
  a=z;r=z+seq;arr.append(orbit_data(a,r,typ)[0])
 mat=S.zeros(*arr[0].shape)
 for i in range(mat.rows):
  for j in range(mat.cols):mat[i,j]=S.factor(S.interpolate([(z,arr[t][i,j]) for t,z in enumerate(pts)],k))
 # verify interpolation independent
 assert mat.subs(k,11)==orbit_data(11,11+seq,typ)[0]
 return mat,orbit_data(6,6+seq,typ)[1:]

def make(seq,typ,sign):
 mat,(ros,eos,indicator)=interpolate(seq,typ)
 c=k*k/2 if seq==0 else k*(k+1)/2
 rhs=mat[:,:-1]*S.ones(len(ros),1)-sign*c*indicator
 vars=S.symbols('v:'+str(mat.cols)); sol=S.linsolve((mat,rhs),vars);tup=next(iter(sol));free=set().union(*(x.free_symbols for x in tup))-{k}
 print('\nCASE',seq,typ,sign,'free',free)
 for z in [S.Rational(0),S.Rational(1,2),S.Rational(1),S.Rational(3,2),S.Rational(2),1/(k-1)]:
  vals=[S.factor(x.subs({s:z for s in free})) for x in tup]
  n=S.symbols('n',nonnegative=True);k0=5 if seq==0 else 4
  ok=True
  for x in vals[:-1]:
   num,den=S.fraction(S.factor(x.subs(k,k0+n)))
   if not (all(c>=0 for c in S.Poly(num,n).all_coeffs()) and all(c>=0 for c in S.Poly(den,n).all_coeffs())):ok=False
  if ok:
   print('WORKS',z,list(zip(ros+['mu'],vals)));assert mat*S.Matrix(vals)==rhs or all(S.simplify(x)==0 for x in mat*S.Matrix(vals)-rhs);return mat,ros,eos,rhs,vals,k0
 print('NO SIMPLE',tup)
 return mat,ros,eos,rhs,tup,k0
if __name__=='__main__':
 import pickle
 out=[]
 for seq in range(3):
  for typ in 'AXB':
   for sign in [1,-1]:out.append((seq,typ,sign,make(seq,typ,sign)))
 with open('/mnt/data/_rigidity_next/symbolic_duals.pkl','wb') as f:pickle.dump(out,f)
