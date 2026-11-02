"""Rodrigues values and Funk eigenvalue coefficients, 17.1, p. 301.

Differentiate the printed polynomial definition, and compare its values
with the closed formulas for degrees 0 through 32. The factor 2*pi is
cancelled, so all comparisons are in QQ. This verifies this finite range;
the general sign follows from the z^(2k) coefficient of (z^2-1)^(2k).
It does not prove the spherical harmonic decomposition or injectivity.
"""

from sage.all import PolynomialRing, QQ, factorial, binomial

R = PolynomialRing(QQ, "z")
z = R.gen()
checks = 0
for n in range(33):
    L = ((z**2 - 1)**n).derivative(n)
    assert L(1) == 2**n * factorial(n)
    checks += 1
    if n % 2:
        assert L(0) == 0
        checks += 1
    else:
        k = n // 2
        printed_zero = factorial(2*k) * binomial(2*k, k)
        assert L(0) == (-1)**k * printed_zero
        assert L(0) / L(1) == (-1)**k * QQ(binomial(2*k, k)) / 4**k
        checks += 2
        if k % 2:
            assert L(0) != printed_zero
            checks += 1

assert ((z**2 - 1)**2).derivative(2)(0) == -4
print(f"ok funk_legendre_eigenvalues: {checks + 1} checks, degrees 0..32")
