"""Exact rational enclosure of the cube averaging error after 30 steps."""
from sage.all import QQ
from sage.version import version

square = (QQ(35) / 2) / 2**60
lower = QQ(389) / 10**11
upper = QQ(390) / 10**11
assert lower**2 < square < upper**2
assert (QQ(4) / 1000)**2 > square
print('3.89e-9 < sqrt(17.5)/2^30 < 3.90e-9 (exact squared inequalities)')
print('SageMath ' + version)
