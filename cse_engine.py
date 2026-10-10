#!/usr/bin/env python3
"""
cse_engine.py - Canonical Substrate Engine (CSE) v1.6
A Deterministic Cosmological Logic Model, in executable form.

This file computes only what the model defines with a number or a formula.

SECTION 1, SUBSTRATE (counts only)
  Global definitions + Nest 0 : the closed cycle of 4,294,967,296 counted operations, and the tick
  Nest 1 + Nest 3 : bound / free energy at a position
  Nest 2          : phase (arc), time points 0, 1, 2, the total runtime, the tick count (Rule 10)
  Nest 4          : radius, poles, and the constant velocity of the shell (Rule 10)
  Nest 5          : dense matter pocket / void test (Rules 2, 4, 5), turn lag (Rule 15),
                    room for gravity (Rule 16)
  Nest 7          : the unit steps, the constants and the mass unit, each exactly 1

SECTION 2, CONVERSION BRIDGE (rates and ratios)
  Nest 9          : the master chain (Rule 3) and the derived examples (Rule 7)
  Nest 10         : dilation in built units (Rule 3), ticks <-> Observer 0 years (Rules 4 and 5),
                    the whole-sphere position (Rule 7), the tier ratio (Rule 8)

SECTION 3, OBSERVER 0 (inputs and readings)
  Block A         : the inputs
  Block B         : the second-chain results (Order A, Order B)
  Block C         : the constants in substrate units

The command appendix_a keeps its name from earlier versions. It now returns the
results of Block B.

Every function is a direct formula. No loop over the cycle is needed.

The engine prints full arithmetic values. Block B shows the same values
cut at the certainty limit of alpha inverse.

Use as a tool:
  python3 cse_engine.py                 summary
  python3 cse_engine.py state 2147483649
  python3 cse_engine.py position 1000
  python3 cse_engine.py local 0.75 1000
  python3 cse_engine.py lag 1000
  python3 cse_engine.py room 1000
  python3 cse_engine.py order_a 13.8e9
  python3 cse_engine.py order_b 4294967295
  python3 cse_engine.py appendix_a
  python3 cse_engine.py selftest
Use as a module:
  import cse_engine as cse
  cse.state(1)
"""
from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction

# --------------------------------------------------
# SECTION 1: GLOBAL DEFINITIONS & COUNTING CONVENTIONS
# --------------------------------------------------
M = 2**31 - 1                 # LIMIT: 2,147,483,647
POSITIONS = 2**31             # positions 0 to M
CYCLE_COUNT = 2**32           # counted operations per cycle
TICK_COUNT = 2**32 - 1        # highest value of the runtime counter (Nest 2, Rule 9)
TRANSITION_COUNT = 2**32 - 2  # the 2 reversals are not transitions

# --------------------------------------------------
# SECTION 3, BLOCK A: INPUTS 4 TO 6 (c, h-bar and G in human units)
# They are placed here because the master chain is built from them.
# --------------------------------------------------
C = 299792458.0               # input 4: meters per second (exact by definition)
HBAR = 1.054571817e-34        # input 5: joule seconds (exact by definition)
G = 6.674e-11                 # input 6: m^3 / (kg s^2) (measured, certain to 4 digits)

# --------------------------------------------------
# SECTION 2, NEST 9: THE MASTER CHAIN (RULE 3)
# Each link uses the link before it.
# --------------------------------------------------
METERS_PER_POSITION = math.sqrt(HBAR * G / C**3)        # Link 1 (space)
SECONDS_PER_TRANSITION = METERS_PER_POSITION / C        # Link 2 (time)
JOULES_PER_ENERGY_UNIT = HBAR / SECONDS_PER_TRANSITION  # Link 3 (energy)

# --------------------------------------------------
# SECTION 2, NEST 10: THE SECOND CHAIN
# --------------------------------------------------
ALPHA_INVERSE = 137.035999177   # dilation index (Nest 10, Rule 2). Shown there as 137.0359991...
YEARS_PER_TICK = 1062           # conversion ratio: 1 tick = 1062 undilated years (Nest 10, Rule 4)
SECONDS_PER_YEAR = 31_557_600   # Nest 10, Rule 8

# Section 3, Block A: inputs 1 to 3. Observer 0 estimates, taken as given.
CURRENT_AGE_YEARS = 13.8e9          # input 1
LIFESPAN_YEARS = 33.3e9             # input 2
EXPANSION_ENDS_IN_YEARS = 11.0e9    # input 3

# --------------------------------------------------
# SECTION 2, NEST 10, RULES 7 AND 8: WHOLE-SPHERE POSITION AND TIER RATIO
# --------------------------------------------------
UNDILATED_SECONDS_PER_TICK = YEARS_PER_TICK * SECONDS_PER_YEAR
UNDILATED_SECONDS_PER_TRANSITION = SECONDS_PER_TRANSITION * ALPHA_INVERSE
PLANCK_TIMES_PER_TICK = UNDILATED_SECONDS_PER_TICK / UNDILATED_SECONDS_PER_TRANSITION
# Rule 7 (postulate): 1 whole-sphere position = the distance light covers in 1 tick.
LIGHT_YEARS_PER_WHOLE_SPHERE_POSITION = YEARS_PER_TICK / ALPHA_INVERSE


# --------------------------------------------------
# SECTION 2, NEST 10, RULE 5: ORDER A AND ORDER B (Nest 8, Rule 6)
# --------------------------------------------------
def order_a(dilated_years: float) -> dict:
    """Observer 0 to substrate: dilated years -> undilated years -> ticks."""
    undilated = dilated_years * ALPHA_INVERSE
    return {
        "dilated_years": dilated_years,
        "undilated_years": undilated,
        "ticks": undilated / YEARS_PER_TICK,
    }


def order_b(ticks: float) -> dict:
    """Substrate to Observer 0: ticks -> undilated years -> dilated years."""
    undilated = ticks * YEARS_PER_TICK
    return {
        "ticks": ticks,
        "undilated_years": undilated,
        "dilated_years": undilated / ALPHA_INVERSE,
    }


# --------------------------------------------------
# SECTION 3, BLOCK B: SECOND-CHAIN RESULTS
# --------------------------------------------------
def appendix_a(current_age: float = CURRENT_AGE_YEARS,
               lifespan: float = LIFESPAN_YEARS,
               expansion_ends_in: float = EXPANSION_ENDS_IN_YEARS) -> dict:
    """Block B, rows 1.1 to 1.8 and lines 2.1 to 2.4. Subtraction is done in ticks only (Nest 8, Rule 7)."""
    age = order_a(current_age)                              # row 1.1
    expected = order_a(lifespan)                            # row 1.2
    corrected = order_b(TICK_COUNT)                         # row 1.3
    mismatch = order_b(expected["ticks"] - TICK_COUNT)      # row 1.4
    remaining = order_b(TICK_COUNT - age["ticks"])          # row 1.5
    cse_turn = order_b(2**31)                               # row 1.6
    observer_turn = order_a(current_age + expansion_ends_in)  # row 1.7
    lag = order_b(observer_turn["ticks"] - 2**31)           # row 1.8
    return {
        "inputs_taken_as_given": {
            "current_age_years": current_age,
            "lifespan_years": lifespan,
            "expansion_ends_in_years": expansion_ends_in,
        },
        "current_age": age,
        "expected_lifespan": expected,
        "corrected_lifespan": corrected,
        "mismatch": mismatch,
        "remaining": remaining,
        "percent_of_runtime": {                             # lines 2.1 and 2.2
            "remaining": remaining["ticks"] / TICK_COUNT * 100,
            "current": age["ticks"] / TICK_COUNT * 100,
        },
        "origin_of_1062": lifespan * ALPHA_INVERSE / TICK_COUNT,  # line 3.4
        "turning_point": {                                  # rows 1.6 to 1.8, lines 2.3 and 2.4
            "cse_turn_of_the_shell": cse_turn,
            "observer_0_turning_point": observer_turn,
            "lag": lag,
            "lag_percent_of_runtime": lag["ticks"] / TICK_COUNT * 100,
            "observer_0_percent_of_runtime": observer_turn["ticks"] / TICK_COUNT * 100,
            "status": "fitted from the Observer 0 input, not derived (Block B, line 3.11)",
        },
    }


# --------------------------------------------------
# SECTION 2, NEST 10, RULE 3: DILATION IN BUILT UNITS
# --------------------------------------------------
def undilate(value: float, seconds_power: int) -> float:
    """Dilated value -> undilated value, by the power of seconds in the unit.

    seconds_power = 1  : a duration (seconds)             value * alpha inverse
    seconds_power = -1 : a speed, and h-bar (per second)  value / alpha inverse
    seconds_power = -2 : an energy, and G (per second^2)  value / alpha inverse^2
    """
    return value * ALPHA_INVERSE**seconds_power


# --------------------------------------------------
# SECTION 1, NEST 0: THE CYCLE
# --------------------------------------------------
def _state(op: int, m: int) -> dict:
    """State after counted operation number `op` (1, 2, 3, ...), for limit m.

    Order inside one cycle (Nest 0, CYCLE COUNT):
      op 1            : P at [Kernel-0]      (polarity switch)
      op 2 .. m+1     : m increments         (Phase 1)
      op m+2          : P at [Kernel-S0]     (polarity return)
      op m+3 .. 2m+2  : m decrements         (Phase 2)
    The loop is closed: op 2m+3 is op 1 of the next cycle.

    Tick (Global definitions, TICK; Nest 2, Rule 10): the runtime counter is at 0 at op 1 and advances
    once for each later counted operation. Its highest value is 2m+1.
    """
    if not isinstance(op, int) or isinstance(op, bool) or op < 1:
        raise ValueError("op must be a whole number, 1 or larger")

    cycle_count = 2 * m + 2
    cycle, k = divmod(op - 1, cycle_count)
    k += 1  # k is the operation number inside the cycle: 1 .. cycle_count

    if k == 1:
        operation, phase, s, transitions = "P", 1, 0, 0
    elif k <= m + 1:
        operation, phase, s = "increment", 1, k - 1
        transitions = s
    elif k == m + 2:
        operation, phase, s, transitions = "P", 2, m, m
    else:
        operation, phase, s = "decrement", 2, 2 * m + 2 - k
        transitions = m + (m - s)

    # Kernel states (Nest 0)
    if s == 0:
        kernel = "Kernel-0"
    elif s == m:
        kernel = "Kernel-S0"
    elif operation == "increment" and s == 1:
        kernel = "Kernel-1"
    elif operation == "decrement" and s == m - 1:
        kernel = "Kernel-S1"
    else:
        kernel = None

    # Poles (Nest 4)
    pole = "Pole 0" if s == 0 else "Pole 1" if s == m else None

    # Time points (Nest 2)
    if k == 1:
        time_point = 0
    elif s == m:
        time_point = 1
    elif k == cycle_count:
        time_point = 2  # resets to 0 at [Kernel-0] (Nest 2, Rule 8)
    else:
        time_point = None

    return {
        "op": op,
        "cycle": cycle,
        "op_in_cycle": k,
        "tick": k - 1,
        "operation": operation,
        "phase": phase,
        "position": s,
        "radius": s,
        "kernel": kernel,
        "pole": pole,
        "time_point": time_point,
        "transitions_elapsed": transitions,
        "bound_units": s,
        "free_units": m - s,
        "bound": s / m,
        "free": 1 - s / m,
        "total": 1,
    }


def state(op: int) -> dict:
    """State of the model after counted operation `op`, with Observer 0 units.

    planck_tier       : the master chain (Nest 9, Rule 3).
    whole_sphere_tier : the second chain (Nest 10, Order B), from the tick.
    """
    st = _state(op, M)
    st["observer_0"] = {
        "planck_tier": {
            "radius_meters": st["position"] * METERS_PER_POSITION,
            "elapsed_seconds": st["transitions_elapsed"] * SECONDS_PER_TRANSITION,
            "bound_joules": st["bound_units"] * JOULES_PER_ENERGY_UNIT,
            "free_joules": st["free_units"] * JOULES_PER_ENERGY_UNIT,
        },
        "whole_sphere_tier": order_b(st["tick"]),
    }
    return st


# --------------------------------------------------
# SECTION 1, NEST 1 + NEST 3: ENERGY AT A POSITION
# --------------------------------------------------
def position(s: int) -> dict:
    """Energy and Observer 0 units at position s (0 to M)."""
    if not isinstance(s, int) or isinstance(s, bool) or not 0 <= s <= M:
        raise ValueError("position must be a whole number from 0 to 2,147,483,647")
    return {
        "position": s,
        "radius": s,
        "pole": "Pole 0" if s == 0 else "Pole 1" if s == M else None,
        "bound_units": s,
        "free_units": M - s,
        "bound": s / M,
        "free": 1 - s / M,
        "total": 1,
        "observer_0": {
            "planck_tier": {
                "radius_meters": s * METERS_PER_POSITION,
                "bound_joules": s * JOULES_PER_ENERGY_UNIT,
                "free_joules": (M - s) * JOULES_PER_ENERGY_UNIT,
            },
        },
    }


# --------------------------------------------------
# SECTION 1, NEST 5: DENSE MATTER POCKET / VOID
# --------------------------------------------------
def local(local_bound_fraction: float, s: int) -> dict:
    """Compare a local bound fraction (0 to 1) with the whole-sphere value s / M."""
    if not 0 <= local_bound_fraction <= 1:
        raise ValueError("local bound fraction must be from 0 to 1")
    if not isinstance(s, int) or isinstance(s, bool) or not 0 <= s <= M:
        raise ValueError("position must be a whole number from 0 to 2,147,483,647")
    whole = Fraction(s, M)
    here = Fraction(local_bound_fraction)
    if here > whole:
        kind = "dense matter pocket"
    elif here < whole:
        kind = "void"
    else:
        kind = "even"
    return {
        "position": s,
        "whole_sphere_value": s / M,
        "local_bound_fraction": local_bound_fraction,
        "result": kind,
    }


# --------------------------------------------------
# SECTION 1, NEST 5, RULE 15: TURN LAG
# --------------------------------------------------
def turn_lag(r: int) -> dict:
    """Minimum turn lag for a place at radius r (0 to M) when the shell turns at Pole 1.

    The lag is at least the distance from the shell, counted in transitions.
    It is longer in dense matter pockets, and the model gives no formula for that.
    """
    if not isinstance(r, int) or isinstance(r, bool) or not 0 <= r <= M:
        raise ValueError("radius must be a whole number from 0 to 2,147,483,647")
    minimum = M - r
    return {
        "radius": r,
        "distance_from_shell": minimum,
        "minimum_lag_transitions": minimum,
        "minimum_lag_percent_of_runtime": minimum / TICK_COUNT * 100,
    }


# --------------------------------------------------
# SECTION 1, NEST 5, RULE 16: ROOM FOR GRAVITY
# --------------------------------------------------
def gravity_room(s: int) -> dict:
    """Room for gravity when the shell is at position s (0 to M).

    The local bound fraction cannot exceed 1, so the excess is at most the
    free fraction, 1 - s / M. Counted in gaps of the Nest 3 line, that is M - s.
    One position from Pole 1 it is exactly 1 gap. At Pole 1 it is 0.
    """
    if not isinstance(s, int) or isinstance(s, bool) or not 0 <= s <= M:
        raise ValueError("position must be a whole number from 0 to 2,147,483,647")
    return {
        "position": s,
        "whole_sphere_value": s / M,
        "room_gaps": M - s,
        "room": (M - s) / M,
        "one_gap": 1 / M,
    }


# --------------------------------------------------
# A NUMBER AS THE MODEL TEXT SHOWS IT
# --------------------------------------------------
def _sci(x: float, digits: int = 4) -> str:
    """A number as 'm x 10^e', with the given count of significant digits."""
    mant, exp = f"{x:.{digits - 1}e}".split("e")
    return f"{mant} x 10^{int(exp)}"


# --------------------------------------------------
# TOTALS (Section 1 counts, both chains, tier ratio, Block C)
# --------------------------------------------------
def totals() -> dict:
    mass = JOULES_PER_ENERGY_UNIT / C**2
    runtime = order_b(TICK_COUNT)
    return {
        "M": M,
        "positions": POSITIONS,
        "cycle_count": CYCLE_COUNT,
        "tick_count": TICK_COUNT,
        "transition_count": TRANSITION_COUNT,
        "reversals_per_cycle": 2,
        "tick_count_parts": {                                # Nest 2, Rule 10
            "arc_1": M,
            "reversal_at_kernel_s0": 1,
            "arc_2": M,
        },
        "master_chain": {
            "meters_per_position": METERS_PER_POSITION,
            "seconds_per_transition": SECONDS_PER_TRANSITION,
            "joules_per_energy_unit": JOULES_PER_ENERGY_UNIT,
        },
        "planck_tier_loop": {
            "maximum_radius_meters": M * METERS_PER_POSITION,
            "one_arc_seconds": M * SECONDS_PER_TRANSITION,
            "total_energy_joules": M * JOULES_PER_ENERGY_UNIT,
        },
        "derived_examples": {
            "mass_kilograms": mass,
            "force_newtons": JOULES_PER_ENERGY_UNIT / METERS_PER_POSITION,
            "power_watts": JOULES_PER_ENERGY_UNIT / SECONDS_PER_TRANSITION,
            "density_kg_per_m3": mass / METERS_PER_POSITION**3,
        },
        "second_chain": {
            "alpha_inverse": ALPHA_INVERSE,
            "undilated_years_per_tick": YEARS_PER_TICK,
            "dilated_years_per_tick": YEARS_PER_TICK / ALPHA_INVERSE,
        },
        "whole_sphere_tier": {
            "total_runtime_ticks": TICK_COUNT,
            "total_runtime_undilated_years": runtime["undilated_years"],
            "total_runtime_dilated_years": runtime["dilated_years"],
            "light_years_per_position": LIGHT_YEARS_PER_WHOLE_SPHERE_POSITION,   # Nest 10, Rule 7
        },
        "tier_ratio": {
            "undilated_seconds_per_tick": UNDILATED_SECONDS_PER_TICK,
            "undilated_seconds_per_planck_time": UNDILATED_SECONDS_PER_TRANSITION,
            "planck_times_per_tick": PLANCK_TIMES_PER_TICK,
        },
        "block_c": {
            "c_in_substrate_units": C / (METERS_PER_POSITION / SECONDS_PER_TRANSITION),
            "hbar_in_substrate_units": HBAR / (JOULES_PER_ENERGY_UNIT * SECONDS_PER_TRANSITION),
            "G_in_substrate_units": G / (METERS_PER_POSITION * C**4 / JOULES_PER_ENERGY_UNIT),
            "c_meters_per_undilated_second": undilate(C, -1),
        },
    }


# --------------------------------------------------
# SELF TEST
# --------------------------------------------------
def selftest() -> list[str]:
    """Check the formulas against a step-by-step walk, and check the 32-bit ends."""
    done = []

    # 1. Counts (Global definitions, Nest 0)
    assert CYCLE_COUNT == 1 + M + 1 + M == 4_294_967_296
    assert TRANSITION_COUNT == M + M == 4_294_967_294
    assert POSITIONS == M + 1
    done.append("counts: 1 + M + 1 + M = 4,294,967,296")

    # 2. Walk a small loop one operation at a time and compare with the formulas.
    m = 127
    walk = [("P", 0)]
    s = 0
    for _ in range(m):
        s += 1
        walk.append(("increment", s))
    walk.append(("P", s))
    for _ in range(m):
        s -= 1
        walk.append(("decrement", s))
    assert len(walk) == 2 * m + 2 and s == 0
    for k, (operation, pos) in enumerate(walk, start=1):
        st = _state(k, m)
        assert (st["operation"], st["position"]) == (operation, pos)
        assert st["bound_units"] + st["free_units"] == m
        assert st["tick"] == k - 1
    assert sum(1 for operation, _ in walk if operation == "P") == 2
    for k in range(2, 2 * m + 3):                          # Nest 4, Rule 10: constant velocity
        now, before = _state(k, m), _state(k - 1, m)
        assert abs(now["position"] - before["position"]) == (0 if now["operation"] == "P" else 1)
    nxt = _state(2 * m + 3, m)
    assert (nxt["cycle"], nxt["op_in_cycle"], nxt["operation"]) == (1, 1, "P")
    done.append("walk: formulas match a step-by-step loop, 1 position per transition, 2 reversals, loop closes")

    # 3. The 32-bit kernel states (Nest 0)
    checks = [
        (1, "P", 0, "Kernel-0", 0),
        (2, "increment", 1, "Kernel-1", None),
        (M + 1, "increment", M, "Kernel-S0", 1),
        (M + 2, "P", M, "Kernel-S0", 1),
        (M + 3, "decrement", M - 1, "Kernel-S1", None),
        (CYCLE_COUNT, "decrement", 0, "Kernel-0", 2),
    ]
    for op, operation, pos, kernel, time_point in checks:
        st = state(op)
        assert (st["operation"], st["position"], st["kernel"], st["time_point"]) == (
            operation, pos, kernel, time_point)
    assert state(CYCLE_COUNT + 1)["cycle"] == 1
    done.append("kernel states: Kernel-0, Kernel-1, Kernel-S0, Kernel-S1 at the right operations")

    # 4. Conservation (Nest 1)
    for op in (1, 2, 12345, M, M + 1, M + 2, M + 3, 3_000_000_000, CYCLE_COUNT):
        st = state(op)
        assert st["bound_units"] + st["free_units"] == M
    done.append("conservation: bound + free = M at every tested operation")

    # 5. Nest 7, Rule 3 and Nest 9, Rule 1: the three constants are rebuilt from the three steps
    L, T, E = METERS_PER_POSITION, SECONDS_PER_TRANSITION, JOULES_PER_ENERGY_UNIT
    assert math.isclose(L / T, C, rel_tol=1e-12)
    assert math.isclose(E * T, HBAR, rel_tol=1e-12)
    assert math.isclose(L * C**4 / E, G, rel_tol=1e-12)
    done.append("constants: c, hbar and G rebuilt from the three steps (Nest 7, Rule 3)")

    # 6. Ticks (Global definitions, TICK; Nest 2, Rules 9 and 10)
    assert TICK_COUNT == CYCLE_COUNT - 1 == TRANSITION_COUNT + 1 == 4_294_967_295
    assert TICK_COUNT == M + 1 + M == sum(totals()["tick_count_parts"].values())
    assert state(1)["tick"] == 0
    assert state(M + 1)["tick"] == M              # the end of Arc 1
    assert state(M + 2)["tick"] == 2**31          # the reversal at [Kernel-S0]
    assert state(CYCLE_COUNT)["tick"] == TICK_COUNT
    assert state(CYCLE_COUNT + 1)["tick"] == 0    # the counter returns to 0
    done.append("ticks: counter runs 0 to 4,294,967,295 and returns to 0")

    # 7. Block B, against the values printed in the model text
    a = appendix_a()
    assert int(a["current_age"]["ticks"]) == 1_780_693_774                      # row 1.1
    assert round(a["expected_lifespan"]["ticks"], -1) == 4_296_891_500          # row 1.2
    assert a["corrected_lifespan"]["undilated_years"] == 4_561_255_267_290      # row 1.3
    assert round(a["corrected_lifespan"]["dilated_years"], -2) == 33_285_087_800  # row 1.3
    assert round(a["mismatch"]["ticks"], -1) == 1_924_200                       # row 1.4
    assert round(a["mismatch"]["dilated_years"], -2) == 14_912_200              # row 1.4
    assert int(a["remaining"]["ticks"]) == 2_514_273_520                        # row 1.5
    assert round(a["remaining"]["dilated_years"], -2) == 19_485_087_800         # row 1.5
    assert abs(a["percent_of_runtime"]["current"] - 41.4600077) < 1e-7          # line 2.2
    assert abs(a["percent_of_runtime"]["remaining"] - 58.5399922) < 1e-7        # line 2.1
    assert abs(a["origin_of_1062"] - 1062.475790) < 1e-6                        # line 3.4
    assert int(a["origin_of_1062"]) == YEARS_PER_TICK
    t = a["turning_point"]
    assert t["cse_turn_of_the_shell"]["undilated_years"] == 2_280_627_634_176   # row 1.6
    assert round(t["cse_turn_of_the_shell"]["dilated_years"], -1) == 16_642_543_910  # row 1.6
    assert round(t["observer_0_turning_point"]["ticks"], -1) == 3_200_087_360   # row 1.7
    assert round(t["lag"]["ticks"], -1) == 1_052_603_720                        # row 1.8
    assert round(t["lag"]["dilated_years"], -1) == 8_157_456_090                # row 1.8
    assert abs(t["lag_percent_of_runtime"] - 24.507840) < 1e-6                  # line 2.3
    assert abs(t["observer_0_percent_of_runtime"] - 74.507840) < 1e-6           # line 2.4
    done.append("block B: rows 1.1 to 1.8 and lines 2.1 to 2.4 match the model text")

    # 8. Order A and Order B return the same numbers (Block B, line 3.5)
    for years in (1.0, 13.8e9, 33.3e9):
        back = order_b(order_a(years)["ticks"])["dilated_years"]
        assert abs(back - years) <= years * 1e-12
    done.append("orders: Order A then Order B returns the starting value")

    # 9. Whole-sphere position and tier ratio (Nest 10, Rules 7 and 8)
    assert UNDILATED_SECONDS_PER_TICK == 33_514_171_200
    assert 4.535e51 < PLANCK_TIMES_PER_TICK < 4.537e51
    assert abs(LIGHT_YEARS_PER_WHOLE_SPHERE_POSITION - 7.749788) < 1e-6
    done.append("tier ratio: one tick is about 4.536e51 Planck times")

    # 10. Block C: the constants return 1 by construction
    b = totals()["block_c"]
    for name in ("c_in_substrate_units", "hbar_in_substrate_units", "G_in_substrate_units"):
        assert abs(b[name] - 1) < 1e-12
    assert round(b["c_meters_per_undilated_second"], 2) == 2_187_691.26         # line 2
    done.append("block C: c, h-bar and G are 1 in substrate units")

    # 11. Turn lag (Nest 5, Rule 15)
    assert turn_lag(M)["minimum_lag_transitions"] == 0
    assert turn_lag(0)["minimum_lag_transitions"] == M
    done.append("turn lag: 0 at the shell, M at Pole 0")

    # 12. Master chain, against the values printed in the model text (Nest 9, Rules 3 and 7)
    mass = E / C**2
    assert (_sci(L), _sci(T), _sci(E)) == ("1.616 x 10^-35", "5.391 x 10^-44", "1.956 x 10^9")
    assert _sci(mass) == "2.176 x 10^-8"
    assert _sci(E / L) == "1.210 x 10^44"
    assert _sci(E / T) == "3.628 x 10^52"
    assert _sci(mass / L**3) == "5.155 x 10^96"
    assert math.isclose(HBAR * C / mass**2, G, rel_tol=1e-12)    # the mass unit (Nest 7, Rule 4)
    done.append("master chain: the 3 links and the derived examples match the model text")

    # 13. Room for gravity (Nest 5, Rule 16)
    assert gravity_room(0)["room_gaps"] == M
    assert gravity_room(M - 1)["room_gaps"] == 1
    assert gravity_room(M)["room_gaps"] == 0
    done.append("room for gravity: M gaps at Pole 0, 1 gap one position from Pole 1, 0 at Pole 1")

    return done


# --------------------------------------------------
# COMMAND LINE
# --------------------------------------------------
def _show(data) -> None:
    print(json.dumps(data, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Canonical Substrate Engine (CSE) v1.6")
    sub = parser.add_subparsers(dest="command")
    p = sub.add_parser("state", help="state after counted operation OP (1 or larger)")
    p.add_argument("op", type=int)
    p = sub.add_parser("position", help="energy at position S (0 to 2147483647)")
    p.add_argument("s", type=int)
    p = sub.add_parser("local", help="pocket / void test: local bound fraction V (0 to 1) at position S")
    p.add_argument("v", type=float)
    p.add_argument("s", type=int)
    p = sub.add_parser("lag", help="minimum turn lag for a place at radius R (0 to 2147483647)")
    p.add_argument("r", type=int)
    p = sub.add_parser("room", help="room for gravity when the shell is at position S (0 to 2147483647)")
    p.add_argument("s", type=int)
    p = sub.add_parser("order_a", help="Observer 0 dilated YEARS -> undilated years -> ticks")
    p.add_argument("years", type=float)
    p = sub.add_parser("order_b", help="TICKS -> undilated years -> Observer 0 dilated years")
    p.add_argument("ticks", type=float)
    sub.add_parser("appendix_a", help="Block B: the second-chain results")
    sub.add_parser("totals", help="counts, both chains, tier ratio, constants")
    sub.add_parser("selftest", help="check the engine against the model")
    args = parser.parse_args()

    if args.command == "state":
        _show(state(args.op))
    elif args.command == "position":
        _show(position(args.s))
    elif args.command == "local":
        _show(local(args.v, args.s))
    elif args.command == "lag":
        _show(turn_lag(args.r))
    elif args.command == "room":
        _show(gravity_room(args.s))
    elif args.command == "order_a":
        _show(order_a(args.years))
    elif args.command == "order_b":
        _show(order_b(args.ticks))
    elif args.command == "appendix_a":
        _show(appendix_a())
    elif args.command == "selftest":
        for line in selftest():
            print("PASS ", line)
    else:
        _show(totals())


if __name__ == "__main__":
    main()
