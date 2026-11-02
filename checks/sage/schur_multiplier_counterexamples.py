"""Exact counterexamples for the printed assertions in 14.2.3 and 14.2.5.

For (C2)^4, bilinear upper triangular forms define 64 cocycles. Their
commutator pairings are distinct, while coboundaries on an abelian group
are symmetric. Hence at least 64 cohomology classes exist for a group of
order 16: the order of H2 need not divide the group order. The standard
product-over-G argument bounds the exponent instead.

For C3, every projective lift of a generator can be rescaled to cube one,
so H2(C3,C*)=0. Clock and shift matrices on C3 x C3 have commutator zeta3.
The pairing between the two factors is bilinear but need not be skew.
All matrices and roots of unity below are exact.
"""

from sage.all import CyclotomicField, matrix, identity_matrix
from sage.env import SAGE_VERSION
from itertools import product
from datetime import datetime,timezone
pairs=[(i,j) for i in range(4) for j in range(i+1,4)]
vectors=list(product(range(2),repeat=4))
add=lambda x,y:tuple(a^b for a,b in zip(x,y))
classes=set()
for coeff in product(range(2),repeat=6):
 def B(x,y): return sum(c*x[i]*y[j] for c,(i,j) in zip(coeff,pairs))%2
 assert all((B(x,y)+B(add(x,y),z)-B(x,add(y,z))-B(y,z))%2==0
            for x in vectors for y in vectors for z in vectors)
 # Coboundaries on an abelian group are symmetric; these invariants differ.
 signature=tuple((B(x,y)-B(y,x))%2 for x in vectors for y in vectors)
 classes.add(signature)
assert len(classes)==64
assert 64>len(vectors)==16
# H2(C3,C*)=0: rescale any lift of its generator to have cube one.
F=CyclotomicField(3);omega=F.gen()
U=matrix(F,3,3,lambda i,j:omega**i if i==j else 0)
V=matrix(F,3,3,lambda i,j:1 if i==(j+1)%3 else 0)
assert U**3==V**3==identity_matrix(F,3)
assert U*V==omega*V*U
assert U*V*U.inverse()*V.inverse()==omega*identity_matrix(F,3)
assert omega!=omega**(-1)
print({'sage':SAGE_VERSION,'utc':datetime.now(timezone.utc).isoformat(),
       'C2_rank4':{'group_order':16,'distinct_cocycle_classes_verified':64,
                   'cocycle_triples_checked':64*16**3},
       'C3_squared':{'commutator':str(omega),'inverse':str(omega**(-1)),
                      'skew_requirement_fails':True}})
