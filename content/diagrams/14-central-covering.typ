#import "@preview/fletcher:0.5.8": diagram, edge, node

#let central-covering-diagram() = {
  set text(bottom-edge: "bounds")
  stack(diagram(
    spacing: 0pt,
    cell-size: (13mm, 10mm),
    node-inset: 1mm,
    edge-stroke: 0.5pt,
    node((0, 0), $1$),
    node((1, 0), $tilde(G)$),
    node((2, 0), $tilde(G)_1$),
    node((3, 0), $RR$),
    node((4, 0), $1$),
    node((0, 1), $1$),
    node((1, 1), $G$),
    node((2, 1), $G_1$),
    node((3, 1), $TT$),
    node((4, 1), $1$),
    ..range(4)
      .map(i => (
        edge((i + 1, 0), (i, 0), "->"),
        edge((i + 1, 1), (i, 1), "->"),
      ))
      .flatten(),
    edge((0, 0), (0, 1), "="),
    edge((1, 0), (1, 1), "->"),
    edge((2, 0), (2, 1), "->"),
    edge((3, 0), (3, 1), "->"),
    edge((4, 0), (4, 1), "="),
  ))
}
