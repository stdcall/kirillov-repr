"""PBW identities and central-character normalization, sections 15.7 and 18.3.

Use the independent PBW algebra of the explicitly given sl_2 brackets.
The Casimir C=X^2+Y^2+Z^2 equals -EF+H(2-H)/4. Check its centrality,
the two iterated-commutator formulas and all three components of E^n F
for n=1..8. Check C on the finite irreducibles of highest weights 0..12.
The general coefficient formulas follow by matching H^2,H and 1 in
the displayed commutator identities; this finite check is not a proof
of the classification of all ideals or all representations.
"""

from itertools import permutations
from sage.all import (LieAlgebra, QQ, matrix, identity_matrix, prod,
                      factorial, PolynomialRing)

L = LieAlgebra(QQ, {("H", "E"): {"E": 2},
                    ("H", "F"): {"F": -2},
                    ("E", "F"): {"H": 1}}, names=("E", "H", "F"))
U = L.universal_enveloping_algebra()
E, H, F = U.gens()
C = -E*F + H*(2-H)/4
adF = lambda x: F*x-x*F
assert all(C*x == x*C for x in (E, H, F))
checks = 3
for n in range(1, 9):
    first = adF(E**n)
    second = adF(adF(E**(n+1)))
    assert first == -n*E**(n-1)*(H+n-1)
    assert second == -(n+1)*(2*E**n*F - n*E**(n-1)*(H+n)*(H+n-1))
    a = -QQ(1)/(2*(n+1)*(2*n+1))
    b = -QQ(1)/2
    alpha = -QQ(2*n)/(2*n+1)
    beta = -QQ(n**3-n)/(4*n+2)
    assert (alpha*C+beta)*E**(n-1) == (
        -alpha*E**n*F + E**(n-1)*(alpha*H*(2-H)/4+beta))
    assert E**n*F == a*second + b*first + (alpha*C+beta)*E**(n-1)
    assert beta/alpha == QQ(n*n-1)/4
    printed_alpha = QQ(n)/(4*n-2)
    printed_beta = QQ(n**3-n)/(4*n-2)
    assert (printed_alpha*C+printed_beta)*E**(n-1) != (
        4*printed_alpha*E**n*F +
        E**(n-1)*(printed_alpha*H*(2-H)+printed_beta))
    checks += 6

for k in range(13):
    e = matrix(QQ, k+1, lambda i, j: j if i == j-1 else 0)
    f = matrix(QQ, k+1, lambda i, j: k-j if i == j+1 else 0)
    h = matrix.diagonal(QQ, [k-2*j for j in range(k+1)])
    central = -e*f + h*(2*identity_matrix(QQ, k+1)-h)/4
    assert central == -QQ(k*(k+2))/4*identity_matrix(QQ, k+1)
    if k:
        assert central != -k*(k+2)*identity_matrix(QQ, k+1)
    checks += 1

compact = LieAlgebra(QQ, {("X", "Y"): {"Z": 1},
                          ("Y", "Z"): {"X": 1},
                          ("X", "Z"): {"Y": -1}}, names=("X", "Y", "Z"))
V = compact.universal_enveloping_algebra()
x, y, z = V.gens()
c = x*x+y*y+z*z

def symmetrize(word):
    return sum((prod(p, V.one()) for p in permutations(word)), V.zero()) / factorial(len(word))

sym_R2 = (x**4+y**4+z**4 + 2*symmetrize((x, x, y, y))
          + 2*symmetrize((x, x, z, z)) + 2*symmetrize((y, y, z, z)))
assert sym_R2 != c*c-QQ(1)/3*c  # Printed reading is refuted.
assert sym_R2 == c*c+QQ(1)/3*c
checks += 2

# Compute the Duflo correction independently from ad(X), through degree 4.
# In this compact basis j(X)=det(P(ad X))^(1/2), P(t)=sinh(t/2)/(t/2).
# Its constant-coefficient operator is applied to R and R^2 before PBW.
S = PolynomialRing(QQ, names=('a', 'b', 'd'))
a, b, d = S.gens()
radial = a*a+b*b+d*d
adjoint = matrix(S, [[0, -d, b], [d, 0, -a], [-b, a, 0]])
assert (adjoint**2).trace() == -2*radial
assert (adjoint**4).trace() == 2*radial**2
j2 = (adjoint**2).trace()/48
j4 = (adjoint**2).trace()**2/4608 - (adjoint**4).trace()/5760
assert j2 == -radial/24 and j4 == radial**2/1920

def laplace(p):
    return sum(p.derivative(v, 2) for v in S.gens())

assert radial-laplace(radial)/24 == radial-QQ(1)/4
assert radial**2-laplace(radial**2)/24+laplace(laplace(radial**2))/1920 == (
    radial**2-QQ(5)/6*radial+QQ(1)/16)
assert sym_R2-QQ(5)/6*c+QQ(1)/16 == (c-QQ(1)/4)**2
checks += 6

print(f"ok sl2_casimir_normalization: {checks} checks; "
      "PBW powers 1..8 and highest weights 0..12")
