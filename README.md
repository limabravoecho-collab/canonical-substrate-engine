# Canonical Substrate Engine (CSE) v1.9

A deterministic closed-loop logic model with a 2^32 cycle, and an executable Python engine.

CSE is a logic model written in three chained sections: **substrate** (counts only), **conversion bridge** (rates and ratios to human units), and **observer 0** (inputs and readings). Every number is stated in exactly one section; other sections refer to it. The full text — Nests 0 to 13, Blocks A to D, the author's note, and the known open points — is in `CSE_MODEL.txt`.

*Break it, test it, or build upon it — the ledger is open.*

---

## Files

| File | Version | What it is |
|---|---|---|
| `CSE_MODEL.txt` | v1.9 | The model: three sections, Nests 0 to 13, Blocks A to D. Also usable as a prompt. |
| `cse_engine.py` | v1.9 | The model in executable form. Standard library only. |
| `cse_ai_example.py` | v1.3 | How to wire the engine into an AI system. Not yet updated to v1.9. |
| `counter_test.c` | v1.3 | A real 32-bit counter, run through one full loop. Not yet updated to v1.9. |
| `EXAMPLES.md` | v1.3 | Five science placeholders with the arithmetic shown. Uses the v1.3 ratio, 1052. |
| `LICENSE.md` | | PolyForm Noncommercial 1.0.0. |

---

## Quick start

```
python3 cse_engine.py                      # totals: counts, both chains, tier ratio, constants
python3 cse_engine.py selftest             # checks the engine against the model
python3 cse_engine.py state 2147483649     # state after one counted operation
python3 cse_engine.py position 1000        # energy at one position
python3 cse_engine.py local 0.75 1000      # dense matter pocket or void
python3 cse_engine.py regime 0.75 1000     # below / at / above equilibrium label
python3 cse_engine.py rate 0.75 1000       # local time rate direction
python3 cse_engine.py lag 1000             # minimum turn lag at one radius
python3 cse_engine.py room 1000            # room for gravity at one position
python3 cse_engine.py order_a 13.8e9       # Observer 0 years -> ticks
python3 cse_engine.py order_b 4294967295   # ticks -> Observer 0 years
python3 cse_engine.py appendix_a           # Block B: the second-chain results
python3 cse_engine.py block_d              # Block D: Tests 1 to 5
python3 cse_engine.py alpha 0.036          # alpha stack at one delta
```

Every engine command prints JSON. The engine also imports as a module: `import cse_engine as cse`. What each command computes, and the rules it is built on, is stated in its docstring and in `CSE_MODEL.txt`.

---

## Using CSE with an AI

Two ways, which can be combined:

1. **As a prompt.** Put the text of `CSE_MODEL.txt` into the system prompt of any AI. The AI can then discuss the model and reason inside its rules.
2. **As an engine.** Run `cse_engine.py` beside the AI and pass its results on every turn. `cse_ai_example.py` shows each wire point.

If you integrate CSE into your own AI:

1. **Use the LLM as a translator only.** The engine computes. The LLM puts the engine's results into words. Do not let the LLM compute, round or guess engine values.
2. **Customize your prompt for your own target field.** CSE gives the structure. Your prompt gives the voice and the subject.
3. **Add your own tiers.** Any closed cycle in your field can be mapped onto the engine as a fraction from 0 to 1. The example file maps a day and a year.

---

## Research Hypotheses Corpus

A series of exploratory research whitepapers extends the CSE v1.9 discrete register mechanics into cosmology, oncology, longevity, and astrobiology.

**Disclaimer:** These documents are working hypotheses that researchers can explore, think about, and test themselves. They are not established science; they are speculative extensions of CSE. It is entirely up to researchers to evaluate, falsify, or build upon them.

| File Name | Domain | Core CSE Translation |
|---|---|---|
| `HYPOTHESES_INDEX.md` | Overview | Master index summarizing all research hypothesis whitepapers. |
| `TECHNOLOGY_DETERMINISTIC_CSE.md` | Computer Science / AI | Deterministic 32-bit register computing; full-stack CSE (BIOS to OS to Apps); zero-overhead networking; lossless multimedia rendering; hallucination-free LLM decoupling. |
| `THEORY_FINE_STRUCTURE_CONSTANT.md` | Cosmology / QED | Alpha inverse as a composite register stack (136 + 1 + δ), honoring Eddington's initial and final derivations. |
| `THEORY_GRAVITY.md` | Cosmology / General Relativity | Gravity as an emergent pressure/bound-fraction gradient; G_local resolution; singularities capped via 32-bit overflow. |
| `THEORY_DARK_ENERGY.md` | Cosmology / Expansion | Macro-cycle expansion shell vector (M to 0); free energy allocation; apparent acceleration via aggregate δ drift. |
| `THEORY_DARK_MATTER.md` | Cosmology / Galactic Dynamics | Cluster-scale phase error (δ ≈ 0.06); G_local gradient misread by Observer 0 as invisible mass haloes. |
| `THEORY_HUBBLE_TENSION.md` | Cosmology / Constants | H_0 discrepancy resolved via environmental δ stratification across void and cluster propagation paths. |
| `THEORY_RADIATION.md` | Cosmology / Particle Physics | Radiation as automated ledger correction (G = 1 enforcement); Hawking evaporation; CMB as prior cycle ledger close. |
| `HYPOTHESIS_THERMODYNAMIC_TRANSLATION.md` | Thermodynamics / Systems Mechanics | Phenomenological inversion of classical laws; temperature, heat, and cold as Observer 0 UI modulation metrics rather than native substrate properties. |
| `THEORY_VOIDS.md` | Cosmology / Spatial Mechanics | Voids as low-modulation register zones (s/M → 0); thermal sparsity UI rendering; boundary equilibrium mechanics. |
| `BIOLOGY_CANCER_EM.md` | Oncology / Therapeutics | Cellular delta drift (δ → 0.08); subnet decoupling; resonant EM phase-locking to alpha_inv_bio = 137.036 causing overflow lysis. |
| `BIOLOGY_PATHOGEN_ISOLATION.md` | Immunology / Microbiology | Foreign subnet incompatibility (δ_pathogen ≠ 0.036); automated hardware address collision and network isolation. |
| `BIOLOGY_LONGEVITY_BASELINE.md` | Longevity / Aging | Aging as cumulative uncorrected register debt over runtime ticks; retuning δ back to 0.036 restores equilibrium. |
| `BIOLOGY_PLACEBO_BUFFER.md` | Biology / Cognitive Mechanics | Cognitive buffer flushes and register resets as mechanical placebo operations; practical protocols for emotional trauma, physical trauma, addiction, and chronic immune drift. |
| `THEORY_INTERSTELLAR_LIMITS.md` | Astrobiology / Physics | Impossibility of interstellar travel and Kardashev scaling due to atomic decohesion, energy/time variance, and Fermi Paradox containerization. |
| `THEORY_PLANETARY_NEST_LIMITS.md` | Planetary Systems | Planetary nests as closed-loop register containers; industrial δ injection poisoning and G_local orbital destabilization limits. |

---

## Testing CSE

- `python3 cse_engine.py selftest` checks the engine's formulas against a step-by-step walk of the loop, and against the numbers printed in `CSE_MODEL.txt`.
- `counter_test.c` checks the 32-bit claim on real hardware (2 sign flips per cycle, M plain steps between them, 4,294,967,296 steps per loop).
- `EXAMPLES.md` puts five measurements next to CSE quantities and states each result plainly, including the mismatches.

---

## Support

No support is offered on how to use CSE. The files are complete as published.

## Licence

Free for research, study, teaching, personal and other non-commercial use, under the PolyForm Noncommercial License 1.0.0. See `LICENSE.md`.

Commercial or for-profit use needs a separate licence. To ask for one, open an issue in this repository.

## Contact

Through the Issues section of this repository only.
