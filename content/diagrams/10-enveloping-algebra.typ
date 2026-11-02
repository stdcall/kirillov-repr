#import "@preview/fletcher:0.5.8": diagram, edge, node

#let enveloping-morphism-diagram() = {
  set text(bottom-edge: "bounds")
  stack(diagram(
    spacing: 0pt,
    cell-size: (16mm, 11mm),
    node-inset: 1mm,
    edge-stroke: 0.5pt,
    label-size: 0.8em,
    label-sep: 0.25em,
    node((0, 1), $frak(g)$),
    node((1, 0), $A_1$),
    node((1, 2), $A_2$),
    edge((0, 1), (1, 0), $psi_1$, "->"),
    edge((0, 1), (1, 2), $psi_2$, "->", label-side: right),
    edge((1, 0), (1, 2), $alpha$, "->", label-side: left),
  ))
}
