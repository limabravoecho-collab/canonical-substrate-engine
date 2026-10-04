# Canonical Substrate Engine (CSE) v1.3

A deterministic closed-loop logic model with a 2^32 cycle and an executable Python engine.

**Status.** CSE is a model for study. The author does not claim that it is a theory of everything. It is published completely open for testing as one.

**Version note.** Only `CSE_MODEL.txt` is at v1.3. The engine, the AI example, the counter test and `EXAMPLES.md` are still at v1.0 and do not yet cover what v1.3 added.

---

## What CSE is

CSE is a logic model written as a header, 11 short sections called nests, and two appendices. Each nest builds on the nests before it.

| Part | Subject | In one line |
|---|---|---|
| Header | Definitions | Position, transition, phase, reversal, tick, and the three counts. |
| 0 | Space | A 4-state closed loop: count up from 0 to M, reverse, count back to 0, reverse. |
| 1 | Energy | Total energy = 1, always. As space grows, free energy becomes bound. |
| 2 | Time | Two arcs per cycle. Time never reverses; only the expansion does. |
| 3 | Energy spectrum | Each position has a bound and a free fraction: `s / M` and `1 − s / M`. |
| 4 | Sphere | The loop is a sphere that expands from its centre and returns. |
| 5 | Energy waves | Dense matter pockets and voids inside the sphere. They always balance. The inside follows the shell's turn late. |
| 6 | Observers | Observer 0 measures. Observer 1 works out the logic. Electromagnetic dilation is defined here. |
| 7 | Bridge | Where the model meets computer science, physics and cosmology. |
| 8 | Conversions | One chain from substrate units to meters, seconds and joules, using ħ, c and G. A second chain and a tier ratio are added. |
| 9 | Closure | The loop resets and starts again. Nothing runs away. |
| 10 | Self-similarity | The same template on every tier. The 32-bit register repeats it. |
| Appendix A | Conversion Block | Ticks to Observer 0 years. Current age, lifespan and turning point, with every line of arithmetic shown. |
| Appendix B | Master Chain Block | The Nest 8 chain followed in both directions. In the substrate, c = ħ = G = 1. |

The numbers of the model:

```
M               = 2^31 − 1 = 2,147,483,647      the limit
positions       = 2^31     = 2,147,483,648      0 to M
cycle count     = 2^32     = 4,294,967,296      1 + M + 1 + M
ticks           = 2^32 − 1 = 4,294,967,295      advances of the runtime counter
transitions     = 2^32 − 2 = 4,294,967,294      the 2 reversals are not transitions
```

The full text is in `CSE_MODEL.txt`.

---

## Added to the model text in v1.3

- **Tick.** One advance of the 32-bit runtime counter. Total runtime = 2^32 − 1 ticks per cycle (Header; Nest 2, Rule 9).
- **Turn lag.** The shell turns at maximum expansion. The inside of the sphere follows late, because nothing moves more than 1 position in 1 transition (Nest 5, Rule 15).
- **Electromagnetic dilation.** A scale on Observer 0's measurements of time, with alpha inverse as its index (Nest 6, Rule 8).
- **Second chain and tier ratio.** The tick is the step of the whole-sphere tier. The Planck-time transition is the step of a smaller tier. One tick ≈ 4.494 × 10^51 Planck times (Nest 8, Rules 11 to 13).
- **Appendix A.** `ticks = (Observer 0 years × alpha inverse) / 1052`, with the arithmetic for the current age, the lifespan and the turning point.
- **Appendix B.** The master chain in both directions, and how the dilation carries into units built from seconds.
- **Plain text.** The model text no longer uses math markup. Powers are written with `^`.

---

## Files

| File | Version | What it is |
|---|---|---|
| `CSE_MODEL.txt` | v1.3 | The model: header, Nests 0 to 10, Appendix A and Appendix B. Also usable as a prompt. |
| `cse_engine.py` | v1.0 | The model in executable form. Standard library only. |
| `cse_ai_example.py` | v1.0 | How to wire the engine into an AI system, with comments at every wire point. |
| `counter_test.c` | v1.0 | A real signed 32-bit counter, run through one full loop. |
| `EXAMPLES.md` | v1.0 | Five science placeholders with the arithmetic shown. |
| `LICENSE.md` | | PolyForm Noncommercial 1.0.0. |

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

What the engine computes: the cycle, the state at any counted operation, the energy fractions, the pocket-or-void test, and the Nest 8 master chain conversions.

What the engine does not compute: anything the model gives no formula for (see "Known open points"), and anything added in v1.3: ticks, Appendix A, Appendix B, the tier ratio and the turn lag.

---

## Testing CSE

- `selftest` checks the engine's formulas against a step-by-step walk of the loop.
- `counter_test.c` checks the claim of Nest 10 on a real machine: 2 sign flips per cycle, M plain steps between them, 4,294,967,296 steps in the loop.
- `EXAMPLES.md` puts five measurements next to CSE quantities and states each result plainly, including the mismatches.
- Appendix A and Appendix B show every line of their arithmetic, so each can be checked with a calculator.

Any reasonably skilled researcher or computer programmer should be able to test CSE and use it to its full advantage.

---

## Known open points

These are stated here so that nobody has to find them the hard way.

1. **Scale.** With Nest 8, Link 1 (1 position = 1 Planck length), one loop has a maximum radius of about 3.47 × 10^−26 meters, one arc lasts about 1.16 × 10^−34 seconds, and the total energy is about 4.2 × 10^18 joules. v1.3 assigns this loop to a smaller tier and gives the ratio to the whole-sphere tier for time only (Nest 8, Rule 12). The size of one position and one energy unit on the whole-sphere tier is not stated.
2. **Missing formulas.** The model states, but gives no formula for: local time (Nest 5, Rules 13 and 14), the amount of drift from the reversal (Nest 5, Rule 9), how bound energy is divided between pockets and voids, and the size of the turn lag (Nest 5, Rule 15), for which it gives only a range.
3. **The axiom.** M = 2^31 − 1 is declared as an axiom (Nest 8, Rule 1). The match with the 32-bit register (Nest 10, Rules 4 and 5) is stated, not derived.
4. **Statements.** Nests 6, 7 and 10 are statements. They are not calculations, and the engine does not compute them.
5. **Direction check.** Under the simplest reading, CSE's energy fractions move in the opposite direction to the measured dark energy and matter shares. See `EXAMPLES.md`, Examples 1 and 2.
6. **Postulates in Appendix A.** Alpha inverse as the dilation index, and the conversion ratio 1052, are postulates. The 1052 was found by dividing Observer 0's lifespan estimate by the total runtime, and the whole number was kept. The tier ratio in Nest 8, Rule 12 is also a stated ratio, not derived from M.
7. **Consistency checks, not confirmations.** The corrected lifespan in Appendix A is within 0.09% of Observer 0's estimate, but the 1052 came from that estimate. The constants in Appendix B return 1 by construction. Both appendices say so.
8. **Open test.** No second measured value has yet been converted with the same alpha inverse and the same 1052 and compared with Observer 0's own number (Appendix A, line 13.9).
9. **Turning point.** CSE turns the shell at 50% of the runtime. Observer 0's model puts the turning point at about 75%. Appendix A reads the difference as a lag, and its size is fitted from Observer 0's input, not derived (Appendix A, item 14).
10. **Location.** The model does not state where Observer 0 is inside the sphere.
11. **Least settled.** Nest 8 and the two appendices are the least settled parts of v1.3.

---

## Support

No support is offered on how to use CSE. The files are complete as published.

## Licence

Free for research, study, teaching, personal and other non-commercial use, under the PolyForm Noncommercial License 1.0.0. See `LICENSE.md`.

Commercial or for-profit use needs a separate licence. To ask for one, open an issue in this repository.

## Contact

Through the Issues section of this repository only.
