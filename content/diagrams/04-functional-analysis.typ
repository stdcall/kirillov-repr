#import "@preview/fletcher:0.5.8": edge, node
#import "01-02-categories.typ": cd

#let equivalent-algebra-representations() = cd(
  cell-size: (18mm, 12mm),
  node((0, 0), $H_1$),
  node((1, 0), $H_1$),
  node((0, 1), $H_2$),
  node((1, 1), $H_2$),
  edge((0, 0), (1, 0), $phi_1 lr((x))$, "->"),
  edge((0, 1), (1, 1), $phi_2 lr((x))$, "->"),
  edge((0, 0), (0, 1), $tau$, "->", label-side: right),
  edge((1, 0), (1, 1), $tau$, "->", label-side: left),
)
