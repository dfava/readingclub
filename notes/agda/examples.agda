module examples where

import Relation.Binary.PropositionalEquality as Eq
open Eq using (_≡_; refl; sym; trans; cong)

open import Level using (_⊔_)

open import Data.Nat using (ℕ; zero; suc; _≤_)

import Data.List as List
open List using (List; length)
import Data.List.All using (All)

import Data.Vec as Vec
open Vec using (Vec)
import Data.Vec.All using (All; lookup)



{-- Using Lists
The type does not express that the list will have size n
or that all list elements will be the same a : A
--}
gen𝕃 : ∀ {A : Set} → (n : ℕ) → (a : A) → List A 
gen𝕃 0 a = List.[]
gen𝕃 (suc n) a = a List.∷ gen𝕃 n a

sizeGen𝕃 : ∀ {A : Set} (n : ℕ) (a : A) → length (gen𝕃 n a ) ≡ n
sizeGen𝕃 0 a = {!!}
sizeGen𝕃 (suc n) a = {!!}
{-- sizeGen𝕃 (suc n) a rewrite sizeGen𝕃 n a = refl --}


{-- postulate for assuming true without proof --}
postulate constGen𝕃 : ∀ {A : Set} (n : ℕ) (a : A) → Data.List.All.All (_≡ a) (gen𝕃 n a)




{-- Using Vecs
The type expresses that the result will have size n
It does not express that all elements will be the same a : A
--}
gen𝕍 : ∀ {A : Set} → (n : ℕ) → (a : A) → Vec A n
gen𝕍 0 a = Vec.[]
gen𝕍 (suc n) a = a Vec.∷ gen𝕍 n a

constGen𝕍 : ∀ {A : Set} (n : ℕ) (a : A) → Data.Vec.All.All (_≡ a) (gen𝕍 n a)
constGen𝕍 0 a = {!!} {-- Data.Vec.All.All.[] --}
constGen𝕍 (suc n) a = {!!} {-- refl Data.Vec.All.All.∷ (constGen𝕍 n a) --}




infixr 5 _∷_by_

data UVec {ℓ} {A : Set ℓ} : ℕ → A → Set ℓ where
  []  : ∀ {a : A} → UVec zero a
  _∷_by_ : ∀ {n} {a} (x : A) (xs : UVec n a) → x ≡ a → UVec (suc n) a

{--
Evaluate (Ctrl-c Ctrl-n) the following
  1 UVec.∷ UVec.[] by refl
  1 UVec.∷ (1 UVec.∷ UVec.[] by refl) by refl
  1 UVec.∷ (2 UVec.∷ UVec.[] by refl) by refl
--}

genU𝕍 : ∀ {A : Set} → (n : ℕ) → (a : A) → UVec n a
genU𝕍 zero _ = UVec.[]
genU𝕍 (suc n) a = a UVec.∷ (genU𝕍 n a) by refl
