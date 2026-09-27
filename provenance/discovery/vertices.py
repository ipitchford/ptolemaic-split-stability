import sympy as s
a,r=s.symbols('a r',positive=True); N=a*(a+1)/2;theta=(a-1)/(a+1); u,Y=s.symbols('u Y');v=-2*u/(r-2);g=u+v
# u<=0 implies g/2>=v? diff u/2? g/2-v=u/2-v/2=u*r/(2(r-2)) <=0. so switch g/2 <= v for u negative.
# low region Y<=g/2: t1=g,t2=2v; middle g/2<=Y<=v t1=2g-2Y,t2=2v; high Y>=v t1=2g-2Y, t2=4v-2Y
verts={'left':(-s.Rational(1,2),-s.Rational(1,2)),'lowercross':(-(r-2)/(3*r-4),-(r-4)/(2*(3*r-4))),'uppercross':(-(r-2)/(4*(r-1)),1/(2*(r-1))),'origin':(0,0)}
for name,(uu,yy) in verts.items():
 for case,(t1,t2) in enumerate([(g,2*v),(2*g-2*Y,2*v),(2*g-2*Y,4*v-2*Y)]):
  E=N*(1-r*(r-1)*theta*Y-2*(r-2)*t1-((r-2)*(r-3)/2)*t2)
  print(name,case,s.factor(E.subs({u:uu,Y:yy})))
