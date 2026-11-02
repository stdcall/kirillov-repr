"""Exact counterexample to symmetry of finite-dimensional Hom spaces."""
from sage.all import PolynomialRing, QQ, identity_matrix, matrix


def intertwining_dimension(source, target):
    rows = source[0].nrows()
    columns = target[0].nrows()
    variables = rows * columns
    equations = []
    for left, right in zip(source, target):
        for i in range(columns):
            for j in range(rows):
                coefficients = [QQ(0)] * variables
                for k in range(rows):
                    coefficients[i * rows + k] += left[k, j]
                for k in range(columns):
                    coefficients[k * rows + j] -= right[i, k]
                equations.append(coefficients)
    return variables - matrix(QQ, equations).rank()


I = identity_matrix(QQ, 3)
E12 = matrix(QQ, 3, 3)
E13 = matrix(QQ, 3, 3)
E12[0, 1] = 1
E13[0, 2] = 1
A, B = I + E12, I + E13
assert A.is_invertible() and B.is_invertible() and A * B == B * A

# The formula defines a representation of the additive group Z^2.
R = PolynomialRing(QQ, names=('m', 'n', 'p', 'q'))
m, n, p, q = R.gens()
T = lambda x, y: I.change_ring(R) + x * E12 + y * E13
assert T(m, n) * T(p, q) == T(m + p, n + q)

trivial = [matrix(QQ, [[1]]), matrix(QQ, [[1]])]
forward = intertwining_dimension([A, B], trivial)
backward = intertwining_dimension(trivial, [A, B])
assert (forward, backward) == (2, 1)
print('G = Z^2, T on Q^3, S trivial: dim Hom(T,S) = 2; dim Hom(S,T) = 1')
