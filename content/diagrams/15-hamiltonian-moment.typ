#import "@preview/fletcher:0.5.8": diagram, edge, node

#let hamiltonian-moment-diagram() = {
  set text(bottom-edge: "bounds")
  stack(diagram(
    spacing: 0pt,
    cell-size: (12mm, 10mm),
    node-inset: 1mm,
    edge-stroke: 0.5pt,
    node((0, 1), $0$),
    node((1, 1), $RR$),
    node((2.7, 1), $C^infinity lr((M,RR))$),
    node((5, 1), $H_0 lr((M))$),
    node((6.3, 1), $0$),
    node((2.7, 2), $frak(g)$),
    node((5, 0), $0$),
    node((5, 2), $H(M)$),
    node((5, 3), $H^1(M,RR)$),
    node((5, 4), $0$),
    edge((0, 1), (1, 1), "->"),
    edge((1, 1), (2.7, 1), "->"),
    edge((2.7, 1), (5, 1), "->"),
    edge((5, 1), (6.3, 1), "->"),
    edge((2.7, 2), (2.7, 1), "->"),
    edge((2.7, 2), (5, 2), "->"),
    edge((5, 0), (5, 1), "->"),
    edge((5, 1), (5, 2), "->"),
    edge((5, 2), (5, 3), "->"),
    edge((5, 3), (5, 4), "->"),
  ))
}
