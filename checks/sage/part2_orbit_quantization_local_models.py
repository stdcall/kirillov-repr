"""Exact local obstructions and the half-density correction in section 15.4.

The curved positive polarization refutes a simultaneous flat normal form.
The operator calculation tests 64 polynomial commutator identities exactly.
The general symmetry argument is integration by parts; finite tests alone
do not establish that argument or analytic self-adjointness.
"""
from sage.all import QQ, PolynomialRing

R = PolynomialRing(QQ, names=("x", "y"))
x, y = R.gens()
K = R.fraction_field()
weight = 1 / (1 + x*x + y*y)**2
# Delta(log weight) = div(grad(weight)/weight).
lap_log = sum((weight.derivative(t) / weight).derivative(t)
              for t in (x, y))
assert lap_log == -8 / (1 + x*x + y*y)**2
# A holomorphic flattening would make log(weight)=log|w'|^2 harmonic.
assert lap_log != 0

S = PolynomialRing(QQ, names=("q", "p"))
q, p = S.gens()

def poisson(f, g):
    return f.derivative(p)*g.derivative(q)-f.derivative(q)*g.derivative(p)

def operator(f, u):
    a = f.derivative(p)
    b = f.subs(p=0)
    # The common imaginary scale is formal; compare its first-order part.
    return a*u.derivative(q)+a.derivative(q)*u/2, b*u

# For linear momentum symbols, Lie derivatives on half-densities represent
# vector fields. This is the first-order part of the commutator identity.
count = 0
for a in [S(1), q, q*q, q**3+1]:
    for b in [S(1), q, q*q+2, q**3-q]:
        bracket = a*b.derivative(q)-b*a.derivative(q)
        for u in [S(1), q, q*q, q**4+q]:
            def action(v, f):
                return v*f.derivative(q)+v.derivative(q)*f/2
            assert action(a, action(b, u))-action(b, action(a, u)) == action(bracket, u)
            assert poisson(a*p, b*p) == bracket*p
            count += 1
# Formal adjoint of a*d/dq equals -a*d/dq-a'; the half term repairs it.
assert (q*q).derivative(q) != 0
print(f"Curved positive model obstruction and {count} half-density brackets passed")
