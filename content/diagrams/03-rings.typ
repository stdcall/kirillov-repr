#import "@preview/fletcher:0.5.8": edge, node
#import "01-02-categories.typ": cd

#let tensor-universal-diagram() = cd(
  cell-size: (17mm, 10mm),
  node((0, 1), $M_1 times dots times M_n$),
  node((2, 0), $M$),
  node((2, 2), $M'$),
  edge((0, 1), (2, 0), $phi$, "->", label-side: left),
  edge((0, 1), (2, 2), $phi'$, "->", label-side: right),
  edge((2, 0), (2, 2), $psi$, "->", label-side: right),
)
