#import "numbering.typ": (
  family-counter, formula-prime-marks, formula-primes, formula-tags,
  numbered-record, object-number, record, record-number,
)
#import "main-defs.typ": number-text
#let references-in(it) = {
  if it.func() == ref { (it.target,) } else if it.has("children") {
    it.children.map(references-in).flatten()
  } else if it.has("body") { references-in(it.body) } else { () }
}
#let numbered-display(it) = {
  let base = formula-primes.at(str(it.label), default: none)
  let prime = if base != none { str(base) }
  let prime-mark = formula-prime-marks.at(str(it.label), default: "′")
  let tag = formula-tags.at(str(it.label), default: none)
  if prime == none and tag == none { family-counter("eq").step() }
  context {
    record("eq", prime: prime, prime-mark: prime-mark, tag: tag)
    let shown = object-number(
      "eq",
      here(),
      prime: prime,
      prime-mark: prime-mark,
      tag: tag,
    ).last()
    math.equation(
      block: true,
      number-align: end + horizon,
      numbering: _ => text(font: "Libertinus Serif", style: "normal")[(#shown)],
      it.body,
    )
  }
}

// A numbered condition stated in words shares the formula counter.
#let numbered-condition(body) = {
  family-counter("eq").step()
  block(above: 0.8em, below: 0.8em, width: 100%, {
    set par(first-line-indent: 0pt)
    record("eq")
    grid(
      columns: (1fr, auto),
      column-gutter: 1em,
      align: (left, right + horizon),
      body, context [(#object-number("eq", here()).last())],
    )
  })
}
#let sequence = [].func()
#let join-pieces(pieces) = sequence(
  pieces
    .map(it => if it.func() == sequence and not it.has("label") {
      it.children
    } else { (it,) })
    .flatten(),
)
#let keep-label(original, rebuilt) = {
  if original.has("label") [#rebuilt#original.label] else { rebuilt }
}

// Put `head` at the start of the first paragraph of `body`.
#let prepend-heading(body, head) = {
  if body.func() == math.equation and body.block {
    (
      block(
        sticky: true,
        above: 0pt,
        below: 0pt,
        par(first-line-indent: (amount: 1.25em, all: true), head),
      )
        + body
    )
  } else if body.func() in (enum.item, list.item, enum, list, terms) {
    // A statement beginning with a list has a separate heading paragraph.
    // Native block stickiness keeps it with the first item across a page.
    block(sticky: true, above: 0pt, below: 0.58em, head) + body
  } else if body.func() == block {
    let fields = body.fields()
    let inner = fields.remove("body")
    block(prepend-heading(inner, head), ..fields)
  } else if body.func() == sequence and body.children.len() > 0 {
    let children = body.children
    let first-break = children.position(it => it.func() == parbreak)
    if first-break != none {
      let prefix = children.slice(0, first-break)
      let prose = prefix.filter(it => it.func() not in ([ ].func(), parbreak))
      if prose.len() > 0 {
        let last = prose.last()
        if last.func() == text and last.text.trim().ends-with(":") {
          // An introductory sentence ending in a colon belongs with the
          // formulation that follows, including a separate italic paragraph.
          return keep-label(body, join-pieces((
            block(sticky: true, spacing: auto, above: 0pt, par(
              first-line-indent: (amount: 1.25em, all: true),
              head + join-pieces(prefix),
            )),
            ..children.slice(first-break),
          )))
        }
      }
    }
    let display = children.position(it => (
      it.func() == math.equation and it.block
    ))
    if display != none {
      let prefix = children.slice(0, display)
      let prose-start = prefix.position(it => (
        it.func() not in ([ ].func(), parbreak)
      ))
      if prose-start != none {
        let paragraph = prefix.slice(prose-start)
        let breaks = paragraph.filter(it => it.func() == parbreak).len()
        let boundary = paragraph.position(it => it.func() == parbreak)
        let follows-break = (
          boundary == none
            or paragraph.slice(boundary + 1).all(it => it.func() == [ ].func())
        )
        let has-block = paragraph.any(it => (
          it.func() in (block, grid, table, figure, list, enum, terms)
        ))
        if breaks <= 1 and follows-break and not has-block {
          // Keep a statement's introductory paragraph with its display.
          // An explicit native paragraph preserves its indent and PDF tag.
          return keep-label(body, join-pieces((
            block(
              sticky: true,
              above: 0pt,
              below: 0pt,
              par(
                first-line-indent: (amount: 1.25em, all: true),
                head
                  + join-pieces(paragraph.filter(it => (
                    it.func() != parbreak
                  ))),
              ),
            ),
            ..children.slice(display),
          )))
        }
      }
    }
    let first = children.position(it => (
      it.func()
        not in (
          [ ].func(),
          parbreak,
        )
    ))
    if first == none { join-pieces((head, body)) } else {
      keep-label(body, join-pieces((
        ..children.slice(0, first),
        prepend-heading(children.at(first), head),
        ..children.slice(first + 1),
      )))
    }
  } else { head + body }
}

// Put `ending` after the last word or formula of `body`.
#let append-ending(body, ending) = {
  if body.func() == math.equation and body.block {
    // A display does not span the line by itself; widen it so that the mark
    // stands at the right margin on the display's last line.
    block(width: 100%, {
      place(bottom + right, ending)
      body
    })
  } else if body.func() in (block, box) {
    let fields = body.fields()
    let inner = fields.remove("body")
    body.func()(append-ending(inner, ending), ..fields)
  } else if body.func() == sequence and body.children.len() > 0 {
    let children = body.children
    let last = children
      .rev()
      .position(it => it.func() not in ([ ].func(), parbreak))
    if last == none { join-pieces((body, ending)) } else {
      let index = children.len() - last - 1
      keep-label(body, join-pieces((
        ..children.slice(0, index),
        append-ending(children.at(index), ending),
        ..children.slice(index + 1),
      )))
    }
  } else { body + ending }
}

// A statement is a run of ordinary paragraphs with a little extra space
// around it, as in the book, not a block of its own: then Typst's paragraph
// indent works as in the book. The statement's head is indented like a new
// paragraph, so is the paragraph after the statement, while text that
// continues a sentence after a display formula stays flush left (a block
// would break the chain of paragraphs and lose the first two indents).
//
// Typst does not indent a paragraph that follows a display. A statement
// starts a new paragraph even there, so its first paragraph is indented
// always (`all: true`, the amount of book-style.typ); the rest of the
// statement follows the ordinary rule.
#let indent-first(body) = {
  let styled(it) = {
    set par(first-line-indent: (amount: 1.25em, all: true))
    it
  }
  let breaks(it) = (
    it.func() in (parbreak, block, grid, table, figure, list, enum, terms)
      or (it.func() == math.equation and it.block)
  )
  if body.func() == sequence and body.children.len() > 0 {
    let end = body.children.position(breaks)
    if end == none { styled(body) } else {
      join-pieces((
        styled(join-pieces(body.children.slice(0, end))),
        ..body.children.slice(end),
      ))
    }
  } else { styled(body) }
}

// The space around a statement is the paragraph spacing and a little more.
// It is weak and collapses with the paragraph spacing and with the space of
// a neighbouring statement, so two statements in a row are as far apart as
// a statement and a paragraph, not twice as far.
#let statement-space = context v(par.spacing + 0.35em, weak: true)
#let statement-block(body) = {
  parbreak()
  statement-space
  indent-first(body)
  parbreak()
  statement-space
}


#let theorem-like(
  kind,
  family,
  title,
  numbered,
  prime,
  body,
  italic: true,
  number-visible: true,
) = {
  if family in ("th", "prop") { family-counter("cor").update(0) }
  let prime = if prime != none { str(references-in(prime).first()) }
  let head = {
    if numbered and prime == none { family-counter(family).step() }
    context {
      record(
        family,
        numbered: numbered,
        prime: prime,
        caption: if title != none { title } else { kind },
      )
      let n = if numbered { object-number(family, here(), prime: prime).last() }
      text(style: "normal")[#strong[
          #kind#if n != none and number-visible [ #n]#if title != none [
            #title].
        ]
      ]
    }
  }
  text(
    style: if italic { "italic" } else { "normal" },
    statement-block(prepend-heading(body, head)),
  )
}
#let theorem(
  kind: "Теорема",
  title: none,
  numbered: true,
  number-visible: true,
  prime: none,
  body,
) = theorem-like(
  kind,
  "th",
  title,
  numbered,
  prime,
  body,
  number-visible: number-visible,
)
#let principle(title: none, numbered: false, body) = theorem-like(
  "Принцип",
  "th",
  title,
  numbered,
  none,
  body,
)
#let lemma(title: none, numbered: true, body) = theorem-like(
  "Лемма",
  "lem",
  title,
  numbered,
  none,
  body,
)
#let proposition(title: none, numbered: true, body) = theorem-like(
  "Предложение",
  "prop",
  title,
  numbered,
  none,
  body,
)
#let corollary(title: none, numbered: false, italic: true, body) = theorem-like(
  "Следствие",
  "cor",
  title,
  numbered,
  none,
  body,
  italic: italic,
)
#let plain-statement(kind, family, numbered, body) = {
  if numbered { family-counter(family).step() }
  let head = context {
    record(family, numbered: numbered, caption: kind)
    strong[#kind#if numbered [ #object-number(family, here()).last()]. ]
  }
  statement-block(prepend-heading(body, head))
}
#let remark(numbered: false, body) = plain-statement(
  "Замечание",
  "rem",
  numbered,
  body,
)
#let example(numbered: false, body) = plain-statement(
  "Пример",
  "exm",
  numbered,
  body,
)
#let definition(body) = statement-block(prepend-heading(body, [*Определение.*
]))
#let proof(title: [Доказательство], body) = statement-block(
  prepend-heading(body, [#emph(title). ]),
)
#let difficulty(kind) = {
  if kind == "core" { super[°] } else if kind == "hard" { super("*") } else if (
    kind == "very-hard"
  ) { super("**") } else { assert(kind == none) }
}
#let hint-link(from, number, target) = context metadata((
  kind: "hint-link",
  from: from,
  number: number,
  position: here().position(),
  target-position: if target != none { target.position() },
))
#let problem(difficulty: none, title: none, body) = {
  family-counter("pr").step()
  let head = context {
    record("pr")
    let number = object-number("pr", here())
    let hints = query(metadata.where(value: (
      kind: "hint",
      family: "pr",
      number: number,
    )))
    let answers = query(metadata.where(value: (
      kind: "answer",
      family: "pr",
      number: number,
    )))
    assert(hints.len() <= 1, message: "More than one hint for a problem")
    assert(answers.len() <= 1, message: "More than one answer for a problem")
    let target = if hints.len() == 1 { hints.first().location() } else if (
      answers.len() == 1
    ) { answers.first().location() }
    hint-link("problem", number, target)
    let mark = if difficulty == "core" { super[°] } else if (
      difficulty == "hard"
    ) { super("*") } else if difficulty == "very-hard" { super("**") }
    let words = strong[Задача #number.last()#mark#if title != none [ #title].]
    if target == none { words } else { link(target, words) }
    [ ]
  }
  text(size: 0.9em, statement-block(prepend-heading(body, head)))
}
#let hint(problems, body, title: [Указание], kind: "hint") = {
  assert(kind in ("hint", "answer"))
  let targets = references-in(problems)
  assert(targets.len() > 0)
  let head = context {
    let links = targets
      .enumerate()
      .map(pair => {
        let (index, target) = pair
        let found = numbered-record(target)
        let number = if found == none { ("?",) } else { record-number(found) }
        [#metadata((kind: kind, family: "pr", number: number))<numbered>]
        let shown = if targets.len() == 1 {
          emph[#title.]
        } else { number-text(str(number.last())) }
        if found == none { shown } else {
          hint-link(kind, number, found.location())
          link(found.location(), shown)
        }
      })
    if targets.len() == 1 { [#links.first() ] } else {
      [#emph[#title к задачам] #links.join[, ]. ]
    }
  }
  text(size: 0.9em, statement-block(prepend-heading(body, head)))
}
#let answer(problems, body) = hint(
  problems,
  body,
  title: [Ответ],
  kind: "answer",
)
#let supplementary-counter = counter("supplementary-bibliography")
#let examples(..items) = context {
  let start = family-counter("exm").get().first() + 1
  enum(numbering: "1.", start: start, ..items.pos())
}
#let example-item(body) = [
  #family-counter("exm").step()
  #record("exm")#body
]
#let book-figure(body) = {
  family-counter("fig").step()
  figure(
    [#record("fig")#body],
    caption: context [Рис. #object-number("fig", here()).last().],
    numbering: none,
    supplement: none,
  )
}
#let editorial-counter = counter("editorial-bibliography")
#let bib-item(supplementary: false, editorial: false, body) = {
  assert(not (supplementary and editorial))
  if editorial { editorial-counter.step() } else if supplementary {
    supplementary-counter.step()
  } else {
    family-counter("bib").step()
  }
  let head = context {
    let tag = if editorial {
      "Р" + str(editorial-counter.get().first())
    } else if supplementary {
      str(supplementary-counter.get().first()) + "*"
    }
    record("bib", tag: tag)
    let n = object-number("bib", here(), tag: tag).last()
    [#n. ]
  }
  statement-block(prepend-heading(body, head))
}
