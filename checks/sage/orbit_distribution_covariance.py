r"""Finite model of the missing coefficient action in section 13.5, p.229.

G=S3 acts on the right cosets H\G, H={1,(12)}. U is the standard
two-dimensional representation over QQ. A point distribution with vector
v at H has Phi(g)=phi(Hg)*v. Averaging is computed directly from the
printed formula, for all eight possible section cutoffs and all three
coordinate test functions. H-fixed v gives cutoff-independent covariant
averages; a nonfixed v satisfies the printed scalar point condition but
fails independence. This verifies the omitted U(h) condition in a finite
model, not the classification of distributions or transverse jets.
"""

from itertools import permutations, product

from sage.all import QQ, matrix, vector


def frozen(a):
    a.set_immutable()
    return a


G = tuple(frozen(matrix(QQ, 3, 3,
                       lambda i, j: int(i == p[j])))
          for p in permutations(range(3)))
identity = frozen(matrix.identity(QQ, 3))
swap = frozen(matrix(QQ, [[0, 1, 0], [1, 0, 0], [0, 0, 1]]))
H = (identity, swap)
basis = matrix(QQ, [[1, 0], [0, 1], [-1, -1]])
U = {g: basis.solve_right(g*basis) for g in G}
checks = 0
for a, b in product(G, repeat=2):
    assert U[a]*U[b] == U[frozen(a*b)]
    checks += 1

cosets = []
for g in G:
    coset = frozenset(frozen(h*g) for h in H)
    if coset not in cosets:
        cosets.append(coset)
assert len(cosets) == 3
x0 = next(i for i, c in enumerate(cosets) if identity in c)
sections = tuple(product(*(tuple(c) for c in cosets)))
assert len(sections) == 8
fixed, nonfixed = vector(QQ, [1, 1]), vector(QQ, [1, 0])
assert U[swap]*fixed == fixed
assert U[swap]*nonfixed != nonfixed
checks += 2


def average(section, test_index, v):
    # rho is one at the chosen section points and zero elsewhere.
    # Phi(g)=phi(Hg)*v; hence only one point contributes for each phi.
    g = section[test_index]
    return U[frozen(g.inverse())]*v


coefficients = []
for i in range(3):
    expected = average(sections[0], i, fixed)
    coefficients.append(expected)
    for section in sections:
        assert average(section, i, fixed) == expected
        checks += 1

for i, coset in enumerate(cosets):
    representative = next(iter(coset))
    for g in G:
        image = frozenset(frozen(h*representative*g) for h in H)
        j = cosets.index(image)
        assert coefficients[j] == U[frozen(g.inverse())]*coefficients[i]
        checks += 1

# The printed point condition is scalar invariance of delta_H, satisfied
# by every vector. The two admissible cutoffs at H expose its defect.
values = {tuple(average(section, x0, nonfixed)) for section in sections}
assert values == {(QQ(1), QQ(0)), (QQ(0), QQ(1))}
checks += 1
print(f'ok orbit_distribution_covariance: {checks} exact finite checks')
