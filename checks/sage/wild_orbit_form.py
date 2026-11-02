"""The seven-dimensional matrix algebra and orbit form in section 19, p.322.

Check all basis brackets in the printed 6x6 realization. On the generic
orbit, use the right action F.g=K(g^(-1))F in coordinates (phi,psi,S,T).
The book uses normalized alternation (5.3): J_k(omega)=k!*omega is the
ordinary differential form. Thus the coordinate matrix below represents
J_2(B_Omega), and B_Omega(A*,B*)=F([A,B])/2. The algebraic B_F in 15.1
retains F([A,B]); only its conversion to the orbit differential form has
the half factor.
This determines the mixed term to be -R*dphi^dpsi, whereas the printed
positive sign gives 3R instead of R on (S*,T*). These exact symbolic
identities do not classify the orbit topology or prove non-type-I.
"""

from sage.all import QQ, QuadraticField, PolynomialRing, matrix, vector

names = ("X", "Y", "U", "V", "S", "T", "R")
brackets = {("S", "X"): ("Y", 1), ("S", "Y"): ("X", -1),
            ("T", "U"): ("V", 1), ("T", "V"): ("U", -1),
            ("S", "T"): ("R", 1)}

def bracket(a, b):
    if (a, b) in brackets:
        return brackets[a, b]
    if (b, a) in brackets:
        c, sign = brackets[b, a]
        return c, -sign
    return None, 0

K = QuadraticField(-1, "I")
I = K.gen()
matrices = {name: matrix(K, 6, 6) for name in names}
matrices["X"][0, 2] = 1
matrices["Y"][0, 2] = I
matrices["U"][1, 2] = 1
matrices["V"][1, 2] = I
matrices["S"][0, 0] = I
matrices["S"][3, 4] = 1
matrices["T"][1, 1] = I
matrices["T"][4, 5] = 1
matrices["R"][3, 5] = 1
real_rows = [[part for entry in matrices[name].list()
              for part in (entry.real(), entry.imag())] for name in names]
assert matrix(QQ, real_rows).rank() == 7
checks = 1
for a in names:
    for b in names:
        c, sign = bracket(a, b)
        expected = sign*matrices[c] if c else matrix(K, 6, 6)
        assert matrices[a]*matrices[b]-matrices[b]*matrices[a] == expected
        checks += 1

P = PolynomialRing(QQ, names)
x, y, u, v, s, t, r = P.gens()
values = dict(zip(names, P.gens()))
fields = {"X": vector(P, [0, 0, -y, 0]),
          "Y": vector(P, [0, 0, x, 0]),
          "U": vector(P, [0, 0, 0, -v]),
          "V": vector(P, [0, 0, 0, u]),
          "S": vector(P, [-1, 0, 0, r]),
          "T": vector(P, [0, -1, -r, 0]),
          "R": vector(P, [0, 0, 0, 0])}
omega = matrix(P, [[0, -r, 1, 0], [r, 0, 0, 1],
                   [-1, 0, 0, 0], [0, -1, 0, 0]])
printed = matrix(P, [[0, r, 1, 0], [-r, 0, 0, 1],
                     [-1, 0, 0, 0], [0, -1, 0, 0]])
for a in names:
    for b in names:
        c, sign = bracket(a, b)
        expected = sign*values[c] if c else P.zero()
        assert fields[a]*(omega/2)*fields[b] == expected/2
        checks += 1
assert fields["S"]*printed*fields["T"] == 3*r
assert fields["S"]*printed*fields["T"] != r
assert omega.det() == 1
checks += 3
print(f"ok wild_orbit_form: {checks} exact bracket and two-form checks")
