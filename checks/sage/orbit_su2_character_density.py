"""SU(2) character densities with explicit Haar and Lebesgue measures.

Passages: eq:orbit-fourier-distribution,
eq:orbit-character-formula, eq:orbit-character-universal-factor.
For X=i theta diag(1,-1), ad X has eigenvalues 0,+2i theta,-2i theta.
Set j=det(P(ad X))=(sin(theta)/theta)^2, dg=j dX. For the shifted integral
orbit of highest weight m, beta-hat=sin((m+1)theta)/theta, while the ordinary
character is sin((m+1)theta)/sin(theta). Thus the source functional I(phi)
on dX requires rho=j^(-1/2). The factor j^(+1/2) pertains to a function
formula and cannot replace rho without changing the measure convention.
Tests cover six highest weights and four angles, not arbitrary Lie groups.
The printed factor and a naive positive square root are both refuted.
The exponential-domain argument is specific to SU(2) as unit quaternions.
"""

from sage.all import *
from datetime import datetime,timezone
th=var('theta',domain='real')
ad=matrix(SR,[[0,-2*th,0],[2*th,0,0],[0,0,0]])
z=var('z')
assert (ad.charpoly()(z)-z*(z*z+4*th*th)).expand()==0
# Haar Jacobian for exp under the compatible Lebesgue normalization.
j=(sin(th)/th)**2
# Symplectic Fourier integral on the rho-shifted integral sphere: I_m.
checks=0
for m in range(6):
 for angle in [pi/6,pi/4,pi/3,pi/2]:
  a=angle
  chi=sum(cos((m-2*k)*a)+I*sin((m-2*k)*a) for k in range(m+1))
  chi=chi.simplify_full()
  orbital=sin((m+1)*a)/a
  haar_j=j.subs({th:a})
  rho=a/sin(a)
  assert (orbital/rho-chi*haar_j).simplify_full()==0
  checks+=1
# Source q=j fails even for the trivial representation (m=0).
a=pi/2;orbital=sin(a)/a;haar_j=(sin(a)/a)**2
wrong=(orbital/haar_j-haar_j).simplify_full()
assert wrong!=0
# q=+sqrt(j) gives the ordinary character as a function, but not its Haar density.
wrong_sqrt=(orbital/(sin(a)/a)-haar_j).simplify_full()
assert wrong_sqrt!=0
print(version());print(datetime.now(timezone.utc).isoformat())
print('ad eigenvalues: 0, +2 i theta, -2 i theta; determinant P(adX)=(sin(theta)/theta)^2')
print('Exact Haar-density checks:',checks,'(highest weights 0..5, four rational multiples of pi)')
print('Correct rho=theta/sin(theta)=det(P)^(-1/2), with source I(phi)=integral phi(expX) I_hat(X)dX.')
print('Source q=det(P) residual at theta=pi/2, m=0:',wrong)
print('q=det(P)^(+1/2) Haar-density residual:',wrong_sqrt)
print('Source |ad imaginary eigenvalues|<=pi gives theta<=pi/2, only Re(unit quaternion)>=0.')
print('The missing hemisphere is open and has half the Haar measure. Strict bound 2*pi gives theta<pi, covering SU(2) except -I.')
