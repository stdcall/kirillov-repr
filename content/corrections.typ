#import "main-defs.typ" as book-defs
#show: book-defs.reference-rules
#let entries = json("../corrections.json").entries
#let markup(value) = eval(value, mode: "markup", scope: dictionary(book-defs))

#set document(
  title: "Кириллов. Элементы теории представлений. Исправления",
  author: "А. А. Кириллов",
  date: none,
)
#set page(
  width: 145mm,
  height: 215mm,
  margin: 16mm,
  numbering: "1",
  footer: context align(center, counter(page).display()),
)
#set text(font: "Libertinus Serif", size: 10.5pt, lang: "ru")
#set par(justify: true, leading: 0.65em, spacing: 0.8em)
#show math.equation: set text(font: "STIX Two Math")
#show heading: set text(size: 12pt)

#align(center, text(size: 15pt)[Исправления])

А.~А.~Кириллов. _Элементы теории представлений._ Второе издание. Москва,
«Наука», 1978. Номера страниц ниже относятся к этому изданию.

#if entries.len() == 0 [
  Исправлений нет.
] else {
  let section = none
  for entry in entries {
    if entry.section != section {
      section = entry.section
      heading(level: 1, numbering: none, section)
    }
    block(breakable: false, above: 1em)[
      #metadata((correction: entry.id))
      *#entry.id* · С.~#entry.printed_page, #markup(entry.place)

      Напечатано: #markup(entry.original)

      Исправлено: #markup(entry.corrected)

      #text(size: 9pt, markup(entry.reason))
    ]
  }
}
