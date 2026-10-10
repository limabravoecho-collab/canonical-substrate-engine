# Canonical Substrate Engine (CSE) v1.6

A deterministic closed-loop logic model with a 2^32 cycle and an executable Python engine.

**Status.** CSE is a model for study. The author does not claim that it is a theory of everything. It is published completely open for testing as one.

**Version note.** The model text and the engine are at v1.6. `cse_ai_example.py`, `counter_test.c` and `EXAMPLES.md` are still at v1.3 and have not been updated to v1.6. The nest numbers changed from v1.3: see "Changed in v1.6".

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
| 2 | 1 | Time | Two arcs per cycle. Time never reverses; only the expansion does. |
| 3 | 1 | Energy spectrum | Each position has a bound and a free fraction: `s / M` and `1 − s / M`. |
| 4 | 1 | Sphere | The loop is a sphere. Its shell moves 1 position per transition. The positions do not stretch. |
| 5 | 1 | Energy waves | Dense matter pockets and voids. They always balance. The inside follows the shell's turn late. The room for gravity shrinks to 0 at the turn. |
| 6 | 1 | Closure | The loop resets and starts again. Nothing runs away. |
| 7 | 1 | Steps | The unit steps, the constants c, ħ and G, and the mass unit are each exactly 1. Tiers. |
| 8 | 2 | Bridge | Where the model meets computer science, physics and cosmology. Order A and Order B. |
| 9 | 2 | Master chain | Substrate steps to meters, seconds and joules, using ħ, c and G. |
| 10 | 2 | Second chain | Electromagnetic dilation, ticks to Observer 0 years, and the tier ratio. |
| 11 | 3 | Observers | Observer 0 measures. Observer 1 works out the logic. |
| 12 | 3 | Self-similarity | A computer is a smaller tier. The 32-bit register repeats the template. |
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

## Changed in v1.6

**Structure**

- **Three sections.** The model text is now ordered as Substrate, Conversion bridge, Observer 0. The two appendices of v1.3 are gone: their content is in Nests 7 to 10 and Blocks A to C.
- **One place.** Each number and each definition is stated in one section only.
- **Nest numbers changed.** Nests 0 to 5 keep their numbers. The others moved:

| v1.3 | v1.6 |
|---|---|
| Nest 6 (Observers) | Nest 11 |
| Nest 7 (Bridge) | Nest 8 |
| Nest 8 (Conversions) | Nest 7 (unit steps and constants), Nest 9 (master chain), Nest 10 (second chain, tier ratio) |
| Nest 9 (Closure) | Nest 6 |
| Nest 10 (Self-similarity) | Nest 12. Tiers are defined in Nest 7, Rule 7 |
| Appendix A | Nest 10, Block A, Block B |
| Appendix B | Nests 7, 8 and 10, Block C |

**Numbers**

- **Lifespan input.** Observer 0's lifespan estimate is now ~33.3 billion years (was ~33). It is the same estimate that the turning point input uses.
- **Conversion ratio.** 1 tick = 1062 undilated years (was 1052). Every second-chain value is recomputed.
- **Tier ratio.** One tick ≈ 4.536 × 10^51 Planck times (was 4.494 × 10^51).
- **G.** The model and the engine both use G = 6.674 × 10^−11, certain to 4 digits.

**New rules**

- **Counts.** Everything in the substrate is a count. Measurement units begin at the conversion bridge (Global definitions).
- **Tick count.** Arc 1 = M ticks, the reversal at the turn = 1 tick, Arc 2 = M ticks (Nest 2, Rule 10).
- **Inert positions.** The shell is the outer edge of the energy. The energy travels across the positions. The positions do not move or stretch (Nest 4, Rule 3).
- **Constant velocity.** The shell moves exactly 1 position per transition, in both arcs (Nest 4, Rule 10).
- **Room for gravity.** The excess that drives gravity is at most the free fraction, `1 − s / M`. It is 0 at the turn (Nest 5, Rule 16).
- **Local values.** The substrate fixes the limits and the balance. It does not fix the value at any one place (Nest 5, Rule 17).
- **Mass unit.** 1 mass unit = 1 energy unit / c^2 = exactly 1 (Nest 7, Rule 4).
- **Whole-sphere position.** A postulate: 1 position on the whole-sphere tier = the distance light covers in 1 tick = 7.749788... light-years (Nest 10, Rule 7).

**Engine**

- **New command.** `room`: the room for gravity at one position.
- **Order of operations.** `steps` returns the standard arithmetic, the substrate form, and a check from the whole-sphere tier for the Planck length, the Planck time and c. Every row is worked from the values the rows above it show, and carries its units and the source of each input.
- **Renamed output (breaking change from v1.3).** In `totals`, `appendix_b` is now `block_c`. In `appendix_a`, `origin_of_1052` is now `origin_of_1062`.
- **Kept names.** The command `appendix_a` and the functions `nest8_facts` and `nest8_steps` keep their v1.3 names. They now serve Block B and Nests 7, 9 and 10.
- **Self-test.** 16 checks (was 12).

---

## Files

| File | Version | What it is |
|---|---|---|
| `CSE_MODEL.txt` | v1.6 | The model: three sections, Nests 0 to 12, Blocks A to C. Also usable as a prompt. |
| `cse_engine.py` | v1.6 | The model in executable form. Standard library only. |
| `cse_ai_example.py` | v1.3 | How to wire the engine into an AI system, with comments at every wire point. |
| `counter_test.c` | v1.3 | A real 32-bit counter, run through one full loop. |
| `EXAMPLES.md` | v1.3 | Five science placeholders with the arithmetic shown. Its numbers use the v1.3 ratio, 1052. |
| `LICENSE.md` | | PolyForm Noncommercial 1.0.0. |

---

## Quick start

```
python3 cse_engine.py selftest            # checks the engine against the model
python3 cse_engine.py totals              # counts, both chains, tier ratio, constants
python3 cse_engine.py state 2147483649    # state after one counted operation
python3 cse_engine.py position 1000       # energy at one position
python3 cse_engine.py local 0.75 1000     # dense matter pocket or void
python3 cse_engine.py lag 1000            # minimum turn lag at one radius
python3 cse_engine.py room 1000           # room for gravity at one position
python3 cse_engine.py order_a 13.8e9      # Observer 0 years -> ticks
python3 cse_engine.py order_b 4294967295  # ticks -> Observer 0 years
python3 cse_engine.py appendix_a          # Block B: the second-chain results
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

What the engine computes: the cycle and the tick, the state at any counted operation, the energy fractions, the pocket-or-void test, the minimum turn lag, the room for gravity, the master chain (Nest 9), both orders of the second chain and the tier ratio (Nest 10), the results of Block B, and the constants of Block C.

What the engine does not compute: anything the model gives no formula for. See "Known open points".

The engine prints full arithmetic values. Block B shows the same values cut at the certainty limit of alpha inverse.

---

## Testing CSE

- `selftest` checks the engine's formulas against a step-by-step walk of the loop, and checks the engine's results against the numbers printed in `CSE_MODEL.txt`: Block B, the master chain and the tier ratio.
- `counter_test.c` checks the claim of Nest 12 on a real machine: 2 sign flips per cycle, M plain steps between them, 4,294,967,296 steps in the loop, and a highest counter value of 4,294,967,295.
- `EXAMPLES.md` puts five measurements next to CSE quantities and states each result plainly, including the mismatches.
- Block B gives every value of the second chain in all three stages, and `steps` shows every line of the master chain, so each can be checked with a calculator.

Any reasonably skilled researcher or computer programmer should be able to test CSE and use it to its full advantage.

---

## Known open points

These are stated here so that nobody has to find them the hard way.

1. **Scale.** With Nest 9, Link 1 (1 position = 1 Planck length), one loop has a maximum radius of about 3.47 × 10^−26 meters, one arc lasts about 1.16 × 10^−34 seconds, and the total energy is about 4.2 × 10^18 joules. The model assigns this loop to a smaller tier. It gives the ratio to the whole-sphere tier for time, and for length under a postulate (Nest 10, Rules 7 and 8). The size of one energy unit on the whole-sphere tier is not stated.
2. **Missing formulas.** The model states, but gives no formula for: local time (Nest 5, Rules 13 and 14), the amount of drift from the reversal (Nest 5, Rule 9), how bound energy is divided between pockets and voids, how gravity changes with distance (Nest 5, Rule 11), and the size of the turn lag (Nest 5, Rule 15), for which it gives only a range. The value at any one place is outside the model's scope: Observer 0 finds it by measurement (Nest 5, Rule 17).
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
14. **Least settled.** Section 2 (Nests 9 and 10) and Blocks A to C are the least settled parts of v1.6.

---

## Support

No support is offered on how to use CSE. The files are complete as published.

## Licence

Free for research, study, teaching, personal and other non-commercial use, under the PolyForm Noncommercial License 1.0.0. See `LICENSE.md`.

Commercial or for-profit use needs a separate licence. To ask for one, open an issue in this repository.

## Contact

Through the Issues section of this repository only.
