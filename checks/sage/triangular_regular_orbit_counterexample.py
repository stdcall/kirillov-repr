"""Refute completeness of the big-cell regular-orbit family, source p.319.

Use the trace pairing on the real upper triangular Lie algebra t(4).
An explicit strictly lower triangular F has a Kirillov matrix of rank8.
This is globally maximal: the central identity always belongs to its
kernel, so an alternating form on the10-dimensional algebra has rank≤8.
Yet F41=0, and the block action Z↦BZA^-1 preserves the zero of Z21.
The proposed antidiagonal J_epsilon has a nonzero21 entry. Thus this
regular orbit never meets the book's proposed canonical family.

This does not classify all other regular orbits. It gives one exact
counterexample and a general block invariant, without testing Typst.
"""
from datetime import datetime, timezone
from sage.all import QQ, PolynomialRing, matrix, identity_matrix, version

F=matrix(QQ, [[0,0,0,0],[1,0,0,0],[1,1,0,0],[0,1,1,0]])
indices=[(i,j) for i in range(4) for j in range(i,4)]
basis=[matrix(QQ,4,4,lambda r,c:int(r==i and c==j)) for i,j in indices]
kirillov=matrix(QQ,[[(F*(x*y-y*x)).trace() for y in basis] for x in basis])
assert kirillov == -kirillov.transpose()
assert kirillov.rank()==8
assert all((F*(identity_matrix(QQ,4)*x-x*identity_matrix(QQ,4))).trace()==0
           for x in basis)
assert len(kirillov.right_kernel().basis())==2

K=PolynomialRing(QQ,names=('a','b','d','e','f','g','u','v','w','z')).fraction_field()
a,b,d,e,f,g,u,v,w,z=K.gens()
A=matrix(K,[[a,b],[0,d]])
B=matrix(K,[[e,f],[0,g]])
Z=matrix(K,[[u,v],[z,w]])
assert (B*Z*A.inverse())[1,0]==g*z/a
assert F[3,0]==0
print(version())
print(datetime.now(timezone.utc).isoformat())
print('F=',F.list())
print('Kirillov rank8, kernel dimension2; maximality follows from central I and even rank.')
print('General transformed lower-left entry = g*z/a; canonical J_epsilon has z=±1.')
