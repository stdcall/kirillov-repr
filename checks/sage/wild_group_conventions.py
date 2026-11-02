"""Matrix duality and Fourier kernel substitutions in section 19, pp.320-321.

Use Re tr(FX) for the displayed dual matrices. Complex conjugation acts
on coefficients of rational functions in REAL variables. Unit rotations
are parametrized by the Cayley formulas, avoiding floating trigonometry.
The identities extend to the omitted rotation by continuity. Independent
rotations give identities for a larger normalizer, hence for the subgroup
whose frequencies are 1 and alpha. Printed readings are refuted alongside
the corrected ones. These checks do not prove irreducibility, ergodicity
or the classification of type-I groups.
"""

from sage.all import QQ, QuadraticField, PolynomialRing, matrix

F0 = QuadraticField(-1, "I")
I = F0.gen()
names = ("alpha", "tau", "s", "t", "ar", "ai", "br", "bi",
         "zr", "zi", "wr", "wi", "xr", "xi", "yr", "yi", "r", "q")
R = PolynomialRing(F0, names)
K = R.fraction_field()
(alpha, tau, s, t, ar, ai, br, bi, zr, zi, wr, wi,
 xr, xi, yr, yi, r, q) = K.gens()

def conjugate_polynomial(p):
    return R({exponent: coefficient.conjugate()
              for exponent, coefficient in p.dict().items()})

def bar(value):
    value = K(value)
    return K(conjugate_polynomial(value.numerator())) / K(
        conjugate_polynomial(value.denominator()))

real = lambda value: (value+bar(value))/2
imag = lambda value: (value-bar(value))/(2*I)
a, b, z, w = ar+I*ai, br+I*bi, zr+I*zi, wr+I*wi
x, y = xr+I*xi, yr+I*yi
u, v = (1+I*r)/(1-I*r), (1+I*q)/(1-I*q)
assert u*bar(u) == 1 and v*bar(v) == 1

g = matrix(K, [[u, 0, z], [0, v, w], [0, 0, 1]])
ginv = matrix(K, [[1/u, 0, -z/u], [0, 1/v, -w/v], [0, 0, 1]])
functional = matrix(K, [[I*tau, 0, 0], [0, I*alpha*tau, 0], [a, b, 0]])
tangent = matrix(K, [[I*s, 0, x], [0, I*alpha*s, y], [0, 0, 0]])
direct = real((functional*ginv*tangent*g).trace())
new_tau = tau+imag(a*z/u+alpha*b*w/v)/(1+alpha**2)
corrected = matrix(K, [[I*new_tau, 0, 0],
                        [0, I*alpha*new_tau, 0], [a/u, b/v, 0]])
printed_tau = tau+imag(a*z+b*w)
printed = matrix(K, [[I*printed_tau, 0, 0],
                      [0, I*alpha*printed_tau, 0], [a/u, b/v, 0]])
assert direct == real((corrected*tangent).trace())
assert direct != real((printed*tangent).trace())

kernel = real(a*bar(x)+b*bar(y))
translated = real(a*bar(x-u*z)+b*bar(y-v*w))
first_phase = -real(a/u*bar(z)+b/v*bar(w))
printed_first = real(u*a*bar(z)+v*b*bar(w))
assert translated-kernel == first_phase
assert translated-kernel != printed_first

old_kernel = (t-tau)*s+real(a*bar(u*x-z)+b*bar(v*y-w))
new_kernel = t*s+real(a/u*bar(x)+b/v*bar(y))
second_phase = -tau*s-real(a*bar(z)+b*bar(w))
printed_second = (t*s+real(u*a*bar(x)+v*b*bar(y))+tau*s
                  + real(u*a*bar(z)+v*b*bar(w)))
assert old_kernel == new_kernel+second_phase
assert old_kernel != printed_second

print("ok wild_group_conventions: unit rotations, coadjoint pairing, "
      "two Fourier kernel identities and three printed refutations")
