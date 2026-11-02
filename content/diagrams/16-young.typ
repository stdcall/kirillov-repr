#import "@preview/cetz:0.5.2"

// A Young table is determined by its non-increasing row lengths.
#let young-tableau(rows) = {
  assert(rows.len() > 0 and rows.all(n => type(n) == int and n > 0))
  assert(rows.zip(rows.slice(1)).all(pair => pair.at(0) >= pair.at(1)))
  cetz.canvas(length: 6mm, {
    import cetz.draw: line, set-style
    set-style(stroke: 0.5pt)
    let at(x, y) = (x, -0.55 * y)
    line(at(0, 0), at(rows.first(), 0))
    for (row, width) in rows.enumerate() {
      line(at(0, row + 1), at(width, row + 1))
    }
    for column in range(rows.first() + 1) {
      let height = rows.filter(width => width >= calc.max(1, column)).len()
      line(at(column, 0), at(column, height))
    }
  })
}
