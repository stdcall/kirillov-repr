/- Kirillov §1.2, p.10: uniqueness of a universal object of a fixed type.
   Hom/composition/identity correspond to Mor/composition/1_X in the book.
   Initiality is the book's universal repelling object. Applying the result
   in the opposite category gives the universal attracting case.

   The general lemma proves inverse identities between the two unique maps;
   it uses only uniqueness of endomorphisms, without assuming the conclusion.
   Empty/Unit explain why the two TYPES must not be mixed. They do not claim
   that the book's implicit 'respectively' is a mathematical printing error.
   No existence theorem for universal objects or category equivalence is
   formalized here. -/
universe u v
namespace KirillovRepr.InitialUniqueness

def Initial {Obj : Type u} (Hom : Obj → Obj → Type v) (X : Obj) : Prop :=
  ∀ Y, ∃ f : Hom X Y, ∀ g : Hom X Y, g = f

theorem initial_inverse_maps {Obj : Type u} (Hom : Obj → Obj → Type v)
    (ident : (X : Obj) → Hom X X)
    (comp : {X Y Z : Obj} → Hom Y Z → Hom X Y → Hom X Z)
    {X Y : Obj} (hx : Initial Hom X) (hy : Initial Hom Y) :
    ∃ f : Hom X Y, ∃ g : Hom Y X,
      comp g f = ident X ∧ comp f g = ident Y := by
  obtain ⟨f, _⟩ := hx Y
  obtain ⟨g, _⟩ := hy X
  obtain ⟨ix, hix⟩ := hx X
  obtain ⟨iy, hiy⟩ := hy Y
  exact ⟨f, g, (hix (comp g f)).trans (hix (ident X)).symm,
    (hiy (comp f g)).trans (hiy (ident Y)).symm⟩

theorem empty_initial : Initial (fun A B : Type => A → B) Empty := by
  intro Y
  refine ⟨Empty.elim, ?_⟩
  intro g
  funext x
  exact Empty.elim x

theorem unit_final : ∀ Y : Type, ∃ f : Y → Unit, ∀ g : Y → Unit, g = f := by
  intro Y
  refine ⟨fun _ => (), ?_⟩
  intro g
  funext y
  exact Unit.ext (g y) ()

theorem no_inverse_empty_unit : ¬ Nonempty (Unit → Empty) := by
  intro ⟨g⟩
  exact Empty.elim (g ())

#print axioms initial_inverse_maps
#print axioms empty_initial
#print axioms unit_final
#print axioms no_inverse_empty_unit
end KirillovRepr.InitialUniqueness
