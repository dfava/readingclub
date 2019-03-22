module exData where

{-- This is comment block --}

{-- Below we are defining natural numbers.
Identifiers names from unicode characters
   ℕ is \bN
  → as \->
--}

data ℕ : Set where
  zero : ℕ
  suc  : ℕ → ℕ

{-- Below is a pragma.
It allows us to use, for example, 1 as opposed to suc zero --}
{-# BUILTIN NATURAL ℕ #-}


{-- Lists --}

infixr 5 _∷l_

data List (A : Set) : Set where
  []  : List A
  _∷l_ : A → List A → List A


{-- Vectors
Pie type, or forall type, shows up in the definition of vectors --}

infixr 5 _∷_

{-- Lots to unpack:
 {}     for implicit arguments
 Set ℓ  are the types at type level ℓ
 A      is a type from type level Set ℓ
--}
data Vec {ℓ} (A : Set ℓ) : ℕ → Set ℓ where
  []  : Vec A zero
  _∷_ : ∀ {n} (x : A) (xs : Vec A n) → Vec A (suc n)

{-- Comment
Normalize 1 ∷ 2 ∷ []
--}
