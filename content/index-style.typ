// Subject Index. Every entry comes from an `#idx(...)` mark placed in the text
// where the term is introduced, so the page numbers are those of this
// edition and follow any reflow. A mark's arguments are the entry as
// printed, split at its commas: "Мера, Винера" is
// `#idx("Мера", "Винера")`.
//
// Layout as in the book: an entry repeating the beginning of the one above
// replaces it by dashes, one per word ("— —, connected" under "algebraic
// group"); when only the first word is shared, only that word is dashed
// ("— of a Lie group" under "Action, affine").
#import "main-defs.typ": *

// Alphabetical by words; a parenthetical qualifier does not count, so
// "Base (of a root system)" precedes "Base, extended" as in the book. A
// Greek letter before a hyphen does not count either: "α-string" and
// "ξ-string" stand under "string", "π-system" under "system", as printed.
#let sort-key(path) = {
  let key = lower(path.join(" ")).replace("ё", "е")
  key = key.replace(regex("\s*\([^)]*\)"), "")
  key = key.replace(regex("[,’'.]"), "")
  let greek = key.match(regex("^(\p{Greek})-"))
  if greek == none { key } else {
    key.slice(greek.end) + " " + greek.captures.first()
  }
}

#let dashes(text) = text.split(" ").map(_ => "—").join(" ")

// The printed form of `path` after `previous` (none at the start of a
// letter group).
#let printed(path, previous) = {
  if previous == none { return path.join(", ") }
  let parts = ()
  let shared = true
  for (i, part) in path.enumerate() {
    if shared and i < previous.len() and previous.at(i) == part {
      parts.push(dashes(part))
    } else if (
      shared
        and i < previous.len()
        and part.split(" ").first() == previous.at(i).split(" ").first()
    ) {
      let words = part.split(" ")
      parts.push(("—", ..words.slice(1)).join(" "))
      shared = false
    } else {
      parts.push(part)
      shared = false
    }
  }
  parts.join(", ")
}

// Each locator has its own context: `here()` inside the index's common
// context would give the start of the index, not the place of this number.
#let locator(location) = box(context {
  metadata((
    kind: "cross-reference",
    target: "index-mark",
    resolved: true,
    position: here().position(),
    target-position: location.position(),
  ))
  link(location, str(counter(page).at(location).first()))
})

#let index-entries = context {
  // Only the marks, by their label: querying all metadata would include
  // the locators this index itself adds, and the layout would not settle.
  let marks = query(<index-mark>)
  // Collect the marks of each entry; one locator per page.
  let entries = (:)
  for mark in marks {
    let target = mark.value.at("target", default: none)
    let destination = if target == none { mark.location() } else {
      let found = query(target)
      if found.len() == 1 { found.first().location() } else { mark.location() }
    }
    let key = mark.value.path.join("\u{1f}")
    let record = entries.at(key, default: (path: mark.value.path, at: ()))
    let number = counter(page).at(destination).first()
    if record.at.all(l => counter(page).at(l).first() != number) {
      record.at.push(destination)
    }
    entries.insert(key, record)
  }
  let sorted = entries.values().sorted(key: e => sort-key(e.path))
  let previous = none
  let initial = none
  for entry in sorted {
    let letter = upper(sort-key(entry.path).first())
    if letter != initial {
      if initial != none { v(0.8em, weak: true) }
      initial = letter
      previous = none
    }
    let shown = printed(entry.path, previous)
    // The first entry of a letter group begins with a capital; a Greek
    // letter keeps its case ("α-string").
    let letters = shown.clusters()
    if (
      previous == none and letters.first().match(regex("^[a-zа-яё]$")) != none
    ) {
      shown = upper(letters.first()) + letters.slice(1).join()
    }
    block(above: 0pt, below: 0.3em, par(hanging-indent: 1.2em)[
      #shown~#entry.at.map(locator).join([, ])
    ])
    previous = entry.path
  }
}

#let subject-index() = {
  source(339)
  heading(numbering: none)[Алфавитный указатель терминов]
  set par(first-line-indent: 0pt, justify: false, leading: 0.45em)
  set text(size: 10pt)
  columns(2, gutter: 8mm, index-entries)
}
