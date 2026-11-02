#import "@preview/fletcher:0.5.8": diagram, edge, node

#let continuous-cohomology-diagram() = {
  set text(bottom-edge: "bounds")
  stack(diagram(
    spacing: 0pt,
    cell-size: (14mm, 15mm),
    node-inset: 1mm,
    edge-stroke: 0.5pt,
    label-size: 0.8em,
    label-sep: 0.25em,
    node((0, 0), $cal(F)^1$),
    node((1, 0), $dots$),
    node((2, 0), $cal(F)^k$),
    node((3.5, 0), $cal(F)^(k+1)$),
    node((5.2, 0), $cal(F)^(k+2)$),
    node((6.5, 0), $dots$),
    node((0, 1), $C_c^0 lr((G, V))$),
    node((1, 1), $dots$),
    node((2, 1), $C_c^(k-1) lr((G, V))$),
    node((3.5, 1), $C_c^k lr((G, V))$),
    node((5.2, 1), $C_c^(k+1) lr((G, V))$),
    node((6.5, 1), $dots$),
    ..((0, 1), (1, 2), (2, 3.5), (3.5, 5.2), (5.2, 6.5))
      .map(
        ((a, b)) => (
          edge((a, 0), (b, 0), "->"),
          edge((a, 1), (b, 1), "->"),
        ),
      )
      .flatten(),
    edge((0, 1), (0, 0), $i_1$, "->", label-side: right),
    edge((2, 1), (2, 0), $i_k$, "->", label-side: right),
    edge((3.5, 1), (3.5, 0), $i_(k+1)$, "->", label-side: right),
    edge((5.2, 1), (5.2, 0), $i_(k+2)$, "->", label-side: right),
  ))
}
