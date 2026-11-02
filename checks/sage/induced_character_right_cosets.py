r"""Exact finite-group check of the character formula for right cosets H\G.

Convention: matrices act on column vectors, and products are composed from
right to left. The induced space consists of functions F(hg)=U(h)F(g),
with [T(g)F](a)=F(ag). Choose a section s of the right cosets H\G and write
s(x)g=h(x,g)s(xg). The section model is
[T(g)f](x)=U(h(x,g))f(xg). Thus its diagonal block, when xg=x, is
U(s(x)g s(x)^(-1)); otherwise there is no diagonal block. Taking traces
proves the general formula with chi_U extended by zero outside H.

The printed formula instead uses s(x)^(-1)g s(x). The example below keeps
that reading and disproves it alongside the corrected formula. All six
elements of S3 are checked, for both characters of H=C2, over QQ. The
section is explicit and verified independently to meet every right coset
exactly once. The induced matrices come directly from the right action
and equivariance, rather than from either character formula.
"""

from datetime import datetime, timezone
from itertools import permutations

from sage.all import QQ, identity_matrix, matrix
from sage.env import SAGE_VERSION


def permutation_matrix(images):
    """Column j is the basis vector indexed by images[j]."""
    result = matrix(QQ, 3, 3, lambda i, j: int(i == images[j]))
    result.set_immutable()
    return result


def frozen(value):
    value.set_immutable()
    return value


G = tuple(permutation_matrix(p) for p in permutations(range(3)))
identity = identity_matrix(QQ, 3)
identity.set_immutable()
swap12 = permutation_matrix((1, 0, 2))
H = (identity, swap12)

# s(H)=1, s(H(23))=(23), s(H(132))=(132), in image notation.
section_images = ((0, 1, 2), (0, 2, 1), (2, 0, 1))
section = tuple(permutation_matrix(p) for p in section_images)
cosets = tuple(frozenset(frozen(h * s) for h in H) for s in section)
assert len(set(cosets)) == 3
assert set().union(*cosets) == set(G)
assert sum(len(coset) for coset in cosets) == len(G)


def induced_matrix(g, character):
    """Rows correspond to x, columns to xg, with multiplier U(h(x,g))."""
    result = matrix(QQ, 3, 3)
    for x, sx in enumerate(section):
        choices = [(y, sx * g * sy.inverse())
                   for y, sy in enumerate(section)
                   if sx * g * sy.inverse() in H]
        assert len(choices) == 1
        y, h = choices[0]
        result[x, y] = character(h)
    return result


print('SageMath', SAGE_VERSION)
print('UTC', datetime.now(timezone.utc).isoformat())
print('Right cosets H\\G; H={1,(12)}; section images:', section_images)
for name, character in [('trivial', lambda h: QQ(1)),
                        ('sign', lambda h: h.det())]:
    operators = {g: induced_matrix(g, character) for g in G}
    assert operators[identity] == identity_matrix(QQ, 3)
    assert all(operators[a] * operators[b] == operators[frozen(a * b)]
               for a in G for b in G)
    failures = []
    for g in G:
        corrected = sum(character(s * g * s.inverse())
                        for s in section if s * g * s.inverse() in H)
        printed = sum(character(s.inverse() * g * s)
                      for s in section if s.inverse() * g * s in H)
        direct = operators[g].trace()
        assert corrected == direct
        if printed != direct:
            failures.append((g, direct, printed))
    assert len(failures) == 2
    print(name, ': all 6 corrected characters agree with direct traces;')
    print('all 36 representation products agree; printed failures:')
    for g, direct, printed in failures:
        images = tuple(list(g.column(j)).index(1) for j in range(3))
        print('  g images=', images, 'direct/corrected=', direct,
              'printed=', printed)
        print(operators[g])
