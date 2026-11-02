#import "@preview/fletcher:0.5.8": edge
#import "01-02-categories.typ": cd

#let equivalent-extensions() = cd(
  cell-size: (13mm, 13mm),
  $1 & G_0 & G & G_1 & 1 \ 1 & G_0 & G' & G_1 & 1$,
  ..range(2)
    .map(row => range(4).map(col => edge((col, row), "r", "->")))
    .flatten(),
  edge((1, 0), "d", "="),
  edge((2, 0), "d", $epsilon$, "->", label-side: right),
  edge((3, 0), "d", "="),
)
