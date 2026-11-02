#import "@preview/fletcher:0.5.8": diagram, edge, node

#let cd(..args) = {
  set text(bottom-edge: "bounds")
  stack(diagram(
    spacing: 0pt,
    node-shape: rect,
    node-inset: 1.2mm,
    edge-stroke: 0.5pt,
    label-size: 0.8em,
    label-sep: 0.25em,
    ..args,
  ))
}

#let cocone-morphism() = cd(
  cell-size: (12mm, 12mm),
  node((1, 0), $X_alpha$),
  node((0, 1), $Y$),
  node((2, 1), $Z$),
  edge((1, 0), (0, 1), $f_alpha$, "->", label-side: right),
  edge((1, 0), (2, 1), $g_alpha$, "->", label-side: left),
  edge((0, 1), (2, 1), $h$, "->"),
)

#let compatible-cocone() = cd(
  cell-size: (12mm, 12mm),
  node((0, 0), $X_alpha$),
  node((2, 0), $X_beta$),
  node((1, 1), $Y$),
  edge((0, 0), (2, 0), $f_(alpha beta)$, "->"),
  edge((0, 0), (1, 1), $f_alpha$, "->", label-side: right),
  edge((2, 0), (1, 1), $f_beta$, "->", label-side: left),
)

#let natural-transformation() = cd(
  cell-size: (28mm, 14mm),
  $F(X) & G(X) \ F(Y) & G(Y)$,
  edge((0, 0), "r", $phi(X)$, "->"),
  edge((0, 0), "d", $F(f)$, "->", label-side: right),
  edge((1, 0), "d", $G(f)$, "->", label-side: left),
  edge((0, 1), "r", $phi(Y)$, "->"),
)
