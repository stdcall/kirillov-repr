"""Finite exact obstruction to a function-valued map before null quotients.

G=H=C2, X is a point, and the inducing representation is trivial.
The integrated cyclic representation sends alpha to sum(alpha).  Formula
13.2(21), before the null quotient, sends alpha to the nonzero kernel
F_alpha(g1,g2)=alpha(g1^-1*g2), even when its integrated vector is zero.
The scalar form on the inducing space is Q(theta)=abs(sum(theta))^2.
These finite checks verify the obstruction and its quotient repair only;
the general positivity argument uses localization on H\G.
"""
from sage.all import QQ, matrix, vector

alpha = vector(QQ, [1, -1])
integrated_vector = sum(alpha)
kernel = matrix(QQ, 2, 2, lambda g1, g2: alpha[(g2 - g1) % 2])
assert integrated_vector == 0
assert kernel != 0  # Refutes a map from the integrated vector to literal F.
assert all(sum(kernel.row(g1)) == 0 for g1 in range(2))

samples = [vector(QQ, [a, b]) for a in range(-2, 3) for b in range(-2, 3)]
for theta in samples:
    q = sum(theta) ** 2
    assert q >= 0
    shifted = vector(QQ, [theta[1], theta[0]])
    assert sum(shifted) == sum(theta)
    assert q == sum(shifted) ** 2
assert matrix(QQ, [[1, 1], [1, 1]]).rank() == 1
print("C2 obstruction and rank-one null quotient verified exactly")
