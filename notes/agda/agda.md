---
author: Daniel Fava
date: March 2019
geometry:
---
\newif\ifslides\slidesfalse

\vspace{12pt}

# A *way too brief* introduction to Agda

\vspace{18pt}

Daniel S. Fava

University of Oslo, Norway

March, 2019

\ifslides
\pagebreak
\fi

## Recapitulation

Curry-Howard

Correspondence between *logics* and *models of computation*

- natural deduction ⇔ lambda calculus
- Hilbert-style deduction ⇔ combinators

Example:

```
f : A→B
``` 

`f` as a function from a proof `a` of proposition `A` to a proof `f(a)` of `B`  [Brouwer-Heyting-Kolmogorov]

- Types as logical formulas, programs as proofs.
- "Type `A` is inhabited" as "proposition `A` has a proof."

\ifslides
\pagebreak
\fi

## Recapitulation

False formula (logic) ⇔ bottom type (computation)

Constructive:  `¬A` means `A → ⊥`

- `¬¬A` does not mean `A`
- `¬¬A` means `¬(A →⊥)` which means `(A → ⊥) → ⊥`

\ifslides
\pagebreak
\fi

Want a language where program, specification, and proofs are all under the same umbrella.

## Dependent types

Rich types that 
more closely express program behavior.

\vspace{12pt}

*Type inference is so last century.*

*The right thing to do is to write the types down,
and then get as much mechanical assistance generating the program as possible.*

Conor McBride

\ifslides
\pagebreak
\fi

## Internal vs. External verification

Example: Creates a list of `n` elements `a : A`

```
gen 3 "uio" ≡ ["uio", "uio", "uio"]
```

- Using `List A`
    - No internal verification
    - Must proof two invariants externally: size and constant element


- Using `Vec A (n : ℕ)`
    - Internal verification: Size is part of `Vec`'s type
    - Must prove constant element externally

- Define `UVec (a : A) (n : ℕ)`
    - Both properties (size and constant element) are internally verified

\iffalse
https://wenkokke.github.io/2016/insertion-sort-in-agda/
\fi

\ifslides
\pagebreak
\fi

## Pi type

In addition to the function type `A→B`, we have the Pi type:

```
Π(x:A) → B(x)
```

where `B(x)` is a *type family*

\vspace{12pt}

Pi type (programming) ⇔ Universal quantification (logic)


\ifslides
\pagebreak
\fi

## Equality type

```
a ≡ b
```

- Normalize (apply definitions) both sides then compare.
- Equality type is proven with `refl`, in other words,
    - `refl` is a constructor for the equality type.


Notions of [equality](https://ncatlab.org/nlab/show/equality)

- definitional (intensional)
- propositional (extensional)
- computational

\ifslides
\pagebreak
\fi


## Type erasure

- A vector is just a list after type erasure
    - Invariant related to size is checked statically
- What can be erased and what can't?
    - At the crux of making the language efficient

\iffalse
\ifslides
\pagebreak
\fi

## Type levels

TODO: QUESTION: WHY?
\fi

\iffalse
\ifslides
\pagebreak
\fi

## Braun trees
\fi
