"""Exact local modular factors for normalized induced kernels.

The calculations do not assert boundedness of a global integral operator.
The cutoff counterexample itself is the elementary divergent integral of 1
on R with H1=H2=G; the distributional repair is proved by averaging P2.
"""
from sage.all import SR, matrix, var

a, b, c, d, t1, t2, u1, u2 = var("a b c d t1 t2 u1 u2")
g = matrix(SR, [[a, b], [c, d]])
h1 = matrix(SR, [[t1, u1], [0, 1 / t1]])
h2 = matrix(SR, [[t2, u2], [0, 1 / t2]])
transformed_c = (h1 * g * h2)[1, 0]
assert (transformed_c - c * t2 / t1).simplify_full() == 0
assert (1 / transformed_c - (t1 / t2) / c).simplify_full() == 0
# Refutes the old weight-free covariance already on the open big cell.
assert (1 / transformed_c - 1 / c).subs(c=3, t1=2, t2=5) != 0

# ax+b: drG=da db/a on a>0, Delta_G(a,b)=a.
inv = matrix(SR, [[-1 / a**2, 0], [b / a**2, -1 / a]])
assert (inv.det() - 1 / a**3).simplify_full() == 0
pulled_right_haar_density = a * inv.det()
assert (pulled_right_haar_density - 1 / a**2).simplify_full() == 0
assert (pulled_right_haar_density - (1 / a) * (1 / a)).simplify_full() == 0
print("SL2 local covariance and ax+b inversion density verified exactly")
