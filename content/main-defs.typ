#import "numbering.typ": numbered-record, place-key, record-number
#let source(n, printed: none) = context [#metadata((
  kind: "source",
  file-page: n,
  printed-page: if printed == none { str(n) } else { printed },
  position: here().position(),
))]
#let number-text(body) = text(weight: "semibold", style: "normal", body)
#let examples-heading(body) = block(
  sticky: true,
  par(first-line-indent: (amount: 1.25em, all: true), strong(body)),
)
#let reference-rules(body) = {
  show ref: it => {
    let caption = it.supplement not in (auto, none, [])
    let result = context {
      let target = str(it.target)
      let prefix = target.split(":").first()
      let record = if (
        it.element != none
          and prefix not in ("def", "front", "bibliography", "proof")
      ) { numbered-record(it.target) }
      let number = if record != none { record-number(record) } else if (
        it.element != none
          and it.element.func() == figure
          and it.element.numbering != none
      ) { it.element.counter.at(it.element.location()) }
      let resolved = it.element != none
      let printed = if number == none {
        if record != none { none } else { "?" }
      } else {
        let own = number.last()
        if prefix == "eq" and record.value.at("tag", default: none) != none {
          str(own)
        } else if prefix == "sec" { str(number.first()) } else if (
          prefix == "ss"
        ) { number.map(str).join(".") } else if (
          prefix in ("pr", "th", "lem", "eq")
        ) {
          if number.slice(0, -1) == place-key(here()) { str(own) } else {
            number.map(str).join(".")
          }
        } else { str(own) }
      }
      let shown = if caption { it.supplement } else if (
        record != none and number == none
      ) { record.value.at("caption", default: [Утверждение]) } else if (
        prefix == "bib"
      ) {
        [\[#number-text(printed)\]]
      } else if (
        prefix == "eq"
      ) {
        [(#number-text(printed))]
      } else { number-text(printed) }
      let destination = if not resolved { none } else if record != none {
        record.location()
      } else { it.element.location() }
      if prefix == "bib" {
        metadata((kind: "bibliographic-mention", target: target))
      }
      metadata((
        kind: "cross-reference",
        target: target,
        resolved: resolved,
        printed: printed,
        position: here().position(),
        target-position: if resolved { destination.position() },
      ))
      if resolved { link(destination, shown) } else { shown }
    }
    if caption { result } else { box(result) }
  }
  body
}
#let idx(..path, target: none) = [#metadata((
  kind: "index-mark",
  path: path.pos(),
  target: target,
))<index-mark>]
#let native-targets(it) = {
  if it.func() == ref { (it.target,) } else if it.has("children") {
    it.children.map(native-targets).flatten()
  } else if it.has("body") { native-targets(it.body) } else { () }
}
#let notation(symbol, references: [], description: none, sort: "") = {
  [#metadata((
    kind: "notation-mark",
    symbol: symbol,
    targets: native-targets(references),
    description: description,
    sort: sort,
  ))<notation-mark>]
}
#let editorial-note-counter = counter("editorial-note")
#let ed-note(body) = {
  editorial-note-counter.step()
  context {
    footnote(numbering: _ => (
      "*"
        + str(
          editorial-note-counter.get().first(),
        )
        + ")"
    ))[#body~— _Прим. ред._]
    counter(footnote).update(n => n - 1)
  }
}
#let Ker = math.op("Ker")
#let Im = math.op("Im")
#let ker = math.op("ker")
#let im = math.op("im")
#let Cyc = math.class(
  "normal",
  text(font: "Libertinus Serif", weight: "bold")[Ц],
)
#let Hom = math.op("Hom")
#let End = math.op("End")
#let Aut = math.op("Aut")
#let tr = math.op("tr")
#let codim = math.op("codim")
#let Re = math.op("Re")
#let Im-part = math.op("Im")
#let supp = math.op("supp")
#let sign = math.op("sign")
#let diag = math.op("diag")
#let id = math.op("id")
#let tensor-projective = math.class("binary", math.hat(sym.times.o))
#let tensor-weak = math.class(
  "binary",
  math.attach(math.limits(sym.times.o, inline: true), b: sym.caron),
)

#let Mor = math.op("Mor")
#let card = math.op("card")
#let group-name(name) = math.class("normal", math.upright(name))
#let GL = group-name("GL")
#let SL = group-name("SL")
#let SO = group-name("SO")
#let SU = group-name("SU")
#let Sp = group-name("Sp")
#let background(body) = text(size: 0.9em, body)
