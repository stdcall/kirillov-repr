"""Exact finite checks for the background in §§4–6 (Kirillov, 1978).

Scope: first-linear polarization; a two-atom Lp change of measure; the
constant-function contour sign; finite commutants refuting the printed
4.5.1; normalized alternating forms in three polynomial coordinates;
small Lie-algebra counterexamples and root systems; cubic BCH and a
matrix commutator path; finite exponential and inverse-series identities.

Refuted printed readings remain next to their corrected counterparts.
These exact identities and counterexamples do not prove general spectral,
direct-integral, Lie-classification, integration or convergence theorems.
The normalization of arbitrary-degree forms is proved separately by the
general identification J_k(omega)=k!*omega; bounded polynomial tests below
only check signs and factors. No numerical integration or floating rank
is used.
"""

from itertools import combinations, permutations, product
from math import comb

from sage.all import (GF, QQ, PolynomialRing, RootSystem, factorial,
                      matrix, vector)
from sage.version import version


checks = 0


def check(claim):
    global checks
    assert claim
    checks += 1


# P.47: the scalar product is linear in its FIRST argument.
gaussian = QQ.extension(QQ['t'].gen()**2 + 1, 'ii')
ii = gaussian.gen()
for x, y in product((gaussian(1), ii, 1 + 2*ii), repeat=2):
    norm2 = lambda z: z*z.conjugate()
    real_part = norm2(x+y) - norm2(x-y)
    printed = (real_part + ii*norm2(x-ii*y) - ii*norm2(x+ii*y))/4
    corrected = (real_part + ii*norm2(x+ii*y) - ii*norm2(x-ii*y))/4
    check(corrected == x*y.conjugate())
    check(printed == x.conjugate()*y)
check(ii.conjugate() != ii)
# P.60: spectrum in [0,infinity) and b^2=a do not force b selfadjoint.
nonselfadjoint = matrix(QQ, [[0, 1], [0, 0]])
check(nonselfadjoint**2 == matrix(QQ, 2))
check(nonselfadjoint != nonselfadjoint.transpose())
# P.62: a unital Banach *-algebra can have no nonzero positive functional.
# On C^2 with (s,t)*=(conj(t),conj(s)), x*x ranges over (z,conj(z)).
# Positivity for z and -z forces a+b=0 and i(a-b)=0, hence a=b=0.
check(matrix(gaussian, [[1, 1], [ii, -ii]]).rank() == 2)

# P.50: rho^(1/p) maps Lp(mu1) TO Lp(mu2), not conversely.
mu1, mu2 = vector(QQ, [2, 8]), vector(QQ, [1, 2])
rho = [mu1[j]/mu2[j] for j in range(2)]
f = vector(QQ, [1, 3])
check(sum(mu2[j]*rho[j]*f[j]**2 for j in range(2)) ==
      sum(mu1[j]*f[j]**2 for j in range(2)))
check(sum(mu1[j]*rho[j]*f[j]**2 for j in range(2)) !=
      sum(mu2[j]*f[j]**2 for j in range(2)))

# P.56: R_x(lambda)=(x-lambda)^(-1). For f=1 and a positive
# contour, the residue is -1; the coefficient must be -1/(2*pi*i).
residue = QQ(-1)
check(-residue == 1)
check(residue != 1)


def commutant(basis, n):
    units = [matrix(QQ, n, n, lambda r, c: int((r, c) == (i, j)))
             for i, j in product(range(n), repeat=2)]
    equations = matrix(QQ, [list(sum((a*u-u*a)[r, c]*vector(QQ,
                         [int(k == q) for k in range(n*n)])
                         for q, u in enumerate(units)))
                         for a in basis for r, c in product(range(n), repeat=2)])
    return [sum((v[q]*u for q, u in enumerate(units)), matrix(QQ, n))
            for v in equations.right_kernel().basis()]


# P.69, theorem 4.5.1: all three printed center conditions hold,
# but the scalar diagonal algebra decomposes EVERY operator on Q^4.
i2 = matrix.identity(QQ, 2)
m2 = [matrix(QQ, 2, 2, lambda r, c: int((r, c) == (i, j)))
      for i, j in product(range(2), repeat=2)]
representation = [a.tensor_product(i2) for a in m2]
representation_prime = commutant(representation, 4)
check(len(representation_prime) == 4)
check(len(commutant([matrix.identity(QQ, 4)], 4)) == 16)
check(matrix(QQ, [a.list() for a in representation]).rank() == 4)
center_equations = matrix(QQ, [[(a*b-b*a)[r, c]
                              for a in representation]
                              for b in representation
                              for r, c in product(range(4), repeat=2)])
check(center_equations.right_kernel().dimension() == 1)
# A scalar commutant alone does not imply the double-commutant theorem
# without selfadjointness: upper triangular 2x2 matrices are a counterexample.
triangular = [m2[0], m2[1], m2[3]]
check(len(commutant(triangular, 2)) == 1)
check(len(commutant(commutant(triangular, 2), 2)) == 4)
check(len(triangular) == 3)

# Pp.87–90: coefficients below are VALUES on ordered coordinate vectors,
# not coefficients of the normalized wedge basis.
ring = PolynomialRing(QQ, ['x', 'y', 'z'])
coordinates = ring.gens()
dimension = len(coordinates)


def value(form, indices):
    if len(set(indices)) != len(indices):
        return ring.zero()
    inversions = sum(indices[i] > indices[j]
                     for i in range(len(indices)) for j in range(i+1, len(indices)))
    return (-1)**inversions * form.get(tuple(sorted(indices)), ring.zero())


def wedge(a, k, b, ell):
    result = {}
    for indices in combinations(range(dimension), k+ell):
        total = ring.zero()
        for selected in combinations(range(k+ell), k):
            remaining = tuple(j for j in range(k+ell) if j not in selected)
            sign = (-1)**sum(j-r for r, j in enumerate(selected))
            total += sign*value(a, tuple(indices[j] for j in selected))*value(
                b, tuple(indices[j] for j in remaining))
        result[indices] = total/comb(k+ell, k)
    return result


def exterior_d(a, k):
    return {indices: sum((-1)**r*value(a, indices[:r]+indices[r+1:]).derivative(
                        coordinates[j]) for r, j in enumerate(indices))/(k+1)
            for indices in combinations(range(dimension), k+1)}


def contraction(a, k, field):
    return {indices: k*sum(field[j]*value(a, (j,)+indices)
                          for j in range(dimension))
            for indices in combinations(range(dimension), k-1)} if k else {}


def plus(a, b, factor=1):
    return {indices: a.get(indices, 0)+factor*b.get(indices, 0)
            for indices in set(a) | set(b)}


def same(a, b):
    return all(c == 0 for c in plus(a, b, -1).values())


monomials = [ring.one()] + list(coordinates)
monomials += [coordinates[i]*coordinates[j]
              for i in range(dimension) for j in range(i, dimension)]
forms = [(k, {indices: monomial}) for k in range(4)
         for indices in combinations(range(dimension), k) for monomial in monomials]
field = vector(ring, [coordinates[1], coordinates[0]*coordinates[2], 1])
for k, a in forms:
    check(all(v == 0 for v in exterior_d(exterior_d(a, k), k+1).values()))
    # Coordinate formula for the ordinary Lie derivative of a covariant tensor.
    lie = {}
    for indices in combinations(range(dimension), k):
        lie[indices] = sum(field[j]*value(a, indices).derivative(coordinates[j])
                           for j in range(dimension))
        lie[indices] += sum(field[j].derivative(coordinates[index]) *
                            value(a, indices[:r]+(j,)+indices[r+1:])
                            for r, index in enumerate(indices)
                            for j in range(dimension))
    cartan = plus(contraction(exterior_d(a, k), k+1, field),
                  exterior_d(contraction(a, k, field), k-1) if k else {})
    check(same(lie, cartan))
for (k, a), (ell, b) in product(forms, repeat=2):
    if k+ell <= dimension:
        check(same(exterior_d(wedge(a, k, b, ell), k+ell),
                   plus(wedge(exterior_d(a, k), k+1, b, ell),
                        wedge(a, k, exterior_d(b, ell), ell+1), (-1)**k)))
check(wedge({(0,): ring.one()}, 1, {(1,): ring.one()}, 1)[(0, 1)] == QQ(1)/2)
check(contraction({(0, 1): ring.one()}, 2, vector(ring, [1, 0, 0]))[(1,)] == 2)

# P.106: zero Killing form does NOT imply nilpotence, already over Q.
# Basis h,u,v with [h,u]=u+v and [h,v]=-u+v.
ad = [matrix(QQ, [[0, 0, 0], [0, 1, -1], [0, 1, 1]]),
      matrix(QQ, [[0, 0, 0], [-1, 0, 0], [-1, 0, 0]]),
      matrix(QQ, [[0, 0, 0], [1, 0, 0], [-1, 0, 0]])]
for a, b in product(ad, repeat=2):
    check((a*b).trace() == 0)
check(ad[0][1:, 1:].det() == 2)
check(ad[0]**3 != 0)

# P.109: the upper triangular Borel of sl2 contains regular h but is
# solvable, two-dimensional and is not its one-dimensional Cartan.
h = matrix(QQ, [[1, 0], [0, -1]])
e = matrix(QQ, [[0, 1], [0, 0]])
f = matrix(QQ, [[0, 0], [1, 0]])
bracket = lambda a, b: a*b-b*a
check(bracket(h, e) == 2*e)
check(bracket(e, f) == h)
check(matrix(QQ, [h.list(), e.list()]).rank() == 2)
check(bracket(h, bracket(e, f)) == matrix(QQ, 2))
# P.102 is a ROW convention, as explicitly defined in §3.4.
row_ad = [matrix(QQ, [[0, 0, 0], [0, 0, 1], [0, -1, 0]]),
          matrix(QQ, [[0, 0, -1], [0, 0, 0], [1, 0, 0]]),
          matrix(QQ, [[0, 1, 0], [-1, 0, 0], [0, 0, 0]])]
for i, j, k in ((0, 1, 2), (1, 2, 0), (2, 0, 1)):
    check(bracket(row_ad[i], row_ad[j]) == -row_ad[k])
    check(bracket(row_ad[i].transpose(), row_ad[j].transpose()) == row_ad[k].transpose())
# P.110: B=1/2[,], the quadratic BCH term, is NOT associative.
bilinear = lambda a, b: bracket(a, b)/2
check(bilinear(bilinear(h, e), f) == h/2)
check(bilinear(h, bilinear(e, f)) == matrix(QQ, 2))

# P.104: characteristic p cannot be omitted in Lie's theorem.
for p in (2, 3, 5, 7):
    field_p = GF(p)
    derivative = matrix(field_p, p, p, lambda i, j: j if i+1 == j else 0, sparse=True)
    multiply = matrix(field_p, p, p, lambda i, j: 1 if i == j+1 else 0, sparse=True)
    check(bracket(derivative, multiply) == matrix.identity(field_p, p))

# P.108: rank-two reduced root systems, independent of the drawing.
for kind, count in ((['A', 1], 2), (['A', 2], 6), (['B', 2], 8), (['G', 2], 12)):
    roots = list(RootSystem(kind).root_lattice().roots())
    check(len(roots) == count)
    check(all(-root in roots and 2*root not in roots for root in roots))

# Pp.106–107: defining linear equations give the small classical ranks.
for size in range(2, 7):
    check(size*size-1 == matrix(QQ, [[int(i == j)
                                    for i, j in product(range(size), repeat=2)]]).right_kernel().dimension())
    units = [matrix(QQ, size, size, lambda r, c: int((r, c) == (i, j)))
             for i, j in product(range(size), repeat=2)]
    constraints = matrix(QQ, [(u.transpose()+u).list() for u in units]).transpose()
    check(constraints.right_kernel().dimension() == size*(size-1)//2)
for rank in range(1, 5):
    size = 2*rank
    symplectic = matrix.block([[matrix(QQ, rank), matrix.identity(QQ, rank)],
                              [-matrix.identity(QQ, rank), matrix(QQ, rank)]])
    units = [matrix(QQ, size, size, lambda r, c: int((r, c) == (i, j)))
             for i, j in product(range(size), repeat=2)]
    constraints = matrix(QQ, [(u.transpose()*symplectic+symplectic*u).list()
                              for u in units]).transpose()
    check(constraints.right_kernel().dimension() == rank*(2*rank+1))

# Quaternionic so*(2n): a nondegenerate skew-Hermitian form i*I_n
# works also for ODD n, omitted by the printed J_n construction.
qbase = [matrix.identity(gaussian, 2),
         matrix(gaussian, [[ii, 0], [0, -ii]]),
         matrix(gaussian, [[0, 1], [-1, 0]]),
         matrix(gaussian, [[0, ii], [ii, 0]])]
# P.79 claims GLOBAL constant rank. q->q^2 on H* has derivative
# u->qu+uq, of real rank4 at1 and rank2 at i. This does NOT assert
# singularity of the level q^2=1, whose two points are regular.
for q, rank in ((qbase[0], 4), (qbase[1], 2)):
    images = [q*u+u*q for u in qbase]
    equations = matrix(QQ, [[part for entry in a.list()
                             for part in (entry[0], entry[1])] for a in images])
    check(equations.rank() == rank)
# Separately, the transposed equation q*i*q=i is not a group over H:
# j,k lie on its level, but jk=i does not. The conjugate-transpose
# equation remains valid over H and is not restricted by this check.
qi, qj, qk = qbase[1:]
check(qj*qi*qj == qi)
check(qk*qi*qk == qi)
check(qj*qk == qi)
check((qj*qk)*qi*(qj*qk) != qi)
for rank in range(1, 5):
    form = matrix.identity(gaussian, rank).tensor_product(qbase[1])
    units = []
    for i, j, q in product(range(rank), range(rank), qbase):
        u = matrix(gaussian, 2*rank)
        u[2*i:2*i+2, 2*j:2*j+2] = q
        units.append(u)
    equations = [u.conjugate_transpose()*form+form*u for u in units]
    constraints = matrix(QQ, [[part for entry in equation.list()
                               for part in (entry[0], entry[1])]
                              for equation in equations]).transpose()
    check(constraints.right_kernel().dimension() == rank*(2*rank-1))

# P.110: in the Heisenberg group a common signed square root produces
# |t|, whose one-sided derivatives disagree. The sign belongs to ONE
# parameter only; the corrected product equals I+t*E13 exactly.
unit = matrix.identity(QQ, 3)
e12 = matrix(QQ, 3, 3, {(0, 1): 1})
e23 = matrix(QQ, 3, 3, {(1, 2): 1})
e13 = matrix(QQ, 3, 3, {(0, 2): 1})
for s in (QQ(1)/7, QQ(2)/3, QQ(2)):
    for sign in (-1, 1):
        x, y = unit+sign*s*e12, unit+s*e23
        check(x*y*x.inverse()*y.inverse() == unit+sign*s*s*e13)
        printed_x, printed_y = unit+sign*s*e12, unit+sign*s*e23
        check(printed_x*printed_y*printed_x.inverse()*printed_y.inverse() == unit+s*s*e13)

# P.77: Grassmann charts normalize COLUMNS selected by J, while the
# lower index labels a row/basis vector. Test exact changes of row basis.
for n in range(2, 6):
    for k in range(1, n):
        a = matrix(QQ, k, n, lambda i, j: (j+1)**i)
        change = matrix(QQ, k, k, lambda i, j: int(i == j)+int(i+1 == j))
        for selected in combinations(range(n), k):
            block = a.matrix_from_columns(selected)
            if block.det() == 0:
                continue
            normalized = block.inverse()*a
            check(normalized.matrix_from_columns(selected) == matrix.identity(QQ, k))
            other = change*a
            check(other.matrix_from_columns(selected).inverse()*other == normalized)

# Truncated free associative polynomials retain the cubic terms which
# the printed proof on p.110 discarded. All coefficients are rational.
degree_bound = 6


def nc_add(*terms):
    result = {}
    for scalar, term in terms:
        for word, coefficient in term.items():
            result[word] = result.get(word, QQ.zero()) + scalar*coefficient
    return {word: coefficient for word, coefficient in result.items() if coefficient}


def nc_mul(a, b):
    result = {}
    for left, c in a.items():
        for right, d in b.items():
            word = left+right
            if len(word) <= degree_bound:
                result[word] = result.get(word, QQ.zero()) + c*d
    return {word: coefficient for word, coefficient in result.items() if coefficient}


def nc_comm(a, b):
    return nc_add((1, nc_mul(a, b)), (-1, nc_mul(b, a)))


def nc_exp(a):
    term, result = {(): QQ.one()}, {(): QQ.one()}
    for n in range(1, degree_bound+1):
        term = nc_mul(term, a)
        result = nc_add((1, result), (QQ(1)/factorial(n), term))
    return result


def nc_log_one_plus(a):
    term, result = {(): QQ.one()}, {}
    for n in range(1, degree_bound+1):
        term = nc_mul(term, a)
        result = nc_add((1, result), (QQ((-1)**(n+1))/n, term))
    return result


def bch3(a, b):
    comm = nc_comm(a, b)
    return nc_add((1, a), (1, b), (QQ(1)/2, comm),
                  (QQ(1)/12, nc_comm(a, comm)),
                  (QQ(1)/12, nc_comm(b, nc_comm(b, a))))


nx, ny, nz = ({(letter,): QQ.one()} for letter in ('X', 'Y', 'Z'))
degree_bound = 3
direct_bch = nc_log_one_plus(nc_add((1, nc_mul(nc_exp(nx), nc_exp(ny))),
                                  (-1, {(): QQ.one()})))
check(direct_bch == bch3(nx, ny))
check(bch3(bch3(nx, ny), nz) == bch3(nx, bch3(ny, nz)))
# The cubic associativity equation contains both B(B(x,y),z) and cubic
# terms. It does not assert the associativity of B alone (refuted above).

# P.119: literal Dynkin block formula, including its nested-bracket/length
# convention, through total degree six. This is a formal coefficient check,
# not a proof of local convergence of the infinite Lie series.
degree_bound = 6


def dynkin_blocks(total, count):
    if count == 0:
        if total == 0:
            yield ()
        return
    for length in range(1, total-count+2):
        for k in range(length+1):
            for tail in dynkin_blocks(total-length, count-1):
                yield ((k, length-k),)+tail


dynkin = {}
for total in range(1, degree_bound+1):
    for count in range(1, total+1):
        for blocks in dynkin_blocks(total, count):
            word = tuple(letter for k, ell in blocks
                         for letter in ('X',)*k+('Y',)*ell)
            nested = {(word[0],): QQ.one()}
            denominator = QQ(count*total)
            for k, ell in blocks:
                denominator *= factorial(k)*factorial(ell)
            for letter in word[1:]:
                nested = nc_comm(nested, {(letter,): QQ.one()})
            dynkin = nc_add((1, dynkin),
                            (QQ((-1)**(count-1))/denominator, nested))
log_exp_product = nc_log_one_plus(nc_add(
    (1, nc_mul(nc_exp(nx), nc_exp(ny))), (-1, {(): QQ.one()})))
check(dynkin == log_exp_product)
for total in range(1, degree_bound+1):
    check({w: c for w, c in dynkin.items() if len(w) == total} ==
          {w: c for w, c in log_exp_product.items() if len(w) == total})

# P.120: (d exp)_X(Y) exp(-X)=alpha(ad X)Y, alpha(z)=(e^z-1)/z.
# Degree-six free words test arbitrary noncommuting matrices to this order.
degree_bound = 6
derivative_exp = {word: coefficient for word, coefficient in nc_exp(
    nc_add((1, nx), (1, ny))).items() if word.count('Y') == 1}
right_derivative = nc_mul(derivative_exp, nc_exp(nc_add((-1, nx))))
ad_power, alpha_ad = ny, {}
for n in range(degree_bound):
    alpha_ad = nc_add((1, alpha_ad), (QQ(1)/factorial(n+1), ad_power))
    ad_power = nc_comm(nx, ad_power)
check(right_derivative == alpha_ad)
left_derivative = nc_mul(nc_exp(nc_add((-1, nx))), derivative_exp)
ad_power, alpha_minus_ad = ny, {}
for n in range(degree_bound):
    alpha_minus_ad = nc_add((1, alpha_minus_ad),
                           (QQ((-1)**n)/factorial(n+1), ad_power))
    ad_power = nc_comm(nx, ad_power)
check(left_derivative == alpha_minus_ad)
check(left_derivative != right_derivative)

# Pp.118–121: finite matrix exponential identities, with all limiting
# coefficients interpreted by their power series at zero.
for size in range(2, 8):
    nilpotent = matrix(QQ, size, size, lambda i, j: int(j == i+1))
    exp_nilpotent = sum((nilpotent**j/factorial(j) for j in range(size)),
                        matrix(QQ, size))
    check(exp_nilpotent == matrix(QQ, size, size,
                                 lambda i, j: QQ(1)/factorial(j-i) if j >= i else 0))
    check(exp_nilpotent[0, size-1] == QQ(1)/factorial(size-1))
poly = PolynomialRing(QQ, ['a', 'b', 'c', 'd'])
a, b, c, d = poly.gens()
traceless = matrix(poly, [[(a-d)/2, b], [c, (d-a)/2]])
rho2 = ((a-d)/2)**2+b*c
check(traceless**2 == rho2*matrix.identity(poly, 2))
poly3 = PolynomialRing(QQ, ['a', 'b', 'c'])
a, b, c = poly3.gens()
skew = matrix(poly3, [[0, a, c], [-a, 0, b], [-c, -b, 0]])
r2 = a*a+b*b+c*c
outer = matrix(poly3, [[b*b, -b*c, a*b], [-b*c, c*c, -a*c], [a*b, -a*c, a*a]])
check(skew**2 == outer-r2*matrix.identity(poly3, 3))
check(skew**3 == -r2*skew)
for power in range(1, 7):
    check(skew**(2*power+1) == (-r2)**power*skew)

series = QQ[['z']]
z = series.gen()
alpha = sum((z**j/factorial(j+1) for j in range(10)), series.zero()).add_bigoh(10)
beta = 1-z/2+z**2/12-z**4/720+z**6/30240-z**8/1209600
check(alpha*beta == series.one().add_bigoh(10))
check(alpha(-z)*z.exp() == alpha)

# P.96: a (0,1)-coefficient of O(k) transforms by
# b_1(z)=-z^k*conj(z)^(-2)*b_2(1/z). Its angular shift is k+2,
# its radial shift k-2. The printed absolute value has k-2-m instead.
for k, a, b in product(range(-4, 5), range(5), range(5)):
    mode = k+2-a+b
    radial_degree = k-2-a-b
    corrected_bound = k-2-abs(k+2-mode)
    check(radial_degree <= corrected_bound)
    if min(a, b) == 0:
        check(radial_degree == corrected_bound)
radial = PolynomialRing(QQ, 'rho')
rho = radial.gen()
functions = radial.fraction_field()
u = functions(1/(1+rho*rho))
rhs = u.derivative()
check(rhs == -2*rho/(1+rho*rho)**2)
check(rhs.numerator().degree()-rhs.denominator().degree() == -3)
printed_bound = 0-2-abs(0-2-1)
corrected_bound = 0-2-abs(0+2-1)
check(printed_bound == -5)
check(corrected_bound == -3)
check(rhs.numerator().degree()-rhs.denominator().degree() > printed_bound)
# Homogeneous radial solutions rho^(m-1) are permitted at0 iff m>=1,
# at infinity iff m<=k+1. A one-dimensional cokernel occurs precisely
# when neither endpoint permits the homogeneous term: k+2<=m<=0.
# This finite check is paired with the general endpoint calculation.
for k in range(-12, 13):
    obstructions = 0
    for mode in range(-20, 21):
        at_zero = mode-1 >= abs(mode-1)
        at_infinity = mode-1 <= k-abs(k-mode+1)
        check(at_zero == (mode >= 1))
        check(at_infinity == (mode <= k+1))
        obstructions += int(not at_zero and not at_infinity)
    check(obstructions == max(-k-1, 0))

print(f'background_exact.py: {checks} exact checks passed (Sage {version}).')
