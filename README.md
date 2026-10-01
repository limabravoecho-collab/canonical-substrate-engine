# Canonical Substrate Engine (CSE) v1.0

A deterministic closed-loop logic model with a 2^32 cycle and an executable Python engine.

**Status.** CSE is a model for study. The author does not claim that it is a theory of everything. It is published completely open for testing as one.

---

## What CSE is

CSE is a logic model written as a header and 11 short sections called nests. Each nest builds on the nests before it.

| Nest | Subject | In one line |
|---|---|---|
| Header | Definitions | Position, transition, phase, reversal, the two counts. |
| 0 | Space | A 4-state closed loop: count up from 0 to M, reverse, count back to 0, reverse. |
| 1 | Energy | Total energy = 1, always. Space compresses energy. |
| 2 | Time | Two arcs per cycle. Time never reverses; only the expansion does. |
| 3 | Energy spectrum | Each position has a compressed and an uncompressed fraction: `s / M` and `1 − s / M`. |
| 4 | Sphere | The loop is a sphere that expands from its centre and returns. |
| 5 | Energy waves | Dense matter pockets and voids inside the sphere. They always balance. |
| 6 | Observers | Observer 0 measures. Observer 1 works out the logic. |
| 7 | Bridge | Where the model meets computer science, physics and cosmology. |
| 8 | Conversions | One chain from substrate units to meters, seconds and joules, using ħ, c and G. |
| 9 | Closure | The loop resets and starts again. Nothing runs away. |
| 10 | Self-similarity | The same template on every tier. The 32-bit register repeats it. |

The numbers of the model:

```
M               = 2^31 − 1 = 2,147,483,647      the limit
positions       = 2^31     = 2,147,483,648      0 to M
cycle count     = 2^32     = 4,294,967,296      1 + M + 1 + M
transitions     = 2^32 − 2 = 4,294,967,294      the 2 reversals are not transitions
```

The full text is in `CSE_MODEL.txt`.

---

## Files

| File | What it is |
|---|---|
| `CSE_MODEL.txt` | The model: header and Nests 0 to 10. Also usable as a prompt. |
| `cse_engine.py` | The model in executable form. Standard library only. |
| `cse_ai_example.py` | How to wire the engine into an AI system, with comments at every wire point. |
| `counter_test.c` | A real signed 32-bit counter, run through one full loop. |
| `EXAMPLES.md` | Five science placeholders with the arithmetic shown. |
| `LICENSE.md` | PolyForm Noncommercial 1.0.0. |

---

## Quick start

```
python3 cse_engine.py selftest            # checks the engine against the model
python3 cse_engine.py totals              # counts, conversions, whole-sphere values
python3 cse_engine.py state 2147483649    # state after one counted operation
python3 cse_engine.py position 1000       # energy at one position
python3 cse_engine.py local 0.75 1000     # dense matter pocket or void

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

What the engine computes: the cycle, the state at any counted operation, the energy fractions, the pocket-or-void test, and the Nest 8 conversions.

What the engine does not compute: anything the model gives no formula for. See "Known open points".

---

## Testing CSE

- `selftest` checks the engine's formulas against a step-by-step walk of the loop.
- `counter_test.c` checks the claim of Nest 10 on a real machine: 2 sign flips per cycle, M plain steps between them, 4,294,967,296 steps in the loop.
- `EXAMPLES.md` puts five measurements next to CSE quantities and states each result plainly, including the mismatches.

Any reasonably skilled researcher or computer programmer should be able to test CSE and use it to its full advantage.

---

## Known open points

These are stated here so that nobody has to find them the hard way.

1. **Scale.** With Nest 8, Link 1 (1 position = 1 Planck length), the whole sphere has a maximum radius of about 3.47 × 10^−26 meters, one arc lasts about 1.16 × 10^−34 seconds, and the total energy is about 4.2 × 10^18 joules. The scale between tiers is not defined in v1.0.
2. **Missing formulas.** The model states, but gives no formula for: local time (Nest 5, Rules 10 and 11), the amount of drift from the reversal (Nest 5, Rule 9), and how compressed energy is divided between pockets and voids.
3. **The axiom.** M = 2^31 − 1 is declared as an axiom (Nest 8, Rule 1). The match with the 32-bit register (Nest 10, Rules 4 and 5) is stated, not derived.
4. **Statements.** Nests 6, 7 and 10 are statements. They are not calculations, and the engine does not compute them.
5. **Direction check.** Under the simplest reading, CSE's energy fractions move in the opposite direction to the measured dark energy and matter shares. See `EXAMPLES.md`, Examples 1 and 2.
6. **Nest 8** is the least settled nest in v1.0.

---

## Support

No support is offered on how to use CSE. The files are complete as published.

## Licence

Free for research, study, teaching, personal and other non-commercial use, under the PolyForm Noncommercial License 1.0.0. See `LICENSE.md`.

Commercial or for-profit use needs a separate licence. To ask for one, open an issue in this repository.

## Contact

Through the Issues section of this repository only.
