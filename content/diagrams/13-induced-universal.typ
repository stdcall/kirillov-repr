#import "@preview/fletcher:0.5.8": diagram, edge, node

#let induced-universal-morphism() = {
  set text(bottom-edge: "bounds")
  stack(diagram(
    spacing: 0pt,
    cell-size: (17mm, 11mm),
    node-inset: 1mm,
    edge-stroke: 0.5pt,
    label-size: 0.8em,
    label-sep: 0.25em,
    node((0, 0), $V$),
    node((1, 0), $L$),
    node((1, 1), $L'$),
    edge((0, 0), (1, 0), $phi$, "->"),
    edge((0, 0), (1, 1), $phi'$, "->"),
    edge((1, 0), (1, 1), $epsilon$, "->", label-side: left),
  ))
}
