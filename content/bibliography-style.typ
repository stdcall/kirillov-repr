#import "bibliography-data.typ": bibliography-data

// The descriptions, including compound records, come only from BibLaTeX.
// userb preserves an abbreviation printed in this edition when its official
// shortjournal form has not been independently confirmed.
#let bib-text(value) = {
  let value = value.replace("--", "–")
  let position = 0
  for match in value.matches(
    regex(
      "\\$[^$]+\\$|[A-Za-z]+[₀₁₂₃₄₅₆₇₈₉ₙ]+∞?",
    ),
  ) {
    value.slice(position, match.start)
    if match.text.starts-with("$") {
      eval(match.text, mode: "markup")
    } else {
      let parts = match.text.match(regex("^([A-Za-z]+)([₀₁₂₃₄₅₆₇₈₉ₙ]+)(∞?)$"))
      let stem = parts.captures.at(0)
      let digits = "₀₁₂₃₄₅₆₇₈₉ₙ".clusters()
      let shown = "0123456789n".clusters()
      let sub = parts
        .captures
        .at(1)
        .clusters()
        .map(c => (
          shown.at(digits.position(d => d == c))
        ))
        .join()
      let base = if stem.len() == 1 { stem } else { "\"" + stem + "\"" }
      let sup = if parts.captures.at(2) == "∞" { "^infinity" } else { "" }
      eval("$" + base + "_" + sub + sup + "$", mode: "markup")
    }
    position = match.end
  }
  value.slice(position)
}
#let bib-backlinks(target) = context {
  let mentions = query(metadata.where(value: (
    kind: "bibliographic-mention",
    target: target,
  )))
  let seen = ()
  let pages = ()
  for mention in mentions {
    let loc = mention.location()
    if not seen.contains(loc.page()) {
      seen.push(loc.page())
      let position = loc.position()
      let destination = (
        page: position.page,
        x: position.x,
        y: calc.max(0pt, position.y - 8pt),
      )
      let pattern = loc.page-numbering()
      let folio = counter(page).at(loc)
      let shown = if pattern == none { str(folio.first()) } else {
        numbering(pattern, ..folio)
      }
      pages.push(box(context [
        #metadata((
          kind: "page-reference",
          resolved: true,
          target: "bib-mention:" + target,
          position: here().position(),
          target-position: position,
          destination-offset-pt: 18,
          description: shown,
        ))
        #link(destination, shown)
      ]))
    }
  }
  if pages.len() > 0 { [~#text(size: 9pt)[\[#pages.join(", ")\]]] }
}
#let bib-description(key) = {
  let entry = bibliography-data.at(key)
  let position = 0
  for match in entry.annotation.matches(regex("\\{([^{}]+)\\}")) {
    bib-text(entry.annotation.slice(position, match.start))
    let token = match.captures.first().split(".")
    let data = if token.len() == 1 { entry } else {
      assert(
        token.first() in entry.at("related", default: "").split(","),
        message: "Template references an unrelated bibliography record",
      )
      bibliography-data.at(token.first())
    }
    let field = token.last()
    if field.starts-with("ref:") {
      // Internal bibliography links remain clickable but never count as
      // mentions of the cited source in the reading text.
      context {
        let target = label("bib:" + field.slice(4))
        let found = query(target)
        if found.len() == 1 {
          let record = query(selector(<numbered>).within(target))
          let shown = if record.len() == 1 {
            str(record.first().value.number.last())
          } else { "?" }
          link(found.first().location(), shown)
        } else { "?" }
      }
    } else if field == "journal" {
      bib-text(data.at("shortjournal", default: data.at(
        "userb",
        default: data.at("journal", default: ""),
      )))
      if "shortjournal" in data and "series" in data {
        [ #bib-text(data.series)]
      }
    } else if field == "author" {
      bib-text(data.author.split(" and ").join(", "))
    } else { bib-text(data.at(field)) }
    position = match.end
  }
  bib-text(entry.annotation.slice(position))
  let language = entry.at("language", default: none)
  if language in ("english", "french", "german") {
    let name = (english: "англ.", french: "фр.", german: "нем.").at(language)
    [ (На #name яз.)]
  }
  for component in (
    (key,) + entry.at("related", default: "").split(",").filter(k => k != "")
  ) {
    let record = bibliography-data.at(component)
    if "doi" in record {
      let part = if "userc" in record { " (" + record.userc + ")" } else { "" }
      [
        #link(
          "https://doi.org/" + record.doi,
          "DOI" + part + ": " + record.doi,
        )]
    }
  }
  bib-backlinks("bib:" + key)
}
