"""Exact Lie brackets of the quadratic oscillator formulas (18.4, pp.315-316).

The source algebra has [p_j,q_k]=delta_jk. Its Lie representation sends
1 to t=i*lambda, so it is NOT an associative algebra representation.
Use the independent differential Weyl algebras over QQ and QQ(t).
Check all brackets in the degree-at-most-two basis for n=1,2. The
symmetrized mixed monomial must map to x_j*d_k+delta_jk/2.
These are identities on polynomial vectors; analytic domains, essential
self-adjointness and integration to a unitary group are not established.
"""

from sage.all import (QQ, PolynomialRing, DifferentialWeylAlgebra,
                      QuadraticField)

K = PolynomialRing(QQ, "t").fraction_field()
t = K.gen()
checks = 0
for n in (1, 2):
    names = tuple(f"x{j}" for j in range(n))
    A = DifferentialWeylAlgebra(QQ, names)
    B = DifferentialWeylAlgebra(K, names)
    q = tuple(A.gens())[:n]
    p = tuple(A.gens())[n:]
    x = tuple(B.gens())[:n]
    d = tuple(B.gens())[n:]

    def image(a):
        result = B.zero()
        for (aa, bb), coefficient in a.monomial_coefficients().items():
            qs = [j for j in range(n) for _ in range(aa[j])]
            ps = [j for j in range(n) for _ in range(bb[j])]
            degree = len(qs)+len(ps)
            assert degree <= 2
            if degree == 0:
                term = t*B.one()
            elif degree == 1:
                term = t*x[qs[0]] if qs else d[ps[0]]
            elif not qs:
                term = d[ps[0]]*d[ps[1]]/t
            elif not ps:
                term = t*x[qs[0]]*x[qs[1]]
            else:
                i, j = qs[0], ps[0]
                term = x[i]*d[j] + (QQ(1)/2*(1-t) if i == j else 0)
            result += coefficient*term
        return result

    basis = ([A.one()]+list(p)+list(q)
             + [p[i]*p[j] for i in range(n) for j in range(i, n)]
             + [(q[i]*p[j]+p[j]*q[i])/2 for i in range(n) for j in range(n)]
             + [q[i]*q[j] for i in range(n) for j in range(i, n)])
    for a in basis:
        for b in basis:
            assert image(a*b-b*a) == image(a)*image(b)-image(b)*image(a)
            checks += 1
    for i in range(n):
        mixed = (q[i]*p[i]+p[i]*q[i])/2
        assert image(mixed) == x[i]*d[i]+QQ(1)/2
        assert image(mixed) != x[i]*d[i]  # Printed symmetric interpretation.
        assert image(q[i]*p[i]) != x[i]*d[i]  # Printed literal interpretation.
        checks += 3

F = QuadraticField(-1, "I")
I = F.gen()
W = DifferentialWeylAlgebra(F, ("z",))
z, dz = W.gens()
for lam in (1, -1):
    direct = (dz*dz/(I*lam) + I*lam*z*z)/2
    corrected = I*lam/2*(z*z-dz*dz)
    printed = -I*lam*(z*z+dz*dz)
    assert direct == corrected and direct != printed
    bargmann = (I/(2*lam)*(z+dz)**2-I*lam/2*(z-dz)**2)/2
    assert bargmann == I*lam*(z*dz+QQ(1)/2)
    checks += 2

print(f"ok oscillator_differential: {checks} exact operator identities; n=1,2")
