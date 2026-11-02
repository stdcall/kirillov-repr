#import "@preview/cetz:0.5.2"
#import "@preview/fletcher:0.5.8": edge, node
#import "01-02-categories.typ": cd

#let bundle-morphism() = cd(
  cell-size: (11mm, 10mm),
  node((0, 0), $E_1$),
  node((2, 0), $E_2$),
  node((1, 1), $M$),
  edge((0, 0), (2, 0), $phi$, "->"),
  edge((0, 0), (1, 1), $p_1$, "->", label-side: right),
  edge((2, 0), (1, 1), $p_2$, "->", label-side: left),
)

// Two rectangular charts close with one reversal of the transverse coordinate.
#let mobius-strip() = cetz.canvas(length: 8mm, {
  import cetz.draw: *
  set-style(stroke: 0.5pt, content: (padding: 1pt))
  let width = 0.15
  let length = 2.8
  for (offset, labels) in (
    (0, ($D$, $C$, $B$, $A$)),
    (3.8, ($B$, $A$, $C$, $D$)),
  ) {
    let corners = (
      (offset, width),
      (offset, -width),
      (offset + length, width),
      (offset + length, -width),
    )
    line(
      corners.at(0),
      corners.at(2),
      corners.at(3),
      corners.at(1),
      close: true,
    )
    for (i, point) in corners.enumerate() {
      content(point, labels.at(i), anchor: if calc.even(i) { "south" } else {
        "north"
      })
    }
  }
  let at(t, v) = {
    let radius = 1.45 + v * calc.cos(t / 2 - 45deg)
    (
      9 + radius * calc.cos(t),
      0.4 * radius * calc.sin(t) + 0.8 * v * calc.sin(t / 2 - 45deg),
    )
  }
  let n = 160
  let half-width = 0.24
  // Paint rear panels before front panels in the oblique projection.
  for indices in (range(int(n / 2)), range(int(n / 2), n)) {
    for i in indices {
      let a = i * 360deg / n
      let b = (i + 1) * 360deg / n
      line(
        at(a, -half-width),
        at(b, -half-width),
        at(b, half-width),
        at(a, half-width),
        close: true,
        fill: white,
        stroke: none,
      )
      line(at(a, -half-width), at(b, -half-width))
      line(at(a, half-width), at(b, half-width))
      if calc.rem(i, 3) == 0 {
        line(at(a, -half-width), at(a, half-width), stroke: 0.2pt)
      }
    }
  }
  for (t, v, label, anchor) in (
    (180deg, -half-width, $A$, "north"),
    (180deg, half-width, $B$, "south"),
    (0deg, -half-width, $C$, "south"),
    (0deg, half-width, $D$, "north"),
  ) {
    content(at(t, v), label, anchor: anchor)
  }
})
