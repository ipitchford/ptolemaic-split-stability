from dual_symbolic import orbit_data
import numpy as np,sympy as s,json
from scipy.optimize import linprog
C={(2,3):s.Rational(6,5),(2,4):s.Rational(3,2),(3,3):s.Rational(9,5),(3,4):s.Integer(3),(3,5):s.Rational(60,11),(4,4):s.Integer(5)}
out=[]
for (a,r),c in C.items():
 for typ in 'AXB':
  M,ros,eos,ind=orbit_data(a,r,typ); ell=M[:,:-1]*s.ones(len(ros),1)
  for sign in [1,-1]:
   rhs=ell-c*sign*ind
   opt=linprog(np.r_[np.ones(len(ros)),0],A_eq=np.array(M).astype(float),b_eq=np.array(rhs).astype(float).ravel(),bounds=[(0,2 if o[0]=='v' else None) for o in ros]+[(None,None)],method='highs')
   if not opt.success: print('FAIL',a,r,typ,sign);continue
   vals=[s.Rational(float(x)).limit_denominator(1000000) for x in opt.x]
   assert M*s.Matrix(vals)==rhs
   assert all(x>=0 for x in vals[:-1]); assert all(vals[j]<=2 for j,o in enumerate(ros) if o[0]=='v')
   out.append(dict(a=a,r=r,typ=typ,sign=sign,c=str(c),orbits=ros,values=list(map(str,vals))))
print('all',len(out))
json.dump(out,open('/mnt/data/_rigidity_next/small_duals.json','w'),indent=2)
