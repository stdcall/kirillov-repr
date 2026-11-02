#let cover-paper = rgb("#c1a269")
#let cover-ink = rgb("#4e260d")
#let cover-rule = rgb("#73552c")

// Capitals are placed by their visible upper edge.
#let cover-line(y, width, body, cap: 7.3mm, tracking: 0pt) = {
  let letters = text(
    font: "Forum",
    size: cap / 0.69,
    fill: cover-ink,
    stroke: 0.11mm + cover-ink,
    tracking: tracking,
    top-edge: "cap-height",
    bottom-edge: "baseline",
    body,
  )
  context {
    let natural = measure(letters).width
    place(top + center, dy: y, scale(
      x: width / natural * 100%,
      reflow: true,
      letters,
    ))
  }
}

#let cover() = [
  #page(
    width: 145mm,
    height: 215mm,
    margin: 0pt,
    fill: cover-paper,
    header: none,
    footer: none,
    numbering: none,
  )[
    #set par(first-line-indent: 0pt, justify: false)
    #counter(page).update(0)
    #cover-line(21.5mm, 66.5mm, [А. А. КИРИЛЛОВ], cap: 5.1mm, tracking: 1.7pt)
    #place(top + center, dy: 34.2mm, line(
      length: 113mm,
      stroke: 1.55mm + cover-rule,
    ))
    #cover-line(47.8mm, 57.5mm, [ЭЛЕМЕНТЫ])
    #cover-line(61.0mm, 44.0mm, [ТЕОРИИ])
    #cover-line(74.2mm, 89.0mm, [ПРЕДСТАВЛЕНИЙ])
    #place(top + center, dy: 92.6mm, line(
      length: 34mm,
      stroke: 1.55mm + cover-rule,
    ))
    #place(top + center, dy: 161.8mm, image(
      "../../assets/nauka-emblem.svg",
      height: 14.8mm,
    ))
  ]
  #pagebreak(weak: true)
]
