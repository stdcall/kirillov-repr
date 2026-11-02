"""Clifford commutators and the two-dimensional spin target (17.3).

For n=2..8, check every elementary skew matrix and every Clifford
generator using the defining positive-square convention e_i^2=1.
The book's half of the sum over ALL i,j doubles the required action.
The corrected quarter of that sum acts by the columns of A; acting by
the printed rows gives its negative. General validity follows directly
from [e_i e_j,e_k]=2(delta_jk e_i-delta_ik e_j), not from this finite range.

The Pauli matrices independently refute a uniform orthogonal target:
their three bivectors span sl_2, while so_2 has dimension one. They have
no nonzero invariant symmetric bilinear form. This does not classify
spinor bilinear forms in all dimensions.
"""

from sage.all import (CliffordAlgebra, QuadraticForm, QQ, QuadraticField,
                      identity_matrix, matrix, vector)

checks = 0
for n in range(2, 9):
    Q = QuadraticForm(QQ, 2 * identity_matrix(QQ, n))
    C = CliffordAlgebra(Q)
    e = C.gens()
    assert all(x*x == C.one() for x in e)
    for i in range(n):
        for j in range(i+1, n):
            corrected = QQ(1)/2 * e[i]*e[j]
            printed = e[i]*e[j]
            for k in range(n):
                column = (e[i] if k == j else C.zero()) - (
                    e[j] if k == i else C.zero())
                actual = corrected*e[k] - e[k]*corrected
                assert actual == column
                assert printed*e[k] - e[k]*printed == 2*column
                if column:
                    assert actual != -column
                    assert printed*e[k] - e[k]*printed != column
                checks += 1

K = QuadraticField(-1, "I")
I = K.gen()
pauli = (matrix(K, [[0, 1], [1, 0]]),
         matrix(K, [[0, -I], [I, 0]]),
         matrix(K, [[1, 0], [0, -1]]))
bivectors = [pauli[i]*pauli[j] for i in range(3) for j in range(i+1, 3)]
assert all(a.trace() == 0 for a in bivectors)
assert matrix(K, [a.list() for a in bivectors]).rank() == 3
symmetric_basis = (matrix(K, [[1, 0], [0, 0]]),
                   matrix(K, [[0, 1], [1, 0]]),
                   matrix(K, [[0, 0], [0, 1]]))
columns = [vector(K, sum(((a.transpose()*B+B*a).list()
                         for a in bivectors), [])) for B in symmetric_basis]
invariance = matrix(K, columns).transpose()
assert invariance.right_kernel().dimension() == 0

print(f"ok spin_clifford_normalization: {checks} generator actions "
      "in dimensions 2..8; Pauli target counterexample")
