#import "@preview/cetz:0.5.2"

// Reduced rank-two root systems, from their angular orbits and root lengths.
#let rank-two-root-systems() = cetz.canvas(length: 8mm, {
  import cetz.draw: *
  set-style(stroke: 0.5pt, line: (mark: (end: "stealth")))
  let root-orbits = (
    ((4, 0deg, 1),),
    ((6, 0deg, 1),),
    ((4, 0deg, 1), (4, 45deg, calc.sqrt(2))),
    ((6, 0deg, calc.sqrt(3)), (6, 30deg, 1)),
  )
  for (i, orbits) in root-orbits.enumerate() {
    let center = (i * 3.7, 0)
    for (order, angle, radius) in orbits {
      for k in range(order) {
        let t = angle + k * 360deg / order
        line(center, (
          center.at(0) + radius * calc.cos(t),
          radius * calc.sin(t),
        ))
      }
    }
  }
})

#let rank-two-dynkin-diagrams() = cetz.canvas(length: 8mm, {
  import cetz.draw: *
  set-style(stroke: 0.5pt, fill: white, content: (padding: 1pt))
  let radius = 0.11
  let span = 1.1
  for multiplicity in range(4) {
    let x = multiplicity * 3.7
    content((x + span / 2, 0.45), [#(multiplicity + 1)])
    if multiplicity > 0 {
      for k in range(multiplicity) {
        let offset = (k - (multiplicity - 1) / 2) * 0.08
        line((x, offset), (x + span, offset))
      }
    }
    if multiplicity > 1 {
      let end = x + span - radius
      line((end - 0.25, 0.16), (end, 0), (end - 0.25, -0.16))
    }
    circle((x, 0), radius: radius)
    circle((x + span, 0), radius: radius)
  }
})

#import "@preview/fletcher:0.5.8": edge, node
#import "01-02-categories.typ": cd

#let local-group-isomorphism() = cd(
  cell-size: (13mm, 12mm),
  node((0, 0), $V'_1 times V'_1$),
  node((2, 0), $upright(bold(R))^n supset V'_1$),
  node((0, 1), $V'_2 times V'_2$),
  node((2, 1), $upright(bold(R))^n supset V'_2$),
  edge((0, 0), (2, 0), $psi_1$, "->"),
  edge((0, 1), (2, 1), $psi_2$, "->"),
  edge((0, 0), (0, 1), $alpha times alpha$, "->", label-side: right),
  edge((2, 0), (2, 1), $alpha$, "->", label-side: left),
)

#let exponential-functoriality() = cd(
  cell-size: (18mm, 13mm),
  node((0, 0), $G_1$),
  node((1, 0), $G_2$),
  node((0, 1), $frak(g)_1$),
  node((1, 1), $frak(g)_2$),
  edge((0, 0), (1, 0), $phi$, "->"),
  edge((0, 1), (1, 1), $phi_* lr((e))$, "->"),
  edge((0, 1), (0, 0), $exp$, "->", label-side: left),
  edge((1, 1), (1, 0), $exp$, "->", label-side: right),
)
