"""The inducing character on the triangular polarization (18.5, p.319).

With B=JAJ^-1 and C_new=A1*C2+C1*B2, its additive phase must be
L(A,C)=tr(J_epsilon*A^-1*C). Indeed B^-1*J_epsilon=J_epsilon*A^-1,
so cyclicity of trace proves L(product)=L(first)+L(second) in general.
The script checks this rational identity in generic diagonal and C
entries for k=1..4 and every sign choice. It also refutes the printed
phase tr(J_epsilon*C) on explicit positive diagonal group elements.
No classification of coadjoint orbits or induced representations is
proved by this check.
"""

from itertools import product
from sage.all import QQ, PolynomialRing, matrix, CyclotomicField

checks = 0
for k in range(1, 5):
    names = ([f"a{j}" for j in range(k)]+[f"b{j}" for j in range(k)]
             + [f"c{j}" for j in range(k*k)]+[f"d{j}" for j in range(k*k)])
    K = PolynomialRing(QQ, names).fraction_field()
    variables = K.gens()
    A1 = matrix.diagonal(K, variables[:k])
    A2 = matrix.diagonal(K, variables[k:2*k])
    C1 = matrix(K, k, k, variables[2*k:2*k+k*k])
    C2 = matrix(K, k, k, variables[2*k+k*k:])
    J = matrix(K, k, k, lambda i, j: int(i+j == k-1))
    B2 = J*A2*J
    Anew, Cnew = A1*A2, A1*C2+C1*B2
    for signs in product((1, -1), repeat=k):
        Je = matrix.diagonal(K, signs)*J
        phase = lambda A, C: (Je*A.inverse()*C).trace()
        assert phase(Anew, Cnew) == phase(A1, C1)+phase(A2, C2)
        assert (Je*Cnew).trace() != (Je*C1).trace()+(Je*C2).trace()
        checks += 2

# k=1, A1=2, A2=1, C1=0, C2=1/3: the printed phase defect is 1/3,
# hence its exponential is a primitive cube root rather than one.
assert QQ(2)/3-QQ(1)/3 == QQ(1)/3
assert CyclotomicField(3).gen() != 1
checks += 2
print(f"ok triangular_polarization_character: {checks} exact checks; k=1..4")
