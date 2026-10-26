# Canonical Substrate Engine (CSE) v1.9

A deterministic closed-loop logic model with a 2^32 cycle and an executable Python engine.

## A Note from the Author

1. **Built in Logic Isolation:** This model was developed in complete isolation from outside academic bias, groupthink, or mainstream theoretical trends.
2. **Empiricals as Checksums:** Because it was built in isolation, real-world scientific empiricals were never used as input knobs to curve-fit the model; instead, they were used strictly as external *checksums* to test if the closed-loop logic held true.
3. **Pure Primitives & Zero Tolerance for Handwaving:** It is constructed entirely on bare logic, integer numbers, finites, arithmetic, and polarity change. Numerology, mysticism, and handwaving were aggressively purged; in a strict closed-loop system, ungrounded assumptions immediately break the math.
4. **Tri-Domain Architecture:** It draws its framework from Computer Science (CS), Electrical Engineering (EE), and Natural System Mechanics.
5. **Completely Open (No Black Boxes):** There are no hidden variables, mysterious force fields, multiverses for anything to leak in or out, extra-dimensions, science fiction analogies/tropes, or black-box abstractions. Everything is wide open and transparent.
6. **Cross-Disciplinary Bridge:** Specialists (such as medical doctors, biologists, or astrophysicists) may encounter unfamiliar terminology rooted in CS and EE primitives. An open mind across domains is essential to see how disparate systems map to discrete register states.
7. **Not a Physics Model:** This is a discrete computational and systems architecture—not a traditional physics model. I am not offering a new interpretation of spacetime or quantum mechanics; I am providing a closed-loop arithmetic framework. It is up to physicists or domain experts to test the register arithmetic and determine how it maps to their fields, if they choose to do so.
8. **Not a Theory of Everything:** I do not claim this is a definitive Theory of Everything, but others are welcome to explore, test, and stress-test it as one.
9. **Reverse-Engineering Pattern Match:** This is not proposed as the ultimate, absolute "true nature" of the universe. It is a reverse-engineered pattern-matching model framed intentionally in CS, EE, and systems terms.
10. **Radical Simplicity:** It has been kept as simple and transparent as possible so that any reasonably logical and mathematically gifted mind can grasp its mechanics from the ground up.
11. **Independent Analytical Utility:** The computational logic, state architecture, and closure principles presented in CSE may be examined as an analytical methodology in their own right, independently of any proposed physical interpretation. Researchers are invited to test the methodology's utility, identify its limitations, and develop applications where appropriate.
12. **Universal Read-Only Memory (UROM) Architecture:** The Root Container is a strictly read-only execution environment (UROM). There are no write-heads, dynamic memory allocations outside pre-compiled boundaries, or root privileges. Observers and subnets run as immutable diagnostic subroutines; state transitions and error corrections operate strictly via local buffer/register adjustments (δ), never by flashing the master ROM.

*Break it, test it, or build upon it—the ledger is open.*

**Version note.** The model text and the engine are at v1.9. `cse_ai_example.py`, `counter_test.c` and `EXAMPLES.md` are still at v1.3 and have not been updated. The nest numbers changed from v1.3: see "Changed in v1.6".

---

## What CSE is

CSE is a logic model written in three sections that are chained together. A number is stated in one section only, and the other sections refer to it.

1. **Substrate.** Counts only: whole numbers of positions, transitions, ticks and energy units. No meters, no seconds.
2. **Conversion bridge.** The rates and ratios that join the counts to human units.
3. **Observer 0.** The observers, their units, their inputs and their readings.

| Part | Section | Subject | In one line |
|---|---|---|---|
| Global definitions | 1 | Definitions | Counts, position, transition, phase, reversal, tick. |
| 0 | 1 | Space | A 4-state closed loop: count up from 0 to M, reverse, count back to 0, reverse. |
| 1 | 1 | Energy | Total energy = 1, always. As the space count rises, free energy becomes bound. |
| 2 | 1 | Time | Two arcs per cycle. Time never reverses; only the expansion does. Time rate has finite bounds, [0, background] (Rule 11). |
| 3 | 1 | Energy spectrum | Each position has a bound and a free fraction: `s / M` and `1 − s / M`. Three descriptive regime labels (Rule 7). |
| 4 | 1 | Sphere | The loop is a sphere. Its shell moves 1 position per transition. The positions do not stretch. |
| 5 | 1 | Energy waves | Dense matter pockets and voids. They always balance. The inside follows the shell's turn late. The room for gravity shrinks to 0 at the turn. Local rate is 1 where local bound equals the whole-sphere value (Rule 19). |
| 6 | 1 | Closure | The loop resets and starts again. Nothing runs away. |
| 7 | 1 | Steps | The unit steps, the constants c, ħ and G, and the mass unit are each exactly 1. Tiers. |
| 8 | 2 | Bridge | Where the model meets computer science, physics and cosmology. Order A and Order B. |
| 9 | 2 | Master chain | Substrate steps to meters, seconds and joules, using ħ, c and G. |
| 10 | 2 | Second chain | Electromagnetic dilation, ticks to Observer 0 years, and the tier ratio. |
| 11 | 3 | Observers | Observer 0 measures. Observer 1 works out the logic. Time is unidirectional; space/length is locked (Rule 5). |
| 12 | 3 | Self-similarity | A computer is a smaller tier. The 32-bit register repeats the template. Tiers differ only in the arithmetic that rebalances dependencies (Rule 6). |
| 13 | 3 | Radiation and ledger correction | c_local, the hardware basis, and stop-limit dynamics (Rule 11). |
| Block A | 3 | Inputs | Observer 0's estimates, and c, ħ and G in human units. |
| Block B | 3 | Second-chain results | Current age, lifespan and turning point, in dilated years, undilated years and ticks. |
| Block C | 3 | Master-chain check | c, ħ and G return 1 in substrate units. |

The numbers of the model:

```
M               = 2^31 − 1 = 2,147,483,647      the limit
positions       = 2^31     = 2,147,483,648      0 to M
cycle count     = 2^32     = 4,294,967,296      1 + M + 1 + M
ticks           = 2^32 − 1 = 4,294,967,295      M + 1 + M advances of the runtime counter
transitions     = 2^32 − 2 = 4,294,967,294      the 2 reversals are not transitions
```

The full text is in `CSE_MODEL.txt`.

---

## Research Hypotheses Corpus

As an extension of the Canonical Substrate Engine, a series of exploratory research whitepapers has been compiled in this repository.

**Important Disclaimer:** *These documents are all working hypotheses that researchers can explore, think about, and test themselves. They are not established science; they represent speculative extensions of the CSE v1.9 discrete register mechanics into cosmology, oncology, longevity, and astrobiology. It is entirely up to researchers to evaluate, falsify, or build upon them.*

The complete index and individual whitepapers are detailed below:

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

## Files

| File | Version | What it is |
|---|---|---|
| `CSE_MODEL.txt` | v1.9 | The model: three sections, Nests 0 to 13, Blocks A to D. Also usable as a prompt. |
| `cse_engine.py` | v1.9 | The model in executable form. Standard library only. |
| `cse_ai_example.py` | v1.9 | How to wire the engine into an AI system, with comments at every wire point. |
| `counter_test.c` | v1.3 | A real 32-bit counter, run through one full loop. |
| `EXAMPLES.md` | v1.3 | Five science placeholders with the arithmetic shown. Its numbers use the v1.3 ratio, 1052. |
| `LICENSE.md` | | PolyForm Noncommercial 1.0.0. |

---

## Quick start

```
python3 cse_engine.py selftest             # checks the engine against the model
python3 cse_engine.py totals               # counts, both chains, tier ratio, constants, v1.9 rule summaries
python3 cse_engine.py state 2147483649    # state after one counted operation
python3 cse_engine.py position 1000       # energy at one position
python3 cse_engine.py local 0.75 1000     # dense matter pocket or void
python3 cse_engine.py regime 0.75 1000    # below / at / above equilibrium label (v1.9)
python3 cse_engine.py rate 0.75 1000      # local time rate direction (v1.9)
python3 cse_engine.py lag 1000            # minimum turn lag at one radius
python3 cse_engine.py room 1000           # room for gravity at one position
python3 cse_engine.py order_a 13.8e9      # Observer 0 years -> ticks
python3 cse_engine.py order_b 4294967295  # ticks -> Observer 0 years
python3 cse_engine.py appendix_a          # Block B: the second-chain results
python3 cse_engine.py block_d             # Block D: Tests 1 to 5
python3 cse_engine.py alpha 0.036         # alpha stack at one delta
python3 cse_engine.py constants           # the three steps and the three constants, in words
python3 cse_engine.py steps planck_length # the order of operations for one name
python3 cse_engine.py reckon 3 + 4 x 2    # exact arithmetic, with the steps shown

python3 cse_ai_example.py                 # shows what an LLM would receive

gcc -O2 -o counter_test counter_test.c && ./counter_test
```

Every engine command prints JSON. The engine also imports as a module: `import cse_engine as cse`.

---

## Using CSE with an AI

There are two ways. They can be combined.

**1. As a prompt.** Put the text of `CSE_MODEL.txt` into the system prompt of any AI. The AI can then discuss the model and reason inside its rules.

**2. As an engine.** Run `cse_engine.py` beside the AI and pass its results to the AI on every turn. `cse_ai_example.py` shows each wire point.

If you integrate CSE into your own AI:

1. **Use the LLM as a translator only.** The engine computes. The LLM puts the engine's results into words. Do not let the LLM compute, round or guess engine values.
2. **Customize your prompt for your own target field.** CSE gives the structure. Your prompt gives the voice and the subject.
3. **Add your own tiers.** Any closed cycle in your field can be mapped onto the engine as a fraction from 0 to 1. The example file maps a day and a year.

What the engine computes: the cycle and the tick, the state at any counted operation, the energy fractions, the pocket-or-void test, the regime label, the local-rate direction, the minimum turn lag, the room for gravity, the master chain (Nest 9), both orders of the second chain and the tier ratio (Nest 10), the results of Block B, and the constants of Block C. From v1.9, `totals` also returns the time-rate bounds (Nest 2 Rule 11) and the stop-limit statement (Nest 13 Rule 11).

What the engine does not compute: anything the model gives no formula for. See "Known open points".

The engine prints full arithmetic values. Block B shows the same values cut at the certainty limit of alpha inverse.

---

## Testing CSE

- `selftest` checks the engine's formulas against a step-by-step walk of the loop, and checks the engine's results against the numbers printed in `CSE_MODEL.txt`: Block B, the master chain and the tier ratio. From v1.9 it also checks the new rule statements (Nest 2 Rule 11, Nest 3 Rule 7, Nest 5 Rule 19, Nest 11 Rule 5, Nest 12 Rule 6, Nest 13 Rule 11).
- `counter_test.c` checks the claim of Nest 12 on a real machine: 2 sign flips per cycle, M plain steps between them, 4,294,967,296 steps in the loop, and a highest counter value of 4,294,967,295.
- `EXAMPLES.md` puts five measurements next to CSE quantities and states each result plainly, including the mismatches.
- Block B gives every value of the second chain in all three stages, and `steps` shows every line of the master chain, so each can be checked with a calculator.

Any reasonably skilled researcher or computer programmer should be able to test CSE and use it to its full advantage.

---

## Known open points

These are stated here so that nobody has to find them the hard way.

1. **Scale.** With Nest 9, Link 1 (1 position = 1 Planck length), one loop has a maximum radius of about 3.47 × 10^−26 meters, one arc lasts about 1.16 × 10^−34 seconds, and the total energy is about 4.2 × 10^18 joules. The model assigns this loop to a smaller tier. It gives the ratio to the whole-sphere tier for time, and for length under a postulate (Nest 10, Rules 7 and 8). The size of one energy unit on the whole-sphere tier is not stated.
2. **Missing formulas.** The model states, but gives no formula for: local time (Nest 5, Rules 13, 14, 18 and 19), the amount of drift from the reversal (Nest 5, Rule 9), how bound energy is divided between pockets and voids, how gravity changes with distance (Nest 5, Rule 11), and the size of the turn lag (Nest 5, Rule 15), for which it gives only a range. The value at any one place is outside the model's scope: Observer 0 finds it by measurement (Nest 5, Rule 17).
3. **The axiom.** M = 2^31 − 1 is declared as an axiom (Nest 7, Rule 1). The match with the 32-bit register (Nest 12, Rules 4 and 5) is stated, not derived.
4. **Statements.** Nests 8, 11 and 12 are statements. They are not calculations, and the engine does not compute them.
5. **Energy shares.** Under the simplest reading, CSE's bound and free fractions today, 0.829 and 0.171, do not match the measured matter and dark energy shares, 0.315 and 0.685. They also move in the opposite direction as the sphere expands. See `EXAMPLES.md`, Examples 1 and 2.
6. **Postulates and fitted values.** Alpha inverse as the dilation index, the whole-number conversion ratio, and the whole-sphere position are postulates (Nest 10, Rules 1, 4 and 7). The value 1062 is fitted: it was found by dividing Observer 0's lifespan estimate by the total runtime, and the whole number was kept. That estimate is certain to about 3 digits, so the division alone fixes the ratio only between about 1060 and 1064.
7. **The tier ratio is not derived.** It is found by dividing one tick by one Planck time, and the Planck time is built from the measured G. The substrate does not yet give this ratio from M alone (Nest 10, Rule 8).
8. **Nothing here derives ħ, G or c.** In substrate units each is exactly 1. Their human-unit values state the size of human units, and only pure ratios are open to derivation (Nest 9, Rule 5).
9. **Consistency checks, not confirmations.** The corrected lifespan in Block B is within 0.05% of Observer 0's estimate, but the 1062 came from that estimate. The constants in Block C return 1 by construction. The check tables of the engine's `steps` command return the Planck length, the Planck time and c by construction. The model and the engine say so.
10. **Open test.** No second measured value has yet been converted with the same alpha inverse and the same 1062 and compared with Observer 0's own number (Block B, line 3.9).
11. **Turning point.** CSE turns the shell at 50% of the runtime. Observer 0's model puts the turning point at about 74.5%. Block B reads the difference as a lag, and its size is fitted from Observer 0's input, not derived (Block B, rows 1.6 to 1.8 and line 3.11).
12. **The turn and the lag.** At the turn the room for gravity is 0, so the sphere has no dense matter pockets and no voids at that moment (Nest 5, Rule 16). The turn lag is read as the turn reaching a place late. How a place persists through the turn is not stated.
13. **Location.** The model does not state where Observer 0 is inside the sphere.
14. **Least settled.** Section 2 (Nests 9 and 10) and Blocks A to D are the least settled parts of v1.9.

---

## Support

No support is offered on how to use CSE. The files are complete as published.

## Licence

Free for research, study, teaching, personal and other non-commercial use, under the PolyForm Noncommercial License 1.0.0. See `LICENSE.md`.

Commercial or for-profit use needs a separate licence. To ask for one, open an issue in this repository.

## Contact

Through the Issues section of this repository only.
