"""Exact finite checks for errata in Kirillov §§7–12.

These checks refute the printed assertions at explicit inputs; they do not certify
general functional-analytic theorems or use finite tests as proofs of them.
Run: sage checks/sage/part2_counterexamples.py
"""
from sage.all import QQ, CC, PolynomialRing, LaurentPolynomialRing, matrix
from sage.all import vector, identity_matrix, SR, var, exp, diff, I, QuadraticField


def refuted_check(name, condition):
    """Fail if a formerly false assertion unexpectedly passes its input."""
    assert not condition, name + ": printed assertion was not refuted"


# 8.1: ordinary equivalence of the middle representations is coarser than
# equivalence of extensions with identity maps on both fixed end modules.
j1 = matrix(QQ, [[1, 1], [0, 1]])
j2 = matrix(QQ, [[1, 2], [0, 1]])
d = matrix(QQ, [[2, 0], [0, 1]])
assert d * j1 * d.inverse() == j2
refuted_check("different nonzero cocycles imply inequivalent middles", j1 == j2)

# 8.3: image inclusion alone does not order oblique idempotents.
p = matrix(QQ, [[1, 1], [0, 0]])
q = matrix(QQ, [[1, 0], [0, 0]])
assert p * p == p and q * q == q
assert p.column_space() == q.column_space()
refuted_check("idempotent order from image inclusion", p * q == p and q * p == p)
assert not q.right_kernel().is_subspace(p.right_kernel())

# Check the repaired image+kernel criterion on all projections onto pairs
# of distinct rational lines from this explicit finite set (not all matrices).
lines = [vector(QQ, v) for v in ((1, 0), (0, 1), (1, 1), (1, -1), (1, 2))]
projections = [matrix(QQ, 2), identity_matrix(QQ, 2)]
for u in lines:
    for v in lines:
        c = matrix(QQ, [u, v]).transpose()
        if c.det():
            projections.append(c * q * c.inverse())
checked_pairs = 0
for p in projections:
    for q in projections:
        order = p * q == p and q * p == p
        inclusions = (p.column_space().is_subspace(q.column_space())
                      and q.right_kernel().is_subspace(p.right_kernel()))
        assert order == inclusions
        checked_pairs += 1

# A reducible indecomposable 2-dimensional representation of the free group
# has End_G(V)=QQ: scalar idempotent 1 is minimal, although V is not simple.
a = matrix(QQ, [[1, 0], [0, 2]])
b = matrix(QQ, [[1, 1], [0, 1]])
units = []
for i in range(2):
    for j in range(2):
        e = matrix(QQ, 2)
        e[i, j] = 1
        units.append(e)
constraints = matrix(QQ, [(e * a - a * e).list() + (e * b - b * e).list()
                           for e in units]).transpose()
assert constraints.right_kernel().dimension() == 1
assert a[1, 0] == b[1, 0] == 0

# 7.3 finite k: the tuple condition is vacuous at k=3 on this reducible H=QQ².
assert identity_matrix(QQ, 2).rank() < 3

# 7.3 infinite k: exact geometric-series constants in the ℓ² counterexample
# ξ1=Σ4^-n e_n, ξ_(n+1)=2^-n e_n, η1=e1, η_(n+1)=0.
xi1_norm2 = QQ(1) / 15
tail_norm2 = QQ(1) / 3
relation_norm2 = 1 + tail_norm2
assert xi1_norm2 + tail_norm2 == QQ(2) / 5
assert 1 / relation_norm2 == QQ(3) / 4
for n in range(1, 15):
    assert QQ(2)**(-n) * QQ(2)**(-n) == QQ(4)**(-n)

# 9.3: averaging T(g)T(g)* gives T(h)AT(h)*=A.  The printed conjugation
# would instead require the same equality for A^-1, which fails exactly.
t = matrix(QQ, [[1, -2], [0, -1]])
assert t * t == 1
av = (identity_matrix(QQ, 2) + t * t.transpose()) / 2
assert av == matrix(QQ, [[3, 1], [1, 1]])
assert t * av * t.transpose() == av
refuted_check("printed unitarizing conjugation",
              t * av.inverse() * t.transpose() == av.inverse())

# 10.4: preserving brackets is insufficient without linearity of ψ.
refuted_check("nonlinear abelian bracket map is additive", (1 + 1)**3 == 1**3 + 1**3)

# 10.3: a Choquet measure need not give a surjective GNS decomposition.
# Three rank-one states on M2 average to tr/2, but their direct integral
# has dimension6 whereas GNS(tr/2) has dimension4.
k3 = QuadraticField(3, "r3")
r3 = k3.gen()
trine = [vector(k3, [1, 0]), vector(k3, [-QQ(1)/2, r3/2]),
         vector(k3, [-QQ(1)/2, -r3/2])]
density = sum((v.column() * v.row() for v in trine)) / 3
assert density == identity_matrix(k3, 2) / 2
embedding = matrix(k3, [sum(((e * v).list() for v in trine), [])
                       for e in units]).transpose()
assert embedding.rank() == 4 and embedding.nrows() == 6
refuted_check("arbitrary Choquet GNS map is onto", embedding.rank() == 6)

# 11.1: with the positive Fourier convention and a scalar product linear in
# its first slot, f=z^-1, χ=z gives ∫fχ=1, but (f,χ)=0.
r = LaurentPolynomialRing(QQ, "z")
z = r.gen()
f, chi = z**-1, z
constant = lambda polynomial: polynomial[0]
assert constant(f * chi) == 1
refuted_check("central scalar without conjugate character",
              constant(f * chi) == constant(f * z**-1))

# 11.3: ψ(X)=-δ′, so its standard convolution differentiates with a minus.
x, aa, y = var("x aa y")
coefficient = exp(aa * x)
assert (-diff(coefficient, x)).simplify_full() == -aa * coefficient
refuted_check("central convolution without antipode",
              (-diff(coefficient, x) - aa * coefficient).is_zero())

# 11.3: connectedness is needed when the infinitesimal center is used.
# On the complex irreducible 2-dimensional representation of O(2), the
# Lie algebra generator is central in U(so(2)), but a reflection reverses it.
rot_generator = matrix(QQ, [[0, -1], [1, 0]])
reflection = matrix(QQ, [[1, 0], [0, -1]])
assert reflection * rot_generator * reflection == -rot_generator
refuted_check("infinitesimal center commutes with disconnected group",
              reflection * rot_generator == rot_generator * reflection)

# 12.1: for the positive kernel, F(xf)=-i∂_y F(f).
kernel = exp(I * x * y)
assert (-I * diff(kernel, y) - x * kernel).simplify_full() == 0
refuted_check("positive sign in coordinate multiplication",
              (I * diff(kernel, y) - x * kernel).simplify_full().is_zero())

# 12.2: the weight family 2^n is natural on weight spaces and tensorial,
# but is not unitary at n=1. Multiplicativity is exact on this finite range;
# the general equality is the elementary identity 2^(m+n)=2^m 2^n.
for m in range(-8, 9):
    for n in range(-8, 9):
        assert QQ(2)**(m + n) == QQ(2)**m * QQ(2)**n
refuted_check("unitarity follows from naturality and tensoriality", QQ(2)**2 == 1)

# 12.3: the monoid algebra with e²=e is a bialgebra, Δ(e)=e⊗e,
# ε(e)=1, but e is not invertible, so no antipode can satisfy S(e)e=1.
# Multiplication by e in basis(1,e) has image span(e), excluding 1.
multiply_e = matrix(QQ, [[0, 0], [1, 1]])
assert multiply_e * multiply_e == multiply_e
refuted_check("bialgebra automatically has antipode",
              vector(QQ, [1, 0]) in multiply_e.column_space())

# Infinite dual warning: the transpose of multiplication on K[t] can have
# arbitrarily high tensor rank.  ℓ(t^n)=1/(n+1) gives Hilbert matrices.
# These bounded checks illustrate the general positive Gram-matrix proof.
for n in range(1, 9):
    hankel = matrix(QQ, n, lambda i, j: QQ(1) / (i + j + 1))
    assert hankel.det() != 0

print("Exact counterexamples passed; repaired projector pairs:", checked_pairs)
print("Infinite-dimensional conclusions use the separate general arguments.")
