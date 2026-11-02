"""Exact prequantization commutators and bundle gluing.

Passages: eq:quantization-commutator-correspondence,
eq:prequantization-curvature, eq:prequantization-local-gluing.
Use {F,G}=F_p G_q-F_q G_p, c=ih/(2pi), Q_F=c xi_F+F+alpha(xi_F).
The general residual is c({F,G}+2 d alpha(xi_F,xi_G)); hence d alpha=-omega.
The tests cover polynomial observables on one cotangent coordinate chart.
They do not assert global existence, self-adjointness or integrability.
Both the printed alpha=+p dq and an isolated sign change in Q are refuted
alongside the corrected chain, retaining the printed transition functions.
"""

from sage.all import *
from datetime import datetime, timezone
p,q,c=var('p q c')
# c=i*h/(2*pi), treated as a nonzero indeterminate.
def pb(f,g): return diff(f,p)*diff(g,q)-diff(f,q)*diff(g,p)
def op(f,u,alpha_sign): return c*pb(f,u)+f*u+alpha_sign*p*diff(f,p)*u
def comm(f,g,u,s): return expand(op(f,op(g,u,s),s)-op(g,op(f,u,s),s))
fs=[SR(1),p,q,p*p,p*q,q*q,p*p*q,p*q*q]
us=[SR(1),p,q,p*q,p*p+q*q]
count=0
for f in fs:
 for g in fs:
  for u in us:
   assert expand(comm(f,g,u,-1)/c-op(pb(f,g),u,-1))==0
   count+=1
# Original alpha=+p*dq gives a concrete failure, not merely different code.
wrong=expand(comm(p,q,SR(1),1)/c-op(pb(p,q),SR(1),1))
assert wrong==2
# Keeping (5) but replacing only its alpha sign requires changing gluing too.
# a_jk=q, alpha_k=0, alpha_j=dq; source g=exp(-a/c).
g_source=exp(-q/c);g_alternative=exp(q/c)
def local_op(f,u,a_q,sign): return c*pb(f,u)+f*u+sign*a_q*diff(f,p)*u
for f in fs:
 for u in us:
  assert (g_source*local_op(f,u,0,1)-local_op(f,g_source*u,1,1)).simplify_full()==0
wrong_glue=(g_source*local_op(p,SR(1),0,-1)-local_op(p,g_source,1,-1)).simplify_full()
assert wrong_glue==2*exp(-q/c)
# Commutator coefficient must be 1/c, not c (nor the printed i*h/(2*h)).
assert expand(comm(p,q,SR(1),-1))==c
print('Sage',version())
print('UTC',datetime.now(timezone.utc).isoformat())
print('Corrected chain: alpha=-p dq, d alpha=-omega; [QF,QG]/c=Q{F,G}:',count,'exact polynomial checks')
print('Original alpha=+p dq witness residual:',wrong)
print('Original gluing plus alpha: 40 exact checks; isolated alpha-sign change fails with residual:',wrong_glue)
print('For p,q the commutator on 1 is',c,'; coefficient 1/c gives 1, coefficient c gives',c*c)
