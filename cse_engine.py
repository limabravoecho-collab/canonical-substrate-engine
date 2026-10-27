#!/usr/bin/env python3
"""
cse_engine.py - Canonical Substrate Engine (CSE) v1.9
A Deterministic Computational Cosmological Logic Model, in executable form.

This file computes only what the model defines with a number or a formula.

SECTION 1, SUBSTRATE (counts only)
  Order of Operations : the alpha stack 136, 137, 137 + delta, G resolution, overflow (Rules 1 to 6)
  Global definitions + Nest 0 : the closed cycle of 4,294,967,296 counted operations, and the tick
  Nest 1 + Nest 3 : bound / free energy at a position, and the three regime labels (Rule 7)
  Nest 2          : phase (arc), time points 0, 1, 2, the total runtime, the tick count (Rule 10),
                    and the time-rate bounds (Rule 11)
  Nest 4          : radius, poles, and the constant velocity of the shell (Rule 10)
  Nest 5          : dense matter pocket / void test (Rules 2, 4, 5), turn lag (Rule 15),
                    room for gravity (Rule 16), local rate (Rule 19)
  Nest 7          : the unit steps, the constants and the mass unit, each exactly 1

SECTION 2, CONVERSION BRIDGE (rates and ratios)
  Nest 9          : the master chain (Rule 3) and the derived examples (Rule 7)
  Nest 10         : dilation in built units (Rule 4), ticks <-> Observer 0 years (Rules 5 and 6),
                    the whole-sphere position (Rule 7), the tier ratio (Rule 8)

SECTION 3, OBSERVER 0 (inputs and readings)
  Nest 11         : ambiguity cross-references (Rule 5)
  Nest 12         : self-similarity sharpening (Rule 6)
  Nest 13         : c_local = 1 / sqrt(alpha_inv_local) (Rule 4), the hardware basis counts (Rule 10),
                    stop-limit dynamics (Rule 11)
  Block A         : the inputs
  Block B         : the second-chain results (Order A, Order B)
  Block C         : the constants in substrate units
  Block D         : the numerical checks, Tests 1 to 5

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
  python3 cse_engine.py regime 0.75 1000
  python3 cse_engine.py rate 0.75 1000
  python3 cse_engine.py lag 1000
  python3 cse_engine.py room 1000
  python3 cse_engine.py order_a 13.8e9
  python3 cse_engine.py order_b 4294967295
  python3 cse_engine.py appendix_a
  python3 cse_engine.py alpha 0.036
  python3 cse_engine.py block_d
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
# SECTION 1, ORDER OF OPERATIONS & SUBSTRATE LAW (Rules 1 to 6)
# Executes before all nests.
# --------------------------------------------------
G_SUBSTRATE = 1                                       # Rule 1: exact substrate units
ALPHA_SUBSTRATE = 1                                   # Rule 1: no dilation at root
TIERS = 4                                             # Rule 2: Nests 0 to 3
REGISTER_BITS = 32                                    # Rule 2: register width, M = 2^31 - 1
CONTROL_BITS = 4 * 2                                  # Rule 2: 4 kernel states x 2 polarity directions
ALPHA_INV_UNIVERSAL = TIERS * REGISTER_BITS + CONTROL_BITS   # Rule 2: 128 + 8 = 136
ALPHA_INV_NEST = ALPHA_INV_UNIVERSAL + 1              # Rule 3: 137
ALPHA_INVERSE = 137.035999177   # Rule 4: alpha_inv_local at the current cosmic mean, measured. Shown as 137.035999...
ALPHA_INV_LOCAL = ALPHA_INVERSE                       # the same number, under its earlier name
DELTA_MEAN = ALPHA_INVERSE - ALPHA_INV_NEST           # Rule 4: 0.035999...
DELTA_VOID = 0.01                                     # Rule 4
DELTA_CLUSTER = 0.06                                  # Rule 4
DELTA_MAX = ALPHA_INV_UNIVERSAL                       # Rule 6: delta -> 136, alpha_inv_local -> 273
G_LOCAL_SUBSTRATE = G_SUBSTRATE / ALPHA_INVERSE**2    # Rule 5: 5.325135e-05 substrate units
REGISTER_MAX = 0x7FFFFFFF                             # Rule 6: = M
REGISTER_ROLL = 0x80000000                            # Rule 6: the next tick after REGISTER_MAX

# --------------------------------------------------
# SECTION 3, BLOCK A: INPUTS 4 TO 6 (c, h-bar and G_local in human units)
# They are placed here because the master chain is built from them.
# --------------------------------------------------
C = 299792458.0               # input 4: meters per second (exact by definition)
HBAR = 1.054571817e-34        # input 5: joule seconds (exact by definition)
G = 6.674e-11                 # input 6: G_local human, m^3 / (kg s^2) (measured, certain to 4 digits)
G_TO_HUMAN = G / G_LOCAL_SUBSTRATE   # input 6: conversion factor, found by division. Shown as 1.253e-06

# --------------------------------------------------
# SECTION 2, NEST 9: THE MASTER CHAIN (RULE 3)
# Each link uses the link before it. Inputs: h-bar, c and G_local human (Rule 2).
# --------------------------------------------------
METERS_PER_POSITION = math.sqrt(HBAR * G / C**3)        # Link 1 (space)
SECONDS_PER_TRANSITION = METERS_PER_POSITION / C        # Link 2 (time)
JOULES_PER_ENERGY_UNIT = HBAR / SECONDS_PER_TRANSITION  # Link 3 (energy)

# --------------------------------------------------
# SECTION 2, NEST 10: THE SECOND CHAIN
# Alpha stack: see Order of Operations, Rules 2 to 4 (Nest 10, Rule 1).
# --------------------------------------------------
YEARS_PER_TICK = 1062           # conversion ratio: 1 tick = 1062 undilated years (Nest 10, Rule 5)
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
# SECTION 1, ORDER OF OPERATIONS, RULES 2 TO 6: THE ALPHA STACK AT A PLACE
# Also Nest 13, Rule 4: c_local = 1 / sqrt(alpha_inv_local).
# --------------------------------------------------
def alpha_stack(delta: float = DELTA_MEAN) -> dict:
    """The alpha stack and G resolution for a local deviation delta (0 to 136).

    alpha_inv_local = 136 + 1 + delta. G_local substrate = 1 / alpha_inv_local^2.
    G_local human = G_local substrate x the conversion factor (Block A, input 6).
    Overflow (Rule 6) is reached when delta = 136: alpha_inv_local = 273.
    """
    if not 0 <= delta <= DELTA_MAX:
        raise ValueError("delta must be from 0 to 136")
    alpha_local = ALPHA_INV_NEST + delta
    g_sub = G_SUBSTRATE / alpha_local**2
    return {
        "delta": delta,
        "alpha_inv_universal": ALPHA_INV_UNIVERSAL,         # Rule 2
        "alpha_inv_nest": ALPHA_INV_NEST,                   # Rule 3
        "alpha_inv_local": alpha_local,                     # Rule 4
        "G_substrate": G_SUBSTRATE,                         # Rule 1
        "G_local_substrate": g_sub,                         # Rule 5
        "G_local_human": g_sub * G_TO_HUMAN,                # Rule 5
        "c_local": 1 / math.sqrt(alpha_local),              # Nest 13, Rule 4
        "overflow": delta == DELTA_MAX,                     # Rule 6
    }


# --------------------------------------------------
# SECTION 1, NEST 3, RULE 7: THE THREE REGIME LABELS
# Labels are intervals on the Nest 3 Rule 5 line, partitioned at the whole-sphere value.
# They are not separate sub-loops.
# --------------------------------------------------
def regime(local_bound_fraction: float, s: int) -> dict:
    """Label a local bound fraction (0 to 1) against the whole-sphere value s / M.

    below-equilibrium  : local bound < whole-sphere value
    at-equilibrium     : local bound = whole-sphere value
    above-equilibrium  : local bound > whole-sphere value
    """
    if not 0 <= local_bound_fraction <= 1:
        raise ValueError("local bound fraction must be from 0 to 1")
    if not isinstance(s, int) or isinstance(s, bool) or not 0 <= s <= M:
        raise ValueError("position must be a whole number from 0 to 2,147,483,647")
    whole = Fraction(s, M)
    here = Fraction(local_bound_fraction)
    if here < whole:
        label = "below-equilibrium"
    elif here == whole:
        label = "at-equilibrium"
    else:
        label = "above-equilibrium"
    return {
        "position": s,
        "whole_sphere_value": s / M,
        "local_bound_fraction": local_bound_fraction,
        "regime": label,
    }


# --------------------------------------------------
# SECTION 3, BLOCK B: SECOND-CHAIN RESULTS
# --------------------------------------------------
def appendix_a(current_age: float = CURRENT_AGE_YEARS,
               lifespan: float = LIFESPAN_YEARS,
               expansion_ends_in: float = EXPANSION_ENDS_IN_YEARS) -> dict:
    """Block B, rows 1.1, 1.3, 1.5, 1.6 and lines 2.1, 2.2. Subtraction is done in ticks only (Nest 8, Rule 7).

    lifespan and expansion_ends_in are inputs 2 and 3 (Block A). They are reported, not used."""
    age = order_a(current_age)                              # row 1.1
    corrected = order_b(TICK_COUNT)                         # row 1.3
    remaining = order_b(TICK_COUNT - age["ticks"])          # row 1.5
    cse_turn = order_b(2**31)                               # row 1.6
    return {
        "inputs_taken_as_given": {
            "current_age_years": current_age,
            "lifespan_years": lifespan,
            "expansion_ends_in_years": expansion_ends_in,
        },
        "current_age": age,
        "corrected_lifespan": corrected,
        "remaining": remaining,
        "cse_turn_of_the_shell": cse_turn,
        "percent_of_runtime": {                             # lines 2.1 and 2.2
            "remaining": remaining["ticks"] / TICK_COUNT * 100,
            "current": age["ticks"] / TICK_COUNT * 100,
        },
    }


# --------------------------------------------------
# SECTION 3, BLOCK D: NUMERICAL CHECKS (Tests 1 to 5)
# --------------------------------------------------
def block_d() -> dict:
    """Block D, Tests 1 to 5. Every number is computed from the constants above."""
    void, cluster, mean, hole = (alpha_stack(DELTA_VOID), alpha_stack(DELTA_CLUSTER),
                                 alpha_stack(DELTA_MEAN), alpha_stack(DELTA_MAX))
    return {
        "test_1": {                                         # 136 = 4 x 32 + 8
            "tiers": TIERS, "bits": REGISTER_BITS, "control": CONTROL_BITS,
            "data_bus": TIERS * REGISTER_BITS, "alpha_inv_universal": ALPHA_INV_UNIVERSAL,
        },
        "test_2": {                                         # G from the alpha stack
            "alpha_inv_local": mean["alpha_inv_local"],
            "G_calc_substrate": mean["G_local_substrate"],
            "G_calc_human": mean["G_local_human"],
            "G_measured_human": G,
        },
        "test_3": {                                         # c_local follows 1 / alpha_inv_local
            "c_local_at_mean": mean["c_local"],
        },
        "test_4": {                                         # void vs cluster
            "delta_void": DELTA_VOID, "delta_cluster": DELTA_CLUSTER,
            "delta_variance": DELTA_CLUSTER / DELTA_VOID,
            "G_void_substrate": void["G_local_substrate"],
            "G_cluster_substrate": cluster["G_local_substrate"],
            "G_ratio": void["G_local_substrate"] / cluster["G_local_substrate"],
            "G_variance_percent": (void["G_local_substrate"] / cluster["G_local_substrate"] - 1) * 100,
        },
        "test_5": {                                         # overflow, no singularity
            "delta_max": DELTA_MAX,
            "alpha_inv_max": hole["alpha_inv_local"],
            "G_substrate_at_max": hole["G_local_substrate"],
            "register_max": REGISTER_MAX, "register_roll": REGISTER_ROLL,
            "overflow": hole["overflow"],
        },
    }


# --------------------------------------------------
# SECTION 2, NEST 10, RULE 4: DILATION IN BUILT UNITS
# --------------------------------------------------
def undilate(value: float, seconds_power: int) -> float:
    """Dilated value -> undilated value, by the power of seconds in the unit.

    seconds_power = 1  : a duration (seconds)                   value * alpha_inv_local
    seconds_power = -1 : a speed, and h-bar (per second)        value / alpha_inv_local
    seconds_power = -2 : an energy, and G_local (per second^2)  value / alpha_inv_local^2
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
    else:
        kind = "void"  # below or equal (Nest 5, Rule 5)
    return {
        "position": s,
        "whole_sphere_value": s / M,
        "local_bound_fraction": local_bound_fraction,
        "result": kind,
    }


# --------------------------------------------------
# SECTION 1, NEST 5, RULE 19: LOCAL RATE
# --------------------------------------------------
def local_rate(local_bound_fraction: float, s: int) -> dict:
    """Local time rate at a place, against the whole-sphere value s / M.

    At the whole-sphere value and at rest, the rate is 1 (unperturbed).
    Above the whole-sphere value (dense pocket), the rate is below 1.
    Below the whole-sphere value (void), the rate is above 1.
    The model gives the direction only; the exact rate at a place is fixed by
    Nest 5 Rule 13 (local time) and Rule 18 (speed time), which the substrate
    fixes by balance, not by value at one place (Nest 5 Rule 17).
    """
    if not 0 <= local_bound_fraction <= 1:
        raise ValueError("local bound fraction must be from 0 to 1")
    if not isinstance(s, int) or isinstance(s, bool) or not 0 <= s <= M:
        raise ValueError("position must be a whole number from 0 to 2,147,483,647")
    whole = Fraction(s, M)
    here = Fraction(local_bound_fraction)
    if here == whole:
        rate_dir = "= 1 (unperturbed)"
    elif here > whole:
        rate_dir = "< 1 (slow, dense pocket)"
    else:
        rate_dir = "> 1 (fast, void)"
    return {
        "position": s,
        "whole_sphere_value": s / M,
        "local_bound_fraction": local_bound_fraction,
        "local_rate": rate_dir,
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
# SECTION 1, NEST 2, RULE 11: TIME-RATE BOUNDS
# --------------------------------------------------
def time_rate_bounds() -> dict:
    """The bounds the model places on the time rate (Nest 2, Rule 11).

    The bounds are descriptive of the substrate, not a formula for a local place.
    """
    return {
        "minimum": 0,
        "minimum_state": "stopped",
        "maximum": 1,
        "maximum_state": "unperturbed background rate (Nest 2, Rule 7 baseline)",
        "open_interval": False,
        "note": "no rate outside [0, background]",
    }


# --------------------------------------------------
# SECTION 3, NEST 13, RULE 11: STOP-LIMIT DYNAMICS
# --------------------------------------------------
def stop_limit() -> dict:
    """The stop-limit dynamics stated in Nest 13, Rule 11.

    At the stop-limit, dynamics suspend. Friction cannot dissipate.
    Compressed energy is stored inert until reset (Nest 6, Rules 4 to 5).
    """
    return {
        "trigger": "Order of Operations Rule 6 (delta = 136, register roll)",
        "dynamics": "suspended",
        "friction": "cannot dissipate",
        "compressed_energy": "stored inert",
        "release": "reset at Nest 6 Rules 4 to 5",
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
        "order_of_operations": alpha_stack(),               # Rules 1 to 6, at the cosmic mean
        "time_rate_bounds": time_rate_bounds(),             # Nest 2, Rule 11
        "stop_limit": stop_limit(),                         # Nest 13, Rule 11
        "hardware_basis": {                                 # Nest 13, Rule 10
            "polarity_bits": 1, "magnitude_bits": 8, "mantissa_bits": 23,
            "total_bits": 1 + 8 + 23,
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
            "alpha_inv_local": ALPHA_INVERSE,
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
        (M
