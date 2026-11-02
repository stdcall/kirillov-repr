"""Exact exterior powers, Pfaffian normalization and positivity.

Passages: eq:pfaffian-exterior-power,
eq:orbit-plancherel-pfaffian-density, eq:orbit-plancherel-polynomial-density.
The algebra isomorphism J_k=k! times a normalized alternating tensor
transports the author's exterior product to the ordinary exterior product.
It does not remove the 1/2 in the sum over all ordered indices or 1/n!
in the top exterior power. The general coefficient of the printed expression
is 2^n n! Pf(A), by expansion over unordered pairs and their permutations.
Checks cover 30 rational matrices of orders 2,4,6; the 2x2 original reading
is explicitly refuted. The Heisenberg test checks positivity, not a general
proof of the Plancherel decomposition theorem.
"""

from sage.all import *
from datetime import datetime,timezone
checks=0
for n in [1,2,3]:
 E=ExteriorAlgebra(QQ,names=tuple('x'+str(i) for i in range(2*n)))
 xs=E.gens();top=prod(xs)
 for seed in range(1,11):
  A=matrix(QQ,2*n,2*n,lambda i,j: 0 if i==j else ((seed+3*i+7*j)%13-6) if i<j else -((seed+3*j+7*i)%13-6))
  form=sum(A[i,j]*xs[i]*xs[j] for i in range(2*n) for j in range(2*n))/2
  pf=A.pfaffian()
  assert form**n/factorial(n)==pf*top
  assert pf**2==A.det()
  # Source omits both divisors: compare exterior coefficients exactly.
  original=(2*form)**n
  assert original==(2**n*factorial(n)*pf)*top
  checks+=1
A=matrix(QQ,[[0,1],[-1,0]])
assert A.pfaffian()==1
# Heisenberg: [X,Y]=Z, orbit z=lambda. Ordered (X,Y) gives Pf=lambda.
assert matrix(QQ,[[0,-1],[1,0]]).pfaffian()==-1
print(version());print(datetime.now(timezone.utc).isoformat())
print(checks,'exact exterior/Pfaffian/determinant checks (2x2,4x4,6x6)')
print('Original coefficient = 2^n n! Pf(A); for A=[[0,1],[-1,0]] source c=2, det=1, c^2=4.')
print('Heisenberg lambda=-1 gives Pf=-1, so positive Plancherel density requires absolute value.')
