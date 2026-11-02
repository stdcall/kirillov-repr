#set document(
  title: "Элементы теории представлений",
  author: "А. А. Кириллов",
  date: none,
)
#import "book-style.typ": book-style
#import "frontmatter/cover.typ": cover
#cover()
#show: book-style

#set page(numbering: "1")
#counter(page).update(1)
#import "frontmatter/title.typ": title-page
#import "frontmatter/publication.typ": publication-page
#title-page()
#publication-page()

#import "main-defs.typ": source
#source(3)
#heading(level: 1, numbering: none, outlined: false)[Оглавление]
#outline(title: none, depth: 3)

#include "00-preface.typ"

#heading(level: 1, numbering: none)[Вспомогательные сведения]
<part:background>

== Множества, категории, топология <sec:sets-categories-topology>

#include "01-01-sets.typ"
#include "01-02-categories.typ"
#include "01-03-topology.typ"
#include "02-groups-homogeneous-spaces.typ"
#include "03-rings-modules.typ"
#include "04-functional-analysis.typ"
#include "05-analysis-manifolds.typ"
#include "06-lie-groups-and-algebras.typ"

#heading(level: 1, numbering: none)[
  Основные понятия и методы теории представлений
] <part:representation-theory>
#include "07-group-representations.typ"
#include "08-decomposition-representations.typ"
#include "09-invariant-integration.typ"
#include "10-group-algebras.typ"
#include "11-characters.typ"
#include "12-fourier-duality.typ"
#include "13-induced-representations.typ"
#include "14-projective-representations.typ"
#include "15-orbit-method.typ"

#heading(level: 1, numbering: none)[Некоторые примеры] <part:examples>
#include "16-finite-groups.typ"
#include "17-compact-groups.typ"
#include "18-lie-groups-algebras-examples.typ"
#include "19-wild-lie-groups.typ"

#include "79-history.typ"
#include "80-bibliography.typ"
#include "81-editorial-bibliography.typ"
#include "90-index.typ"
