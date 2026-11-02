// Sections run through the book; statements restart in each subsection.
// The unnumbered part headings do not reset the section counter.
#let place-key(location) = {
  let values = counter(heading).at(location)
  (values.at(1, default: 0), values.at(2, default: 0))
}
#let family-depth = (
  pr: 2,
  th: 2,
  lem: 2,
  prop: 2,
  cor: 2,
  rem: 2,
  exm: 2,
  exc: 2,
  eq: 2,
  tab: 0,
  fig: 0,
  bib: 0,
)
#let family-counter(family) = counter("numbered:" + family)
#let formula-primes = (
  "eq:right-section-factorization": <eq:left-section-factorization>,
  "eq:right-section-haar": <eq:left-section-haar>,
  "eq:right-quasi-invariant": <eq:left-quasi-invariant>,
  "eq:right-section-cocycle": <eq:left-section-cocycle>,
  "eq:real-character-norm": <eq:irreducible-character-norm>,
  "eq:vector-field-flow-coordinates": <eq:vector-field-flow>,
  "eq:lie-induced-intertwiner-kernel": <eq:finite-induced-intertwiner-kernel>,
  "eq:extension-coset-factorization": <eq:projective-multiplier-cocycle>,
  "eq:prequantization-cotangent-operator": <eq:prequantization-local-operator>,
  "eq:homogeneous-differential-form-equivariance": // Shares (6).
  <eq:homogeneous-tensor-field-equivariance>,
)
#let formula-prime-marks = (:)
#let formula-tags = ("eq:orbit-character-formula": "Φ")
#let restart-counters(level) = {
  for (family, depth) in family-depth {
    if depth > 0 and depth >= level - 1 { family-counter(family).update(0) }
  }
}
#let numbered-record(target) = {
  if query(target).len() != 1 { return none }
  query(selector(<numbered>).within(target)).at(0, default: none)
}
#let object-number(
  family,
  location,
  prime: none,
  prime-mark: "′",
  tag: none,
) = {
  let scope = place-key(location).slice(0, family-depth.at(family))
  if tag != none { return (..scope, tag) }
  if prime != none {
    let base = numbered-record(label(prime))
    let number = if base == none { ("?",) } else { base.value.number }
    return (..number.slice(0, -1), str(number.last()) + prime-mark)
  }
  (..scope, family-counter(family).at(location).first())
}
#let record-number(item) = {
  if item.value.kind in ("hint", "answer") { return item.value.number }
  if item.value.at("native", default: false) { return item.value.number }
  if item.value.family == "heading" {
    return place-key(item.location()).slice(0, item.value.level - 1)
  }
  if not item.value.at("numbered", default: true) { return none }
  object-number(
    item.value.family,
    item.location(),
    prime: item.value.at("prime", default: none),
    prime-mark: item.value.at("prime-mark", default: "′"),
    tag: item.value.at("tag", default: none),
  )
}
#let record(
  family,
  numbered: true,
  caption: none,
  ..flags,
) = context [#metadata((
  kind: "numbered",
  family: family,
  numbered: numbered,
  caption: caption,
  ..flags.named(),
  number: if numbered { object-number(family, here(), ..flags.named()) },
))<numbered>]
