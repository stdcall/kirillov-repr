#import "@preview/fletcher:0.5.8": diagram, edge, node

#let coassociativity-diagram() = {
  set text(bottom-edge: "bounds")
  stack(diagram(
    spacing: 0pt,
    cell-size: (19mm, 12mm),
    node-inset: 1mm,
    edge-stroke: 0.5pt,
    label-size: 0.8em,
    label-sep: 0.25em,
    node((0, 1), $L$),
    node((1, 0), $L ⊗_K L$),
    node((1, 2), $L ⊗_K L$),
    node((2, 1), $L ⊗_K L ⊗_K L$),
    edge((0, 1), (1, 0), $m$, "->"),
    edge((0, 1), (1, 2), $m$, "->", label-side: right),
    edge((1, 0), (2, 1), $m ⊗ 1$, "->"),
    edge((1, 2), (2, 1), $1 ⊗ m$, "->", label-side: right),
  ))
}
