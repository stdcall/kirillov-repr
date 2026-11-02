"""Affine-group Jacobian and the fixed-point character factor in 13.5.

Compute the conjugation Jacobian directly for ax+b and right cosets of the
dilation subgroup. On the branch a>1, compare the pushforward density and
the modular square-root factor symbolically, with an exact witness a=4.
This checks the density convention, not the general kernel theorem.
"""
from sage.all import SR, matrix, var
from sage.env import SAGE_VERSION
from datetime import datetime, timezone
a,x=var('a x')
# G={(a,b):a>0}, (a,b)(c,d)=(ac,b+ad), H={(a,0)}.
# H\G coordinate x=b/a; s(x)=(1,x); dlG=da db/a^2, dlH=da/a.
# The conjugation map is (x,a) -> (a,(a-1)x).
conjugation=(SR(a),SR((a-1)*x))
jacobian=matrix([[v.derivative(t) for t in (a,x)] for v in conjugation]).det()
assert jacobian==a-1
# On a>1, absolute values may be removed.
density=(a**2/(a*(a-1))).simplify_full()
A=1/a
assert (density-1/(1-A)).simplify_full()==0
assert (a-1/A).simplify_full()==0
corrected=(density*a**(-SR(1)/2)).simplify_full()
expected=1/(A**(-SR(1)/2)-A**(SR(1)/2))
assert (corrected-expected).simplify_full()==0
assert density.subs(a=4)==SR(4)/3
assert (1-A).subs(a=4)==SR(3)/4
assert corrected.subs(a=4)==SR(2)/3
print({'sage':SAGE_VERSION,'utc':datetime.now(timezone.utc).isoformat(),
       'jacobian':str(jacobian),'pushforward_density':str(density),
       'modular_ratio_G_H':str(a),'det_A':str(A),
       'correct_character_coefficient':str(corrected),
       'at_a4':{'printed_density':'3/4','correct_density':'4/3',
                'printed_modular_rhs':'1/4','correct_modular_rhs':'4',
                'correct_character':'2/3'}})
