#import "numbering.typ": restart-counters
#import "statements.typ": numbered-display
#import "main-defs.typ": reference-rules

#let part-counter = counter("part")
#let heading-number(it) = counter(heading).at(it.location())
#let heading-prefix(it) = {
  let n = heading-number(it)
  if it.level == 2 { [§ #n.at(1).] } else {
    [#n.at(1).#n.at(2).]
  }
}
#let book-style(body) = {
  set page(
    width: 145mm,
    height: 215mm,
    margin: (x: 16mm, top: 17mm, bottom: 17mm),
    header: counter(footnote).update(0),
    footer: context align(center, text(size: 9pt, counter(page).display())),
  )
  set text(font: "Libertinus Serif", size: 10.5pt, lang: "ru")
  set par(
    justify: true,
    first-line-indent: 1.25em,
    leading: 0.58em,
    spacing: 0.65em,
  )
  show link: set text(fill: black)
  show regex("^-\\p{L}"): it => sym.wj + it
  show regex("(?i)т\\. [еопдн]\\.|и\\. о\\.|н\\. э\\."): it => {
    it.text.replace(" ", "\u{00a0}")
  }
  set heading(
    numbering: (..n) => {
      let n = n.pos()
      if n.len() == 2 { "§ " + str(n.at(1)) + "." } else {
        str(n.at(1)) + "." + str(n.at(2)) + "."
      }
    },
    supplement: none,
  )
  show heading: it => {
    if it.level == 1 { pagebreak(weak: true) }
    if (
      it.level == 1 and it.has("label") and str(it.label).starts-with("part:")
    ) {
      part-counter.step()
      context [#metadata((
        kind: "numbered",
        family: "heading",
        level: 1,
        native: true,
        number: part-counter.get(),
      ))<numbered>]
    }
    if it.numbering != none {
      restart-counters(it.level)
      [#metadata((
        kind: "numbered",
        family: "heading",
        level: it.level,
      ))<numbered>]
    }
    set par(first-line-indent: 0pt, justify: false)
    let shown = if it.numbering != none {
      [#heading-prefix(it) #it.body]
    } else { it.body }
    block(
      width: 100%,
      sticky: true,
      above: if it.level == 1 { 8mm } else { 4mm },
      below: if it.level == 1 { 5mm } else { 3mm },
      {
        if it.level <= 2 {
          align(center, text(size: 12pt, weight: "regular", {
            if (
              it.level == 1
                and it.has("label")
                and str(it.label).starts-with("part:")
            ) {
              context {
                let ordinal = ("ПЕРВАЯ", "ВТОРАЯ", "ТРЕТЬЯ").at(
                  part-counter.get().first() - 1,
                )
                [ЧАСТЬ #ordinal]
              }
              linebreak()
            }
            shown
          }))
        } else { strong(shown) }
      },
    )
  }
  show outline: set par(first-line-indent: 0pt)
  show outline.entry: set block(breakable: false)
  show outline.entry: it => {
    set block(
      sticky: (
        it.level == 1
          and it.element.has("label")
          and str(it.element.label).starts-with("part:")
      ),
    )
    link(it.element.location(), it.indented(
      if it.element.numbering != none { heading-prefix(it.element) },
      it.inner(),
    ))
  }
  set math.equation(numbering: none, supplement: none)
  show math.equation.where(block: true): set block(
    above: 0.8em,
    below: 0.8em,
  )
  show math.equation: set text(font: "STIX Two Math")
  show math.equation.where(block: false): set text(
    top-edge: "bounds",
    bottom-edge: "bounds",
  )
  show math.equation: it => {
    show ":": math.class("punctuation", ":")
    show "≥": sym.gt.eq.slant
    show "≤": sym.lt.eq.slant
    it
  }
  show math.equation.where(block: true): it => {
    if it.has("label") and str(it.label).starts-with("eq:") {
      numbered-display(it)
    } else { it }
  }
  set math.cases(gap: 0.6em)
  set enum(numbering: "1)", indent: 1.25em)
  set table(stroke: 0.5pt, inset: 0.4em)
  show table: set par(first-line-indent: 0pt, justify: false)
  set footnote(numbering: n => str(n) + ")")
  set footnote.entry(indent: 1.5em)
  show footnote.entry: it => {
    context metadata((
      kind: "footnote-placement",
      anchor-page: it.note.location().page(),
      entry-page: it.location().page(),
    ))
    it
  }
  show: reference-rules
  body
}
