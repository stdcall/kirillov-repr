"""Exact finite checks for §§2.1, 2.3, 3.1–3.3 and 3.5.

Expected matrices/signs follow the formulas on printed pp.20–21,25,36–38,
40,42,44 of Kirillov, Elements of representation theory, 2nd ed.,1978.
Checks: quaternion and F4 matrix models; cyclic gcd/lcm, Hom and tensor
presentations for 1<=m,n<=12; decimal idempotents modulo 10**k, 1<=k<=8;
three real tensor-algebra models; small Clifford models and the volume
element signs underlying the three periodicity identities.

The printed 'least common divisor' at p.40 is retained below as a refuted
reading next to the corrected gcd. Finite ranges do NOT prove the general
classification, completion, tensor-product or periodicity theorems. In
particular this does not validate the infinite Hom(Q*,H) row on p.21.
All rings and ranks are exact. Clifford signs are checked directly in
explicit matrices; no QuadraticForm constructor convention is assumed.
"""

from itertools import product

from sage.all import GF, QQ, ZZ, NumberField, PolynomialRing, crt, gcd, lcm, matrix
from sage.version import version


checks = 0


def check(claim):
    global checks
    assert claim
    checks += 1


def flat(a):
    return list(a.list())


# Printed p.37, all sixteen signs in the real quaternion model.
def quaternion_matrix(a, b, c, d):
    return matrix(QQ, [[a, b, c, d], [-b, a, -d, c],
                       [-c, d, a, -b], [-d, -c, b, a]])


qb = [quaternion_matrix(*v) for v in matrix.identity(ZZ, 4).rows()]
one, qi, qj, qk = qb
check(matrix(QQ, [flat(a) for a in qb]).rank() == 4)
for a in (qi, qj, qk):
    check(a * a == -one)
for a, b, c in ((qi, qj, qk), (qj, qk, qi), (qk, qi, qj)):
    check(a * b == c)
    check(b * a == -c)

# Printed p.37, independent complex 2x2 model.
poly = PolynomialRing(QQ, 'z')
cc = NumberField(poly.gen()**2 + 1, 'ii')
ii = cc.gen()
cb = [matrix(cc, [[1, 0], [0, 1]]),
      matrix(cc, [[ii, 0], [0, -ii]]),
      matrix(cc, [[0, 1], [-1, 0]]),
      matrix(cc, [[0, ii], [ii, 0]])]
for a in cb[1:]:
    check(a * a == -cb[0])
check(cb[1] * cb[2] == cb[3])
check(matrix(cc, [flat(a) for a in cb]).rank() == 4)

# Printed p.38: four displayed matrices are closed and form F4.
f4 = [matrix(GF(2), a) for a in
      ([[1, 0], [0, 1]], [[1, 1], [1, 0]],
       [[0, 1], [1, 1]], [[0, 0], [0, 0]])]
for a, b in product(f4, repeat=2):
    check(a + b in f4)
    check(a * b in f4)
    check(a * b == b * a)
for a in f4[:3]:
    check(a.det() != 0)
check(f4[1]**2 == f4[2])
check(f4[1]**3 == f4[0])

# Printed pp.21,25,40. Smith presentations rather than floating ranks.
for m, n in product(range(1, 13), repeat=2):
    d, big = gcd(m, n), lcm(m, n)
    smith = matrix(ZZ, [[m, 0], [0, n]]).smith_form()[0]
    check([abs(smith[i, i]) for i in range(2)] == [d, big])
    # Hom(Z/n,Z/m): image of 1 may be exactly an element killed by n.
    check(sum(1 for x in range(m) if (n * x) % m == 0) == d)
    # Tensor has one generator with the two relations m*t=n*t=0.
    check(abs(matrix(ZZ, [[m, n]]).smith_form()[0][0, 0]) == d)
printed_least_common_positive_divisor = 1
check(gcd(2, 4) != printed_least_common_positive_divisor)
check(abs(matrix(ZZ, [[2, 4]]).smith_form()[0][0, 0]) == 2)

# Printed pp.36–37. CRT gives every idempotent, not a decimal sample search.
for k in range(1, 9):
    mod = 10**k
    residues = {ZZ(crt(a, b, 2**k, 5**k)) % mod
                for a, b in product((0, 1), repeat=2)}
    check(len(residues) == 4)
    for a in residues:
        check((a * a - a) % mod == 0)
        for power in range(1, 7):
            check(pow(int(a), power, mod) == a)
    if k == 7:
        check(residues == {0, 1, 2890625, 7109376})

# Printed p.42: H tensor H -> Mat4(QQ), using a*x*conjugate(b).
# Coefficients are read from the already checked quaternion matrix basis.
qflat = matrix(QQ, [flat(a) for a in qb]).transpose()


def qcoeff(a):
    return qflat.solve_right(matrix(QQ, 16, 1, flat(a))).column(0)


left = [matrix(QQ, [qcoeff(a * x) for x in qb]).transpose() for a in qb]
right = [matrix(QQ, [qcoeff(x * (b if j == 0 else -b)) for x in qb])
         .transpose() for j, b in enumerate(qb)]
for a, b in product(left, right):
    check(a * b == b * a)
check(matrix(QQ, [flat(a * b) for a, b in product(left, right)]).rank() == 16)
# C tensor H -> Mat2(C): cb spans over C (rank checked above).
# C tensor C -> C+C, z tensor w |-> (z*w, conjugate(z)*w).
check(matrix(QQ, [[1, 0, 1, 0], [0, 1, 0, 1],
                  [0, 1, 0, -1], [-1, 0, 1, 0]]).rank() == 4)

# Printed p.44: e_i^2=+1 for a positive square of Q, -1 for a negative.
e = matrix(QQ, [[1, 0], [0, -1]])
fplus = matrix(QQ, [[0, 1], [1, 0]])
fminus = matrix(QQ, [[0, 1], [-1, 0]])
for a, b, signs in ((e, fplus, (1, 1)), (e, fminus, (1, -1)),
                    (qi, qj, (-1, -1))):
    identity = matrix.identity(QQ, a.nrows())
    check(a * a == signs[0] * identity)
    check(b * b == signs[1] * identity)
    check(a * b == -b * a)
    check(matrix(QQ, [flat(x) for x in (identity, a, b, a * b)]).rank() == 4)
    volume = a * b
    # (e1e2)^2=-sign1*sign2: the p/q swap in the last two identities.
    check(volume**2 == -signs[0] * signs[1] * identity)
    check(a * volume == -volume * a)
    check(b * volume == -volume * b)
check(matrix(QQ, [[1, 1], [1, -1]]).rank() == 2)  # C(1,0,0)=R+R
check(fminus**2 == -matrix.identity(QQ, 2))         # C(0,1,0)=C

print(f'ok part1_exact: {checks} checks')
print('SageMath ' + version)
