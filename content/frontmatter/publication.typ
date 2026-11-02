#import "../main-defs.typ": source

#let publication-page() = page(
  width: 145mm,
  height: 215mm,
  margin: 0pt,
  fill: white,
  header: none,
  footer: none,
  numbering: "1",
)[
  #set text(font: "Libertinus Serif", size: 10.5pt, fill: black)
  #set par(first-line-indent: 0pt, leading: 0.4em, spacing: 0.4em)
  #source(2)
  #place(top + left, dx: 6.8mm, dy: 6mm, block[
    517.2\
    К 43\
    УДК 517.5
  ])
  #place(top + left, dx: 38mm, dy: 51.5mm, block(width: 69mm)[
    #set par(first-line-indent: (amount: 1.25em, all: true), justify: true)
    *Элементы теории представлений.* А.~А.~Кириллов. Главная редакция
    физико-математической литературы издательства «Наука», М., 1978.

    #v(3mm)
    Книга написана на основе курса лекций и семинаров по теории представлений,
    которые автор вел в Московском государственном университете. Она
    представляет собой компактное изложение на современном уровне основ теории
    представлений.

    Книга рассчитана на студентов, аспирантов и научных работников в области
    математики и физики, интересующихся не только практическими применениями
    теории представлений, но и самой теорией.
  ])
  #place(bottom + left, dx: 7mm, dy: -7mm, text(size: 9pt)[
    К $frac("20203—043", "053(02)-78")$ 42-78
  ])
]
