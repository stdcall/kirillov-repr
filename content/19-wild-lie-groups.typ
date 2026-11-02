#import "main-defs.typ": *
#import "statements.typ": *
#let Ind = math.op("Ind")

== Примеры диких групп Ли <sec:wild-lie-groups>

Простейший пример группы Ли, не принадлежащий типу I, можно построить следующим
образом. Пусть $alpha$ — иррациональное вещественное число. Рассмотрим группу
$G$ матриц вида
$
  mat(e^(i t), 0, z; 0, e^(i alpha t), w; 0, 0, 1), quad
  t in RR, quad z,w in CC.
$
<eq:wild-five-dimensional-group>

#source(320)
Ясно, что это — группа Ли. Как топологическое пространство, $G$ гомеоморфна
$RR^5$. Как группа она является полупрямым произведением одномерной подгруппы
$z=w=0$ и четырехмерного коммутативного нормального делителя $t=0$.

Рассмотрим $K$-представление этой группы. Отождествим пространство $frak(g)^*$
посредством спаривания $lr(⟨F,X⟩)=Re tr(F X)$ с пространством матриц вида
$
  mat(i tau, 0, 0; 0, i alpha tau, 0; a, b, 0), quad tau in RR, quad a,b in CC,
$
<eq:wild-coadjoint-functional>
Получаем следующий явный вид действия $G$ в $frak(g)^*$:
$
  K(t,z,w): (a,b,tau) mapsto
  (a_t,b_t,tau+frac(#Im-part (a_t z+alpha b_t w), 1+alpha^2)),
$
где $a_t=a e^(-i t)$, $b_t=b e^(-i alpha t)$. Таким образом, $G$-орбиты в
$frak(g)^*$ при $a!=0$, $b!=0$ — это двумерные цилиндры, образующей которых
является ось $tau$, а направляющей — кривая, заданная параметрическими
уравнениями
$
  a=a_0 e^(i t), quad b=b_0 e^(i alpha t), quad t in RR.
$ <eq:wild-dense-torus-curve>
Ясно, что эта кривая расположена всюду плотно на поверхности тора
$ abs(a)=abs(a_0), quad abs(b)=abs(b_0). $
Разбиение $frak(g)^*$ на $G$-орбиты не удовлетворяет условиям
п.~@ss:means-invariant-measures, а соответствующее фактор-пространство
$cal(O)(G)$ не является полуотделимым.

#problem[
  Докажите, что на группе $G$ есть двусторонне инвариантная мера, которая в
  параметрах $t$, $z=x+i y$, $w=u+i v$ имеет вид
  $ dif g=dif t dif x dif y dif u dif v. $
] <pr:wild-group-haar-measure>

Рассмотрим регулярное представление $T$ группы $G$. Оно действует в
$L^2(G,dif g)$ правыми сдвигами и в координатах $t$, $z$, $w$ может быть
записано формулой
$ lr([T(tau,xi,eta) f])(t,z,w)=f(t+tau,z+e^(i t) xi,w+e^(i alpha t) eta). $
<eq:wild-regular-representation>
Мы покажем сейчас, что это представление можно двумя различными способами
разложить на неприводимые компоненты.

*Первый способ.* Сделаем преобразование Фурье по переменным $z$ и $w$:
$
  tilde(f)(t,a,b)=integral integral integral integral f(t,z,w)
  e^(i Re(a overline(z)+b overline(w))) dif x dif y dif u dif v.
$
<eq:wild-first-fourier-transform>

#problem[
  Проверьте, что под действием преобразования Фурье представление $T$ переходит
  в представление $T_1$, задаваемое равенством
  $
    lr([T_1 (tau,xi,eta) tilde(f)])(t,a,b)
    =e^(-i Re(e^(-i t) a overline(xi)+e^(-i alpha t) b overline(eta)))
    tilde(f)(t+tau,a,b).
  $
  <eq:wild-first-transformed-representation>
] <pr:wild-first-fourier-representation>

#source(321)
Формула @eq:wild-first-transformed-representation показывает, что $T_1$ является
непрерывной суммой представлений $U_(a,b)$, $a,b in CC$, действующих в
$L^2(RR,dif t)$ по формуле
$
  lr([U_(a,b)(tau,xi,eta) phi])(t)
  =e^(-i Re(e^(-i t) a overline(xi)+e^(-i alpha t) b overline(eta))) phi(t+tau).
$
<eq:wild-line-representation>

#problem[Докажите, что все представления $U_(a,b)$ при $a!=0$, $b!=0$
  неприводимы.]
<pr:wild-line-irreducibility>

#hint[@pr:wild-line-irreducibility][
  Проверьте, что всякий оператор, перестановочный с операторами
  $U_(a,b)(0,xi,eta)$, является оператором умножения на функцию.
]

#problem[
  Докажите, что представления $U_(a,b)$ и $U_(a_1,b_1)$ эквивалентны тогда и
  только тогда, когда существует такое вещественное число $tau$, что
  $ a_1=a e^(i tau), quad b_1=b e^(i alpha tau). $
] <pr:wild-line-equivalence>

#hint[@pr:wild-line-equivalence][
  Проверьте, что сплетающий оператор для $U_(a_1,b_1)$ и $U_(a,b)$ может быть
  только оператором сдвига по $tau$.
]

*Второй способ.* Сделаем замену переменных:
$ f(t,z,w)=phi(t, e^(-i t) z, e^(-i alpha t) w) $
и перейдем к преобразованию Фурье:
$
  tilde(phi)(s,a,b)=integral integral integral integral integral phi(t, z, w)
  e^(i Re(t s+a overline(z)+b overline(w))) dif t dif x dif y dif u dif v.
$
<eq:wild-second-fourier-transform>

#problem[
  Проверьте, что после такого преобразования представление $T$ перейдет в
  представление $T_2$, задаваемое равенством:
  $
    lr([T_2 (tau,xi,eta) tilde(phi)])(s,a,b)
    =e^(-i Re(tau s+a overline(xi)+b overline(eta)))
    tilde(phi)(s,e^(-i tau) a,e^(-i alpha tau) b).
  $
  <eq:wild-second-transformed-representation>
] <pr:wild-second-fourier-representation>

#hint[@pr:wild-second-fourier-representation][
  Полезно рассмотреть отдельно преобразования $T_2 (0,xi,eta)$ и
  $T_2 (tau,0,0)$.
]

Пусть $X_(r,rho)$ — двумерная поверхность в $CC^2$, заданная уравнениями
$abs(a)=r$, $abs(b)=rho$, где $r$ и $rho$ — положительные вещественные числа.
Нулевые значения радиусов можно не учитывать в этом разложении, так как они
образуют множество меры нуль.

Представление $T_2$ естественно распадается в непрерывную сумму представлений
$V_(r,rho,s)$, действующих в $L^2(X_(r,rho))$ по формуле
$
  lr([V_(r,rho,s)(tau,xi,eta) phi])(a,b)
  =e^(-i Re(tau s+a overline(xi)+b overline(eta)))
  phi(e^(-i tau) a, e^(-i alpha tau) b).
$
<eq:wild-torus-representation>

#problem[Докажите, что представления $V_(r,rho,s)$ неприводимы при всех $r$,
  $rho$ и $s$.]
<pr:wild-torus-irreducibility>

#hint[@pr:wild-torus-irreducibility][
  Воспользуйтесь тем, что всякая измеримая функция на $X_(r,rho)$, инвариантная
  относительно $V_(r,rho,0)(tau,0,0)$, постоянна почти всюду.
]

#problem[
  Докажите, что представления $V_(r,rho,s)$ и $V_(r,rho,s')$ эквивалентны тогда
  и только тогда, когда разность $s-s'$ может быть записана в виде $m+alpha n$,
  $m,n in ZZ$.
] <pr:wild-torus-equivalence>

#hint[@pr:wild-torus-equivalence][
  Сплетающий оператор — это оператор умножения на функцию вида $a^m b^n$.
]

#problem[
  Докажите, что ни одно из представлений $U_(a,b)$ не эквивалентно ни одному из
  представлений $V_(r,rho,s)$.
] <pr:wild-decompositions-differ>

#hint[@pr:wild-decompositions-differ][
  Сравните оператор ограничения этих представлений на подгруппу $t=0$.
]

#source(322)
Таким образом, два построенные нами разложения существенно различны. Это
показывает, что группа $G$ не принадлежит типу I.

Более тонкий пример группы Ли не типа I, в котором не выполнено второе условие
критерия Костанта — Ауслендера (см. п.~@ss:orbit-representation-construction,
теорема @th:kostant-auslander-criterion), можно построить так.

Пусть $frak(g)$ — алгебра Ли размерности 7 над $RR$ с базисом $X$, $Y$, $U$,
$V$, $S$, $T$, $R$ и следующими ненулевыми коммутаторами:
$
  [S,X]=Y, quad [S,Y]=-X, quad\
  [T,U]=V, quad [T,V]=-U, quad [S,T]=R.
$
Эту алгебру можно реализовать клеточно-диагональными матрицами 6-го порядка, с
диагональными клетками
$
  mat(i s, 0, z; 0, i t, w; 0, 0, 0) quad "и" quad
  mat(0, s, r; 0, 0, t; 0, 0, 0),
$
где $z=x+i y$, $w=u+i v$ и $x$, $y$, $s$, $t$, $u$, $v$, $r$ — вещественные
параметры (координаты относительно базиса $X$, $Y$, $S$, $T$, $U$, $V$, $R$).
Пусть $G$ — связная односвязная группа Ли, соответствующая алгебре $frak(g)$.

#problem[
  Докажите, что орбиты $Omega$ максимальной размерности в $frak(g)^*$ при $R!=0$
  относительно $G$ топологически эквивалентны $bb(T)^2 times RR^2$ и что класс
  когомологий, определяемый канонической формой $B_Omega$, отличен от нуля.
] <pr:wild-orbit-nonexact-form>

#hint[@pr:wild-orbit-nonexact-form][
  Рассматривая $X$, $Y$, $S$, $T$, $U$, $V$, $R$ как линейные функции на
  $frak(g)^*$, докажите, что уравнения
  $ X^2+Y^2=r_1^2, quad U^2+V^2=r_2^2, quad R=r_3 $
  при $r_1!=0$, $r_2!=0$, $r_3!=0$ задают орбиту, и что на этой орбите
  $ B_Omega=dif phi and dif S+dif psi and dif T-R dif phi and dif psi, $
  где $phi$ и $psi$ — параметры на $Omega$, определяемые из равенств
  $X=r_1 cos phi$, $Y=r_1 sin phi$, $U=r_2 cos psi$, $V=r_2 sin psi$.
]

Тот факт, что группа $G$ не принадлежит типу I, можно установить следующим
образом. В $G$ имеется коммутативный нормальный делитель, алгебра Ли которого
натянута на векторы $X$, $Y$, $U$, $V$. Применяя к этому случаю рассуждения
пп.~@ss:group-extension-representations и @ss:projective-representations-basics,
легко показать, что изучение представлений группы $G$ можно свести к изучению
представлений группы $G_0$ матриц вида
$ mat(1, m, r; 0, 1, n; 0, 0, 1), quad m,n in ZZ, quad r in RR. $

#source(323)
#problem[Докажите, что группа $G_0$ не принадлежит типу I.]
<pr:discrete-heisenberg-not-type-one>

#hint[@pr:discrete-heisenberg-not-type-one][
  Пусть $H$ — подгруппа $G_0$, выделяемая условием $m=0$. Для любых вещественных
  $lambda$ и $phi$ определим характер $chi_(lambda,phi)$ группы $H$ равенством:
  $ chi_(lambda,phi)(n,r)=e^(i(lambda r+n phi)). $
  Докажите, что представления $T_(lambda,phi)=Ind(G_0, H, chi_(lambda,phi))$ при
  $lambda/(2pi) in.not QQ$ неприводимы и для таких $lambda$, $lambda_1$
  $T_(lambda,phi) tilde.op T_(lambda_1,phi_1)$ тогда и только тогда, когда
  $lambda=lambda_1$, а $phi-phi_1$ имеет вид $2 pi k+lambda l$, где $k$ и $l$ —
  целые числа.

  Выведите отсюда, что если $lambda$ несоизмеримо с $pi$, то классы
  эквивалентности представлений $T_(lambda,phi)$ и $T_(lambda,phi_1)$ не
  разделяются никаким открытым подмножеством в $hat(G)$.
]

Очень интересно было бы применить метод орбит к изучению представлений диких
групп Ли. Так, весьма правдоподобно, что роль орбит должны играть эргодические
$G$-инвариантные меры в $frak(g)^*$, а формула @eq:orbit-character-formula
выражает относительный след оператора представления в смысле фон Неймана.
Возможно также, что в терминах орбит можно описать разложение регулярного
представления на факторы и дать явную формулу для обобщенной меры Планшереля в
смысле И. Сигала (см. п.~@ss:generalized-plancherel)#footnote[См.
  @bib:Pukanszky1972.].
