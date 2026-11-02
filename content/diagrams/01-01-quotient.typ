#import "@preview/fletcher:0.5.8": diagram, edge, node

#let quotient-diagram() = {
  set text(bottom-edge: "bounds")
  stack(diagram(
    spacing: 0pt,
    cell-size: (12mm, 11mm),
    node-shape: rect,
    node-inset: 1.2mm,
    edge-stroke: 0.5pt,
    label-size: 0.8em,
    label-sep: 0.25em,
    node((0, 0), $X$),
    node((2, 0), $Y$),
    node((1, 1), $X_((R))$),
    edge((0, 0), (2, 0), $f$, "->"),
    edge((0, 0), (1, 1), $p$, "->", label-side: right),
    edge((1, 1), (2, 0), $g$, "->", label-side: right),
  ))
}
