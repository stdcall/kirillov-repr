#import "../main-defs.typ": source

#let title-line(y, width, body, size: 34pt) = context {
  let letters = text(
    font: "Libertinus Serif",
    size: size,
    fill: black,
    top-edge: "cap-height",
    bottom-edge: "baseline",
    body,
  )
  place(top + center, dy: y, scale(
    x: width / measure(letters).width * 100%,
    reflow: true,
    letters,
  ))
}

#let title-page() = page(
  width: 145mm,
  height: 215mm,
  margin: 0pt,
  fill: white,
  header: none,
  footer: none,
  numbering: "1",
)[
  #set par(first-line-indent: 0pt, justify: false)
  #counter(page).update(1)
  #source(1)
  #title-line(7mm, 43mm, [А. А. КИРИЛЛОВ], size: 17pt)
  #title-line(40.5mm, 66mm, [ЭЛЕМЕНТЫ])
  #title-line(53.8mm, 47mm, [ТЕОРИИ])
  #title-line(67.1mm, 104mm, [ПРЕДСТАВЛЕНИЙ])
  #place(top + center, dy: 96mm, text(
    size: 9.5pt,
    weight: "bold",
  )[ИЗДАНИЕ ВТОРОЕ])
  #place(top + center, dy: 170.2mm, image(
    bytes(read("../../assets/nauka-emblem.svg").replace("#64451e", "#000000")),
    format: "svg",
    height: 14mm,
  ))
  #place(top + center, dy: 189.8mm, align(center)[
    #set text(size: 10.3pt, weight: "bold")
    МОСКВА «НАУКА»
  ])
  #place(top + center, dy: 195mm, align(center)[
    #set text(size: 10.3pt, weight: "bold")
    ГЛАВНАЯ РЕДАКЦИЯ
  ])
  #place(top + center, dy: 199.8mm, align(center)[
    #set text(size: 10.3pt, weight: "bold")
    ФИЗИКО-МАТЕМАТИЧЕСКОЙ ЛИТЕРАТУРЫ
  ])
  #place(top + center, dy: 205.3mm, text(size: 9pt)[1 9 7 8])
]
