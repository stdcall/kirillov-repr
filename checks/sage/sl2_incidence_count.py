"""Exhaustive incidence counts over F_2, F_3, F_4 and F_5 (16.3, p. 293).

Count the intermediate vectors directly, rather than composing a formula
from the book. This checks the coefficients of the stated product of two
incidence operators and exhibits the missing compatibility condition in
its hint. It is not a proof for every finite field; that follows because
the two linear equations have rank two or are dependent and consistent.
"""

from sage.all import GF

checks = 0
refuted = 0
for q in (2, 3, 4, 5):
    F = GF(q, "a")
    scalars = [s for s in F if s]
    vectors = [(a, b) for a in F for b in F if a or b]

    def determinant(x, y):
        return x[0] * y[1] - x[1] * y[0]

    for x in vectors:
        for y in vectors:
            for s1 in scalars:
                for s2 in scalars:
                    actual = sum(determinant(x, z) == s1 and
                                 determinant(z, y) == s2 for z in vectors)
                    lam = -s2 / s1
                    compatible = y == (lam * x[0], lam * x[1])
                    expected = 1 if determinant(x, y) else q * compatible
                    assert actual == expected
                    checks += 1
                    if not determinant(x, y) and not compatible:
                        assert actual == 0 and actual != q
                        refuted += 1

assert refuted > 0
print(f"ok sl2_incidence_count: {checks} counts; "
      f"{refuted} refute the printed unconditional q")
