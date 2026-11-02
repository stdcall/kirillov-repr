import Std.Tactic

namespace KirillovRepr.QuotientFactorization

variable {X Q Y : Type}

def FactorsThrough (p : X → Q) (f : X → Y) (g : Q → Y) : Prop :=
  ∀ x, g (p x) = f x

theorem constant_on_fibers_of_factorization
    (p : X → Q) (f : X → Y) (g : Q → Y)
    (hg : FactorsThrough p f g) :
    ∀ x x', p x = p x' → f x = f x' := by
  intro x x' hp
  calc
    f x = g (p x) := (hg x).symm
    _ = g (p x') := congrArg g hp
    _ = f x' := hg x'

theorem factorization_exists_unique
    (p : X → Q) (f : X → Y)
    (surjective : ∀ q, ∃ x, p x = q)
    (constant : ∀ x x', p x = p x' → f x = f x') :
    ∃ g, FactorsThrough p f g ∧
      ∀ h, FactorsThrough p f h → h = g := by
  classical
  let representative : Q → X := fun q => Classical.choose (surjective q)
  have representative_eq : ∀ q, p (representative q) = q := by
    intro q
    exact Classical.choose_spec (surjective q)
  let g : Q → Y := fun q => f (representative q)
  have factors : FactorsThrough p f g := by
    intro x
    exact constant (representative (p x)) x (representative_eq (p x))
  refine ⟨g, factors, ?_⟩
  intro h hh
  funext q
  obtain ⟨x, hx⟩ := surjective q
  calc
    h q = h (p x) := congrArg h hx.symm
    _ = f x := hh x
    _ = g (p x) := (factors x).symm
    _ = g q := congrArg g hx

#print axioms constant_on_fibers_of_factorization
#print axioms factorization_exists_unique

end KirillovRepr.QuotientFactorization
