"""Exact arithmetic of the principal-series dimensions in section 16.3.

The odd-q summands are printed on p. 294. In even characteristic the
q-2 nontrivial characters are paired by inversion, giving (q-2)/2
representations of degree q+1, beside the trivial and Steinberg modules.
These checks establish the resulting polynomial identity, not the
representation-theoretic classification or irreducibility assertions.
The two erroneous printed polynomials are retained as refuted checks.
"""

from sage.all import PolynomialRing, QQ

R = PolynomialRing(QQ, "q")
q = R.gen()
odd = (q - 3) / 2 * (q + 1)**2 + 1 + q**2 + 2 * ((q + 1) / 2)**2
even = (q - 2) / 2 * (q + 1)**2 + 1 + q**2
corrected = q * (q - 1) * (q + 3) / 2
printed_total = q * (q + 1) * (q + 3) / 2
printed_even = (q + 2) / 2 * (q + 1)**2 + 1 + q**2

assert odd == corrected
assert even == corrected
assert odd != printed_total
assert printed_even != even
# The smallest cases also exhibit the failure of the printed readings.
assert odd(3) == 18 and printed_total(3) == 36
assert even(2) == 5 and printed_even(2) == 23

print("ok sl2_principal_dimensions: 6 checks")
