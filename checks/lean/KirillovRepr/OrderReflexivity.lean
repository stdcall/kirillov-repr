import Std.Tactic

namespace KirillovRepr.OrderReflexivity

def StrictGreater (x y : Nat) : Prop := y < x

def PrintedLinear (Y : Nat → Prop) : Prop :=
  ∀ x, Y x → ∀ y, Y y → StrictGreater x y ∨ StrictGreater y x

theorem transitive :
    ∀ x y z, StrictGreater x y → StrictGreater y z → StrictGreater x z := by
  unfold StrictGreater
  omega

theorem antisymmetric :
    ∀ x y, StrictGreater x y → StrictGreater y x → x = y := by
  unfold StrictGreater
  omega

theorem printed_linear_empty (Y : Nat → Prop) (h : PrintedLinear Y) :
    ∀ x, ¬Y x := by
  intro x hx
  have hxx := h x hx x hx
  unfold StrictGreater at hxx
  omega

theorem every_printed_linear_subset_bounded :
    ∀ Y, PrintedLinear Y → ∃ b, ∀ y, Y y → StrictGreater b y := by
  intro Y h
  refine ⟨0, ?_⟩
  intro y hy
  exact False.elim (printed_linear_empty Y h y hy)

theorem no_maximal_element :
    ¬∃ m, ∀ n, StrictGreater n m → n = m := by
  rintro ⟨m, hm⟩
  have hs : StrictGreater (m + 1) m := by
    unfold StrictGreater
    omega
  have he := hm (m + 1) hs
  omega

theorem not_reflexive : ¬∀ x, StrictGreater x x := by
  intro h
  have h0 := h 0
  unfold StrictGreater at h0
  omega

#print axioms transitive
#print axioms antisymmetric
#print axioms printed_linear_empty
#print axioms every_printed_linear_subset_bounded
#print axioms no_maximal_element
#print axioms not_reflexive

end KirillovRepr.OrderReflexivity
