# CSE v1.6 — EXAMPLES

Five science placeholders, with the arithmetic shown.

## Read this first

1. These are **placeholders**. A placeholder shows how a measured number can be put next to a CSE quantity. It is not a derivation, not a prediction and not evidence.
2. Every example has the same five parts: the measurement, the CSE quantity, the arithmetic, the result, and what CSE does not explain.
3. The result is stated plainly, including when it does not match. Nothing here was adjusted to fit.
4. **Sizes are not compared.** With Nest 9, Link 1, one loop has a maximum radius of about 3.47 × 10^−26 meters. The observable universe is about 1.27 × 10^52 times larger. CSE v1.6 assigns that loop to a smaller tier. It gives the ratio to the whole-sphere tier for time, and for length only under a postulate (Nest 10, Rules 7 and 8). These examples do not use that postulate, so sizes are not compared. Ratios are.
5. **"Today" comes from Block B.** CSE v1.6 converts Observer 0's age of 13.8 billion years into tick 1,780,693,774 (Block B, row 1.1). In Arc 1 the position equals the tick. This rests on a postulate and a fitted value of Nest 10: alpha inverse as the dilation index, and the conversion ratio 1062.
6. Every CSE number below can be reproduced with `cse_engine.py`.

Symbols: `M = 2,147,483,647`. `s` = position. Bound fraction = `s / M`. Free fraction = `1 − s / M`.

---

## Example 1 — Dark energy

**Measurement.** Dark energy is about 0.685 of the total energy density of the universe today (Planck 2018: 0.6847 ± 0.0073).

**CSE quantity (assumed reading).** The free fraction, `1 − s / M` (Nest 3, Rule 5), at today's position. The reading is an assumption: Nest 3 names the free end "electromagnetic radiation", not dark energy.

**Arithmetic.**

```
Today's position (Block B, row 1.1):   s = 1,780,693,774
check: python3 cse_engine.py position 1780693774
       bound 0.829200, free 0.170800

The position this reading would need:
1 − s / M = 0.685
s = 0.315 × 2,147,483,647 = 676,457,349        (rounded to a whole position)
check: python3 cse_engine.py position 676457349
       bound 0.315000, free 0.685000
check: python3 cse_engine.py order_b 676457349
       5.24 billion dilated years
```

**Result. Mismatch.** CSE gives a free fraction of 0.171 today. The measured dark energy share is 0.685. For the two to agree, today would have to be position 676,457,349, which is 5.24 billion years after the start, not 13.8 billion.

**Direction check: mismatch.** In CSE, Arc 1 is the expansion, and the free fraction falls as the sphere expands. Measurement says the dark energy share rises as the universe expands. Under this reading the two move in opposite directions.

**What CSE does not explain.** Why the value is 0.685. What dark energy is.

---

## Example 2 — Dark matter

**Measurement.** Matter is about 0.315 of the total. Of that, dark matter is about 0.265 and ordinary matter about 0.049 (Planck 2018). Dark matter is about 5.4 times ordinary matter.

**CSE quantity (assumed reading).** The bound fraction, `s / M`, at today's position, the same position as Example 1. Nest 3, Rule 6 places matter at the bound end.

**Arithmetic.**

```
bound fraction at today's position, s = 1,780,693,774:   0.829
measured matter share:                                    0.315

The measured split, written in CSE units:
dark matter:      0.265 × M = 569,083,166 energy units
ordinary matter:  0.049 × M = 105,226,699 energy units
ratio:            0.265 / 0.049 = 5.41
```

**Result. Mismatch.** CSE gives a bound fraction of 0.829 today. The measured matter share is 0.315. This is the mismatch of Example 1 seen from the other side: both examples use one position, and both pairs of numbers add up to 1. The split into 0.265 and 0.049 is **not computable** in CSE v1.6. The units above are the measured fractions written in CSE units.

**Direction check: mismatch.** The same as Example 1, from the other side: in CSE the bound fraction rises during the expansion, and measurement says the matter share falls.

**What CSE does not explain.** The ratio 5.4. Nest 5 defines dense matter pockets and voids but gives no formula for how much bound energy sits in each.

---

## Example 3 — The Hubble tension

**Measurement.** Two methods give two values for the expansion rate today:

```
early-universe method (Planck 2018):        67.4 ± 0.5  km/s/Mpc
local distance ladder (SH0ES 2022):         73.0 ± 1.0  km/s/Mpc
ratio:        73.0 / 67.4 = 1.083
difference:   8.3 %
```

**CSE quantity (assumed reading).** Two measurements by Observer 0, made from different places and moments (Nest 11, Rules 2, 4 and 5), with local time running at different rates (Nest 5, Rules 13 and 14).

**Arithmetic.**

```
If the whole difference came from local time rate:
required rate ratio between the two measurements = 1.083
```

**Result. Not computable.** CSE v1.6 states that local time differs between places. It gives no formula for how much. So CSE cannot produce 1.083 or any other number here. The electromagnetic dilation (Nest 10, Rule 1) does not help: it is one fixed scale, so it cancels in a ratio.

**What CSE does not explain.** The size of the tension. A formula for Nest 5, Rule 13 would be needed first; then this example becomes a real test.

---

## Example 4 — The matter–antimatter imbalance

**Measurement.** The early universe had a very small excess of matter over antimatter. The measured baryon-to-photon ratio is about 6.1 × 10^−10 (Planck 2018).

**CSE quantity (assumed reading).** The 1-unit asymmetry of the signed 32-bit counter. `counter_test.c` shows it: 2,147,483,648 negative values and 2,147,483,647 positive values, one unpaired value in 2^32 states.

**Arithmetic.**

```
1 / 2^32 = 1 / 4,294,967,296 = 2.33 × 10^−10
measured:                      6.1  × 10^−10
measured / CSE = 6.1 × 10^−10 × 4,294,967,296 = 2.62
```

**Result. Mismatch by a factor of 2.6.** The two numbers have the same order of magnitude. They are not equal, and no CSE rule produces the factor 2.6.

**Note.** The asymmetry belongs to the computer tier (two's complement). The CSE cycle itself is symmetric: both poles have one reversal (Nest 0, CYCLE COUNT).

**What CSE does not explain.** The measured value. Until a rule gives the factor, the closeness in order of magnitude is a coincidence and nothing more.

---

## Example 5 — The black hole limit

**Established physics.** A mass `m` inside the radius `r_s = 2 G m / c²` is a black hole (the Schwarzschild radius).

**CSE quantity.** Nest 9, Rules 3 and 7: 1 position = 1.616 × 10^−35 meters. 1 energy unit = 1.956 × 10^9 joules = 2.176 × 10^−8 kilograms.

**Arithmetic.**

```
One energy unit:
  r_s = 2 G m / c² = 2 × 6.674e−11 × 2.176483e−8 / (299,792,458)²
      = 3.2324 × 10^−35 meters
      = 2.000 positions

All M energy units (one full loop):
  mass = M × 2.176483e−8 kg = 46.74 kilograms
  r_s  = 6.94 × 10^−26 meters = 4,294,967,294 positions = 2 × M
  maximum radius of the loop (Pole 1) = M positions
  r_s / maximum radius = 2.000
```

**Result. Exact.** In CSE units the Schwarzschild radius is exactly 2 positions per energy unit. This follows from the definitions in Nests 7 and 9; it is an identity, not a discovery.

**Consequence.** One loop holds M energy units inside a radius that is never larger than M positions. Its Schwarzschild radius is 2 × M positions. So by standard arithmetic the loop stays inside its own Schwarzschild radius for the whole cycle. (2 × M = 4,294,967,294 is also the TRANSITION COUNT, because both are 2 × M.)

**Tier.** CSE v1.6 assigns the loop measured in Planck lengths to a smaller tier (Nest 10, Rule 8). The meters and kilograms above belong to that tier. If the same three unit steps hold on the whole-sphere tier, the identity carries over unchanged, because it is stated in positions and energy units. CSE v1.6 postulates this for length and time (Nest 10, Rule 7). It does not state the energy step of the whole-sphere tier.

**Reading.** Nest 1 says nothing leaves the Root Container. A region inside its own Schwarzschild radius is one that nothing leaves. The two statements agree. CSE does not contain general relativity, so this is a reading, not a result.

**What CSE does not explain.** Whether the agreement means anything. Gravity itself.

---

## Summary

| # | Placeholder | Result |
|---|---|---|
| 1 | Dark energy | Mismatch: CSE free fraction 0.171 today, measured 0.685. Direction check: mismatch. |
| 2 | Dark matter | Mismatch: CSE bound fraction 0.829 today, measured 0.315. Split: not computable. Direction check: mismatch. |
| 3 | Hubble tension | Not computable. A formula for local time is missing. |
| 4 | Matter–antimatter imbalance | Same order of magnitude. Mismatch by a factor of 2.6. |
| 5 | Black hole limit | Exact identity: 2 positions per energy unit. |

These results are part of the open testing of CSE. A model is tested by the cases where it fails as much as by the cases where it fits.
