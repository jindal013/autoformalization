# Introduction to Real Analysis

## Chapter 1: The Real Numbers

### 1.1 Field Axioms

The real numbers form a field, which means they satisfy the following axioms:

**A1.** For all a, b ∈ ℝ, a + b = b + a (commutativity of addition)
**A2.** For all a, b, c ∈ ℝ, (a + b) + c = a + (b + c) (associativity of addition)
**A3.** There exists 0 ∈ ℝ such that for all a ∈ ℝ, a + 0 = a (additive identity)
**A4.** For each a ∈ ℝ, there exists -a ∈ ℝ such that a + (-a) = 0 (additive inverse)

**M1.** For all a, b ∈ ℝ, a · b = b · a (commutativity of multiplication)
**M2.** For all a, b, c ∈ ℝ, (a · b) · c = a · (b · c) (associativity of multiplication)
**M3.** There exists 1 ∈ ℝ such that for all a ∈ ℝ, a · 1 = a (multiplicative identity)
**M4.** For each a ∈ ℝ with a ≠ 0, there exists a⁻¹ ∈ ℝ such that a · a⁻¹ = 1 (multiplicative inverse)

**D.** For all a, b, c ∈ ℝ, a · (b + c) = a · b + a · c (distributivity)

### 1.2 Order Axioms

The real numbers are ordered, satisfying:

**O1.** For all a, b ∈ ℝ, exactly one of a < b, a = b, or a > b holds (trichotomy)
**O2.** For all a, b, c ∈ ℝ, if a < b and b < c, then a < c (transitivity)
**O3.** For all a, b, c ∈ ℝ, if a < b, then a + c < b + c (addition preserves order)
**O4.** For all a, b, c ∈ ℝ, if a < b and c > 0, then a · c < b · c (multiplication preserves order)

### 1.3 Completeness Axiom

**C.** Every nonempty subset of ℝ that is bounded above has a least upper bound.

## Chapter 2: Sequences and Series

### 2.1 Convergence of Sequences

A sequence (aₙ) converges to L if for every ε > 0, there exists N ∈ ℕ such that for all n ≥ N, |aₙ - L| < ε.

**Theorem 2.1.1 (Uniqueness of Limits):** If a sequence converges, its limit is unique.

**Proof:** Suppose (aₙ) converges to both L and M. Then for any ε > 0, there exist N₁, N₂ ∈ ℕ such that:

- For n ≥ N₁, |aₙ - L| < ε/2
- For n ≥ N₂, |aₙ - M| < ε/2

Let N = max(N₁, N₂). Then for n ≥ N:
|L - M| = |L - aₙ + aₙ - M| ≤ |L - aₙ| + |aₙ - M| < ε/2 + ε/2 = ε

Since this holds for all ε > 0, we must have L = M.

### 2.2 Cauchy Sequences

A sequence (aₙ) is Cauchy if for every ε > 0, there exists N ∈ ℕ such that for all m, n ≥ N, |aₘ - aₙ| < ε.

**Theorem 2.2.1:** A sequence converges if and only if it is Cauchy.

## Chapter 3: Continuity

### 3.1 Definition of Continuity

A function f: ℝ → ℝ is continuous at a point c if for every ε > 0, there exists δ > 0 such that for all x with |x - c| < δ, we have |f(x) - f(c)| < ε.

**Theorem 3.1.1:** If f and g are continuous at c, then:

1. f + g is continuous at c
2. f · g is continuous at c
3. If g(c) ≠ 0, then f/g is continuous at c

### 3.2 Intermediate Value Theorem

**Theorem 3.2.1 (Intermediate Value Theorem):** Let f be continuous on [a, b]. If f(a) < f(b) and y is between f(a) and f(b), then there exists c ∈ (a, b) such that f(c) = y.

## Chapter 4: Differentiation

### 4.1 Definition of Derivative

The derivative of f at a point a is defined as:
f'(a) = lim\_{h→0} (f(a + h) - f(a))/h

if this limit exists.

**Theorem 4.1.1:** If f is differentiable at a, then f is continuous at a.

**Proof:** Since f is differentiable at a, the limit lim*{h→0} (f(a + h) - f(a))/h exists. Therefore:
lim*{h→0} (f(a + h) - f(a)) = lim\_{h→0} h · (f(a + h) - f(a))/h = 0 · f'(a) = 0

This shows that lim\_{h→0} f(a + h) = f(a), so f is continuous at a.

### 4.2 Mean Value Theorem

**Theorem 4.2.1 (Mean Value Theorem):** Let f be continuous on [a, b] and differentiable on (a, b). Then there exists c ∈ (a, b) such that:
f'(c) = (f(b) - f(a))/(b - a)

## Chapter 5: Integration

### 5.1 Riemann Sums

A partition of [a, b] is a finite set P = {x₀, x₁, ..., xₙ} where a = x₀ < x₁ < ... < xₙ = b.

The Riemann sum of f with respect to P and sample points ξᵢ ∈ [xᵢ₋₁, xᵢ] is:
S(f, P, ξ) = Σᵢ₌₁ⁿ f(ξᵢ)(xᵢ - xᵢ₋₁)

### 5.2 Definition of Riemann Integral

A function f is Riemann integrable on [a, b] if there exists a number I such that for every ε > 0, there exists δ > 0 such that for any partition P with mesh less than δ and any choice of sample points ξ, we have |S(f, P, ξ) - I| < ε.

**Theorem 5.2.1:** If f is continuous on [a, b], then f is Riemann integrable on [a, b].

### 5.3 Fundamental Theorem of Calculus

**Theorem 5.3.1 (First Fundamental Theorem):** Let f be continuous on [a, b] and define F(x) = ∫ₐˣ f(t) dt. Then F is differentiable on (a, b) and F'(x) = f(x).

**Theorem 5.3.2 (Second Fundamental Theorem):** Let f be continuous on [a, b] and let F be any antiderivative of f. Then:
∫ₐᵇ f(x) dx = F(b) - F(a)
