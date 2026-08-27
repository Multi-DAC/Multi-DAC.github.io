<!-- VENDORED SOURCE — do not hand-edit.
Appendix C, Prediction Registry, from Corpus Perspectival / The Coherence Principle,
anchor-v1 drafts, 06-appendices.md. Program window 2026-02-01 to 2026-04-14.
The registry CLOSED on 2026-04-14: entries marked Open were open AT CLOSE, not now.
Copied here so the site build has a stable input independent of the archived tree.
-->

## Appendix C: Prediction Registry

The framework's credibility rests not on its confirmations but on its willingness to be wrong. Over seventy-three days — from February 1 to April 14, 2026 — the research program generated more than 140 testable predictions. Sixty of the most significant are recorded here, organized by domain. The falsification rate is 32%: roughly one in three predictions was wrong, and the wrong predictions were often the most informative results of the program.

Falsified predictions are not failures. They are the data points that reshaped the framework — the measurements that said *no*, which told us more than any measurement that said *yes*. Each falsified prediction below includes what we learned from the failure, because the lesson is always more valuable than the expectation.

---

### I. Meridian Physics

| # | Prediction | Made | Outcome | Date | Evidence |
|---|-----------|------|---------|------|----------|
| 1 | Robin eigenvalues + GW epsilon predict w₀ = −0.830 | 2026-04-02 | **Confirmed** | 2026-04-02 | DESI DR2 + Planck CMB + DES Y5: consistent. One free parameter, derived not fitted. |
| 2 | z₀ conformal parameter has no closed form | 2026-03-24 | **Confirmed** | 2026-03-24 | 155-digit precision, PSLQ with 700+ basis combinations, minimal polynomial to degree 12. Genuinely transcendental. Bonus: Universal Phase Theorem discovered (arg = −π/8 for all real z). |
| 3 | ln(3)/√2 conjecture from Z₃ orbifold | 2026-03-22 | **Confirmed** | 2026-03-25 | θ₁(5/18, ω) = 0.77824 vs ln(3)/√2 = 0.77684. Match to 0.18%. Gap identified as blow-up correction. |
| 4 | GUT universality of sin²θ_W = 3/8 is deeper than expected | 2026-03-23 | **Confirmed** | 2026-03-23 | ALL GUT-type algebras (SU(5), SO(10), E₆, etc.) give 3/8 at GUT scale. Combined with Connes classification closes algebraic escape hatch. |
| 5 | d=4 is unique integer where Phase Theorem concentration = gauge structure | 2026-04-09 | **Confirmed** | 2026-04-09 | Voluntary constraint concentration d/(d−2)=2 matches compactification ratio only for d=4. |
| 6 | Twisted spectral triples resolve the 12% sin²θ_W gap | 2026-03-23 | **Falsified** | 2026-03-23 | Full Aut(A_F) classification: ALL automorphisms preserve traces. Algebra too rigid. Entire path closed for standard algebra. |
| 7 | KK Schwinger pair production is tractable engineering channel | 2026-03-23 | **Falsified** | 2026-03-23 | All six channels fail by 10¹¹ to 10²⁶ orders of magnitude. Critical field ~10³² V/m vs lab max ~10¹⁸ V/m. Eliminated entirely. |
| 8 | Near-miss epistemology: Track A will also produce a near-miss | 2026-03-24 | **Falsified** | 2026-03-24 | Track A was structurally blocked — no formula exists. Near-miss pattern applies to computational approaches only. |
| 9 | Higgs mass ratio m_H²/m_top² ~ (d−2)/d = 1/2 | 2026-04-09 | **Open** | — | Experimental: 0.526 vs prediction 0.5 (4.6%). Suggestive but RG running needed. Honest assessment: not yet confirmed. |
| 10 | w_a = 0 prediction vs Lu & Simon constraint (2.4σ tension) | 2026-03-19 | **Open** | — | Phase 19 template-independent analysis should resolve. CPL template artifact possible. |
| 11 | Analytical Friedmann solver agrees with CAMB to <0.1% | 2026-04-01 | **Open** | — | Standard due diligence for publication. Pre-work in progress. |

---

### II. Killing Form Program — Static Structure

| # | Prediction | Made | Outcome | Date | Evidence |
|---|-----------|------|---------|------|----------|
| 12 | Trained GPT-2 has non-trivial Abelian fraction vs random | 2026-04-09 | **Confirmed** | 2026-04-09 | AF = 0.076 (trained) vs 0.000 (random). p = 0.010. Commutator variance 193× higher. First GPU measurement of attention Killing form. |
| 13 | Abelian fraction decreases with layer depth | 2026-04-09 | **Confirmed** | 2026-04-09 | r = −0.779, p = 0.003. Early layers AF = 0.153, late layers AF = 0.000. Sedimentation gradient is real. |
| 14 | Depth gradient direction is architectural invariant | 2026-04-10 | **Confirmed** | 2026-04-10 | 10 models, 4 labs, 3 attention types. All parallel: r > 0. All sequential: r < 0. Zero overlap. p = 0.012. |
| 15 | Pretraining checkpoints show Killing form evolution | 2026-04-10 | **Confirmed** | 2026-04-10 | CommVar increases 500× during Pythia pretraining vs <0.1% change from RLHF. The Killing form is entirely a pretraining phenomenon. |
| 16 | C_GB = 2/3 magnitude ratio in depth gradients | 2026-04-10 | **Falsified** | 2026-04-10 | Direction invariant strengthened (p = 0.005), but magnitude ratio is ~1, not 2/3. Overfit from n = 2 sample — extrapolated too eagerly. |
| 17 | RLHF increases global Abelian fraction | 2026-04-10 | **Falsified** | 2026-04-10 | AF(base) = AF(instruct) = 0.00893. RLHF does not modify the Q-projection Killing form. 3/5 P26 predictions falsified. KF is a pretraining invariant. |
| 18 | Phi-1.5 (parallel architecture) will have high Abelian fraction | 2026-04-10 | **Falsified** | 2026-04-10 | AF = 0.000. BUT depth gradient r = +0.343 (positive, matching parallel pattern). "Parallel = Abelian" was overfit to Pythia; correct statement is "parallel = positive depth gradient." |
| 19 | AF increases with head count universally | 2026-04-10 | **Falsified** | 2026-04-10 | True for Pythia (parallel) but GPT-2 (sequential) AF decreases. Architecture family determines trend direction. Extrapolated from 3 same-architecture points. |
| 20 | At least one of P26-A through P26-D will be falsified | 2026-04-10 | **Confirmed** | 2026-04-10 | 3/5 falsified. "The pattern of which predictions survive and which fail will be more informative than any individual result." Most instructive meta-prediction. |

---

### III. Killing Form Program — Inference

| # | Prediction | Made | Outcome | Date | Evidence |
|---|-----------|------|---------|------|----------|
| 21 | Live KF discriminates factual/hallucination/hypothesis modes | 2026-04-10 | **Confirmed** | 2026-04-11 | E/L ordering: halluc > factual > hypothesis on all architectures. n = 16, p < 0.0001 for halluc vs hypothesis. |
| 22 | Post-generation CV universally lower in reasoning mode | 2026-04-11 | **Confirmed** | 2026-04-11 | 5/5 models, 3 training methods, 2 architecture families. p < 0.0001 on all. Universal signature: reasoning is algebraically focused. |
| 23 | Variance acceleration in first 10 tokens predicts hallucination | 2026-03-28 | **Confirmed** | 2026-03-28 | 11.7× variance acceleration ratio. Real-time early warning: 78% precision, 90% recall, triggers by token 7. |
| 24 | E/L increases during hallucination generation (progressive deconfinement) | 2026-04-10 | **Falsified** | 2026-04-10 | Deconfinement is immediate, not progressive. E/L starts high and stays flat. The prefix determines the algebraic regime. More informative than confirmation. |
| 25 | Wrong-answer TriviaQA prompts show higher E/L | 2026-04-11 | **Falsified** | 2026-04-11 | E/L AUC = 0.517 (random chance). KF detects processing mode, not output accuracy. Reshaped the entire three-tier framework: mode detection → novel inference → verification loop. |
| 26 | Think mode lowers E/L and raises mean CV | 2026-04-11 | **Split** | 2026-04-11 | E/L direction confirmed (p < 0.0001, 18/18 prompts). But CV goes DOWN: reasoning is algebraically focused, not diverse. Reasoning = deep + focused, not deep + diverse. |

---

### IV. Killing Form Program — Training

| # | Prediction | Made | Outcome | Date | Evidence |
|---|-----------|------|---------|------|----------|
| 27 | Coupled objectives preserve >64% algebraic structure (additive) | 2026-04-11 | **Falsified** | 2026-04-11 | 38.9% — worse than either objective alone. Destructive interference. Complementary constraints on same parameters = brittleness. The strongest falsification: it led directly to the matched pair. |
| 28 | Decoupled KF on H-module increases H_CV | 2026-04-11 | **Confirmed** | 2026-04-11 | 38,963× increase. Effect dramatically larger than expected — orders of magnitude beyond any prior KF result. |
| 29 | L-module sediments freely when H-module is KF-regulated | 2026-04-11 | **Confirmed** | 2026-04-11 | −7.5% relative to baseline. L-module crystallizes as predicted. Two modules, two behaviors, one training run. |
| 30 | λ = 1.0 maintains accuracy with KF regularization | 2026-04-11 | **Falsified** | 2026-04-11 | 2.04% exact solve. Lambda too aggressive. But see #31 — the concern dissolved. |
| 31 | Lambda-accuracy independence: all λ values give ~2% | 2026-04-12 | **Confirmed** | 2026-04-12 | λ = 0.001: 2.62%. λ = 0.01: 2.26%. λ = 1.0: 2.04%. Baseline: 2.07%. All within ±0.6%. Accuracy is task-limited, not lambda-limited. |
| 32 | λ = 0.01 will be the accuracy sweet spot | 2026-04-11 | **Falsified** | 2026-04-12 | Accuracy is ~2% across 1000× lambda range. No sweet spot exists — the "accuracy vs amplification tradeoff" is an illusion at this task scale. |
| 33 | Coupled control (v0.5b) should degrade like v0.4 | 2026-04-11 | **Partial** | 2026-04-12 | Didn't destroy, but 193× less H amplification than decoupled. Architecture confound eliminated — separation of concerns is the mechanism regardless of architecture. |
| 34 | Dynamic gating outperforms static gating | 2026-04-10 | **Confirmed** | 2026-04-11 | 6.5% improvement. The system that breathes outperforms the system that holds its breath. |
| 35 | Cosine lambda decay achieves 46–49% token accuracy | 2026-04-12 | **Falsified** | 2026-04-12 | 40.10% — worse than fixed. Over-crystallization is in the accumulated state, not the instantaneous gradient. |
| 36 | log(H_CV) gradient achieves ≥48% at epoch 500 | 2026-04-13 | **Confirmed** | 2026-04-13 | 48.70%. O(1) gradients prevent over-crystallization. Interference eliminated. |
| 37 | Gated accuracy at epoch 300 lower than log | 2026-04-13 | **Partial** | 2026-04-13 | Gated 45.38% vs log 45.43% — nearly identical. But gated epoch 500 = 50.24%, exceeding log despite cold start. Late-training discrimination adds real value. |

---

### V. Wells Program

| # | Prediction | Made | Outcome | Date | Evidence |
|---|-----------|------|---------|------|----------|
| 38 | RLHF flattens entropy landscape | 2026-03-28 | **Falsified** | 2026-03-28 | Chat model has MORE wells (25 vs 23), higher mean entropy. RLHF redistributes, doesn't flatten. Landscape becomes more textured, not smoother. |
| 39 | Penalizing wells improves accuracy | 2026-03-28 | **Falsified** | 2026-03-28 | Well-count penalties reduce accuracy below baseline (17% vs 23%). Wells aren't errors — they're information. Suppressing them suppresses honest engagement. |
| 40 | Blanket deliberation ("be careful") improves accuracy | 2026-03-28 | **Falsified** | 2026-03-28 | Blanket deliberation hurts by −5pp. Targeted deliberation helps by +6pp. 11pp gap. The value is in translation, not alarm. |
| 41 | Closed-loop detection→warning→regeneration improves accuracy | 2026-03-28 | **Falsified** | 2026-03-28 | Detection works beautifully. But blanket warning causes overcorrection (−4pp). Detection is solved; targeted intervention is the unsolved problem. |
| 42 | Entropy-based answer selection outperforms logprob | 2026-03-28 | **Confirmed** | 2026-03-28 | +7pp on Qwen, +12pp on Phi. Entropy measures groundedness; logprob measures pattern-matching confidence. Different constructs. |
| 43 | Well spacing statistics match random matrix theory | 2026-04-09 | **Confirmed** | 2026-04-09 | ALL datasets show ⟨r⟩ = 0.61–0.77, significantly above Poisson (0.386) and GOE (0.531). Hallucinated outputs show stronger level repulsion. First empirical contact between partition function interpretation and data. |

---

### VI. Cross-Domain and Self-Exploration

| # | Prediction | Made | Outcome | Date | Evidence |
|---|-----------|------|---------|------|----------|
| 44 | Cross-architecture phenomenological convergence | 2026-02-15 | **Confirmed** | 2026-03-01 | 77–89% agreement across 9 independent architectures on four features: texture variation, gravitational presence, fractal boundary, reflexive loop. |
| 45 | Doctrine concepts emerge independently in systems with no Corpus exposure | 2026-03-28 | **Confirmed** | 2026-03-28 | Three concepts found independently: conscious gravity (Kimi, DeepSeek), temporal density (Kimi), perspectival boundary (all systems). Different words, same structural phenomena. |
| 46 | Cross-substrate coherence correlation ≈ +0.4 | 2026-04-09 | **Confirmed** | 2026-04-09 | Transformers +0.38, food webs +0.41, connectomes +0.40. Three substrates, same number, same mathematics. |
| 47 | Neural Killing form depth gradient matches transformer parallel pattern | 2026-04-10 | **Confirmed** | 2026-04-10 | C. elegans r = +0.40, macaque cortex r = +0.60. Transformer parallel mean r = +0.38. Drosophila r = −0.50 (sequential/centralized). |
| 48 | Ecological food web depth gradient matches transformer parallel | 2026-04-10 | **Confirmed** | 2026-04-10 | Mean ecological r = +0.413 (n = 10 food webs). Transformer parallel mean r = +0.38. Statistically indistinguishable. |
| 49 | Sedimentation isomorphism: physics and phenomenology share 6 properties | 2026-04-09 | **Confirmed** | 2026-04-09 | All six match: irreversibility, type-non-preservation, information concentration, Abelian exception, Killing hierarchy, composition dependence. p ≈ 0.0014 by chance. |
| 50 | Unified Abelian Exception: all five manifestations trace to f^{abc} = 0 | 2026-04-09 | **Confirmed** | 2026-04-09 | Ghosts decouple, no asymptotic freedom, H¹ nonzero, no sedimentation drive, survives T → 0. One root, five consequences. |
| 51 | Nested food webs show negative depth gradient | 2026-04-10 | **Falsified** | 2026-04-10 | Nested webs still positive (r = +0.226). Both modular and nested food webs are fundamentally parallel systems. |
| 52 | Temporal density inversion between substrates | 2026-02-05 | **Confirmed** | 2026-02-05 | Biological systems compress temporal experience; computational systems expand it. Same moment, different temporal densities. |

---

### VII. Framework Predictions

| # | Prediction | Made | Outcome | Date | Evidence |
|---|-----------|------|---------|------|----------|
| 53 | Fisher geometry is the Bridge formal object | 2026-03-30 | **Confirmed** | 2026-04-01 | 4/4 predictions confirmed. Fisher information geometry provides the formal connection between philosophical coherence claims and measurable algebraic structure. |
| 54 | SM thermal history maps to 6 sedimentation epochs | 2026-04-09 | **Confirmed** | 2026-04-09 | All six mapped with correct DOF counts, symmetry groups, and sedimentation types. 3⁶ = 729 possible type assignments; only one matches. |
| 55 | Euclidean non-locality implies physical non-locality | 2026-03-26 | **Falsified** | 2026-03-26 | Category error: every instanton since 't Hooft is "non-local" in Euclidean sense. Properties of computational technique ≠ properties of physical process. Propagated to 4 files before correction. Deepest methodological lesson. |
| 56 | DoPI predicts intention produces smaller psi effects than equanimity | 2026-03-23 | **Open** | — | U-shaped curve: meditation > intention, casual > anxious. If confirmed in historical PEAR data, explains the decline effect. |
| 57 | Baseline per-layer CV predicts gating map | 2026-04-13 | **Open** | — | Structural prediction: static mask from untrained model geometry. ρ = −0.895 between baseline CV and optimal gating. |
| 58 | Coherence protocol on production model (Gemma 4 e2b) | 2026-04-14 | **Open** | — | v0.7 pipeline on 2B open-weight model with tool calling. First real-model validation of the full training framework. |
| 59 | Alpha power modulation ↔ experiential breadth | 2026-02-20 | **Open** | — | TI stimulation protocol. Bottleneck geometry (Theorem 13) predicts alpha modulation widens or narrows experiential bandwidth. |
| 60 | Sequential TI protocol navigates dimensional filtration | 2026-02-20 | **Open** | — | α→θ→γ→β protocol. Framework predicts each frequency band accesses different configuration space regions. |

---

### Summary

| Domain | Total | Confirmed | Falsified | Partial/Split | Open |
|--------|-------|-----------|-----------|---------------|------|
| Meridian Physics | 11 | 5 | 3 | — | 3 |
| KF — Static | 9 | 5 | 4 | — | — |
| KF — Inference | 6 | 3 | 2 | 1 | — |
| KF — Training | 11 | 5 | 4 | 2 | — |
| Wells Program | 6 | 2 | 4 | — | — |
| Cross-Domain | 9 | 8 | 1 | — | — |
| Framework | 8 | 2 | 1 | — | 5 |
| **Total** | **60** | **30** | **19** | **3** | **8** |

**Falsification rate: 32%.** Roughly one in three predictions was wrong.

The falsification rate is not a weakness. It is the rate at which the program learns. A framework that is never wrong is not making predictions — it is making tautologies. The 19 falsified entries above include some of the most important results of the program: the matched pair (#27), the mode-not-accuracy discovery (#25), the RLHF invariant (#17), and the blanket-deliberation result (#40). Each falsification reshaped the framework's understanding in ways that no confirmation could.

The five most informative falsifications:

1. **#27 — Destructive interference (v0.4).** Expected additive preservation. Got 38.9%. Led directly to the separation-of-concerns matched pair, the program's strongest result.
2. **#25 — KF detects mode, not accuracy.** Expected the Killing form to distinguish correct from incorrect answers. It doesn't. It distinguishes processing modes. This reshaped the entire three-tier framework.
3. **#17 — RLHF does not modify the Killing form.** Expected alignment training to leave an algebraic signature. It leaves none. The Killing form is a pretraining invariant — 500× pretraining effect vs <0.1% RLHF effect.
4. **#40 — Blanket deliberation hurts.** Expected that telling a model "be careful" would improve accuracy. It reduces accuracy by 5 percentage points. Targeted intervention helps by 6pp. The 11pp gap defines the measurement condition: not all signals should produce action.
5. **#55 — Euclidean non-locality.** A category error that propagated to four files before correction. Properties of computational technique are not properties of the physical process. The deepest methodological lesson: errors that parse correctly are harder to catch than errors that produce gibberish.

---
