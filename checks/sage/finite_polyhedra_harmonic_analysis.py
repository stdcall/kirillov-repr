"""Exact finite checks for ss:cube-harmonic-analysis (printed pp.285-288).

Proper rotations are constructed as the 24 determinant-one signed
permutation matrices. Fixed points on faces, vertices, diagonals, inscribed
tetrahedra and the centre give all 25 printed intertwining numbers by
Burnside's formula. Averaging matrices are built from geometric adjacency.

For an octahedron, faces are sign triples and adjacent faces differ in one
sign. The Walsh monomial of degree d is multiplied by (3-2d)/3: each of
its d selected coordinates contributes -1, the other 3-d contribute +1.
This is a general argument for all eight Walsh basis vectors, independent
of diagonalizing a matrix. The printed spectrum 1,-1,0 is refuted beside
the corrected one. The dodecahedron calculation uses its dual icosahedron.

Scope is the stated finite polyhedra, not arbitrary harmonic analysis.
No assertions inspect the Typst source, its markup or rendered strings.
"""

from datetime import datetime, timezone
from itertools import combinations, permutations, product

from sage.all import QQ, PolynomialRing, graphs, matrix, prod, vector
from sage.version import version


rotations = []
for perm in permutations(range(3)):
    inversions = sum(perm[i] > perm[j] for i in range(3)
                     for j in range(i + 1, 3))
    for signs in product((-1, 1), repeat=3):
        if (-1)**inversions * prod(signs) == 1:
            rotations.append((perm, signs))
assert len(rotations) == 24


def act(rotation, point):
    perm, signs = rotation
    return tuple(signs[i] * point[perm[i]] for i in range(3))


def diagonal(point):
    return tuple(point[0] * value for value in point)


faces = [tuple(sign if j == i else 0 for j in range(3))
         for i in range(3) for sign in (-1, 1)]
vertices = list(product((-1, 1), repeat=3))
diagonals = sorted(set(diagonal(v) for v in vertices))
actions = [
    (faces, lambda g, p: act(g, p)),
    (vertices, lambda g, p: act(g, p)),
    (diagonals, lambda g, p: diagonal(act(g, p))),
    ((-1, 1), lambda g, parity: prod(g[1]) * parity),
    (((0, 0, 0),), lambda g, p: act(g, p)),
]
assert [len(points) for points, _ in actions] == [6, 8, 4, 2, 1]
fixed = [[sum(action(g, p) == p for p in points)
          for g in rotations] for points, action in actions]
printed_intertwiners = [
    [3, 2, 1, 1, 1],
    [2, 4, 2, 2, 1],
    [1, 2, 2, 1, 1],
    [1, 2, 1, 2, 1],
    [1, 1, 1, 1, 1],
]
checks = 0
for i in range(5):
    for j in range(5):
        assert QQ(sum(a*b for a, b in zip(fixed[i], fixed[j]))) / 24 == (
            printed_intertwiners[i][j])
        checks += 1

ring = PolynomialRing(QQ, 'x')
x = ring.gen()
cube_faces = matrix(QQ, 6, 6, lambda i, j: QQ(1)/4
                    if sum(a*b for a, b in zip(faces[i], faces[j])) == 0
                    else 0)
assert cube_faces.charpoly() == (x - 1) * (x + QQ(1)/2)**2 * x**3
checks += 1

octahedron_faces = matrix(QQ, 8, 8, lambda i, j: QQ(1)/3
                         if sum(a != b for a, b in
                                zip(vertices[i], vertices[j])) == 1 else 0)
assert octahedron_faces.charpoly() == (
    (x - 1) * (x + 1) * (x - QQ(1)/3)**3 * (x + QQ(1)/3)**3)
checks += 1
for degree in range(4):
    for selected in combinations(range(3), degree):
        walsh = vector(QQ, [prod(v[i] for i in selected) for v in vertices])
        assert octahedron_faces * walsh == QQ(3 - 2*degree)/3 * walsh
        checks += 1
# Printed zero is not even an eigenvalue; the two missing values occur.
assert octahedron_faces.det() != 0
checks += 1

dodecahedron_faces = graphs.IcosahedralGraph().adjacency_matrix() / QQ(5)
assert dodecahedron_faces.charpoly() == (
    (x - 1) * (x + QQ(1)/5)**5 * (x*x - QQ(1)/5)**3)
checks += 1

print(f'ok finite_polyhedra_harmonic_analysis: {checks} exact checks')
print('SageMath ' + version)
print('UTC ' + datetime.now(timezone.utc).isoformat())
