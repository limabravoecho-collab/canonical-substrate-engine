#!/usr/bin/env python3
"""
cse_engine.py - Canonical Substrate Engine (CSE) v1.0
A Deterministic Cosmological Logic Model, in executable form.

This file computes only what the model defines with a number or a formula:
  Header + Nest 0 : the closed cycle of 4,294,967,296 counted operations
  Nest 1 + Nest 3 : compressed / uncompressed energy at a position
  Nest 2          : phase (arc) and time points 0, 1, 2
  Nest 4          : radius and poles
  Nest 5          : dense matter pocket / void test (Rules 2, 4, 5)
  Nest 8          : the master chain of conversion to Observer 0 units

Every function is a direct formula. No loop over the cycle is needed.

Use as a tool:
  python3 cse_engine.py                 summary
  python3 cse_engine.py state 2147483649
  python3 cse_engine.py position 1000
  python3 cse_engine.py local 0.75 1000
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
# HEADER: GLOBAL DEFINITIONS & COUNTING CONVENTIONS
# --------------------------------------------------
M = 2**31 - 1                 # LIMIT: 2,147,483,647
POSITIONS = 2**31             # positions 0 to M
CYCLE_COUNT = 2**32           # counted operations per cycle
TRANSITION_COUNT = 2**32 - 2  # the 2 reversals are not transitions

# --------------------------------------------------
# NEST 8: SUBSTRATE CONSTANTS, WRITTEN IN HUMAN UNITS
# --------------------------------------------------
HBAR = 1.054571817e-34        # joule seconds
C = 299792458.0               # meters per second
G = 6.67430e-11               # m^3 / (kg s^2)

# Master chain. Each link uses the link before it.
METERS_PER_POSITION = math.sqrt(HBAR * G / C**3)        # Link 1 (space)
SECONDS_PER_TRANSITION = METERS_PER_POSITION / C        # Link 2 (time)
JOULES_PER_ENERGY_UNIT = HBAR / SECONDS_PER_TRANSITION  # Link 3 (energy)


# --------------------------------------------------
# NEST 0: THE CYCLE
# --------------------------------------------------
def _state(op: int, m: int) -> dict:
    """State after counted operation number `op` (1, 2, 3, ...), for limit m.

    Order inside one cycle (Nest 0, CYCLE COUNT):
      op 1            : P at [Kernel-0]      (polarity switch)
      op 2 .. m+1     : m increments         (Phase 1)
      op m+2          : P at [Kernel-S0]     (polarity return)
      op m+3 .. 2m+2  : m decrements         (Phase 2)
    The loop is closed: op 2m+3 is op 1 of the next cycle.
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
        "operation": operation,
        "phase": phase,
        "position": s,
        "radius": s,
        "kernel": kernel,
        "pole": pole,
        "time_point": time_point,
        "transitions_elapsed": transitions,
        "compressed_units": s,
        "uncompressed_units": m - s,
        "compressed": s / m,
        "uncompressed": 1 - s / m,
        "total": 1,
    }


def state(op: int) -> dict:
    """State of the model after counted operation `op`, with Observer 0 units."""
    st = _state(op, M)
    st["observer_0"] = {
        "radius_meters": st["position"] * METERS_PER_POSITION,
        "elapsed_seconds": st["transitions_elapsed"] * SECONDS_PER_TRANSITION,
        "compressed_joules": st["compressed_units"] * JOULES_PER_ENERGY_UNIT,
        "uncompressed_joules": st["uncompressed_units"] * JOULES_PER_ENERGY_UNIT,
    }
    return st


# --------------------------------------------------
# NEST 1 + NEST 3: ENERGY AT A POSITION
# --------------------------------------------------
def position(s: int) -> dict:
    """Energy and Observer 0 units at position s (0 to M)."""
    if not isinstance(s, int) or isinstance(s, bool) or not 0 <= s <= M:
        raise ValueError("position must be a whole number from 0 to 2,147,483,647")
    return {
        "position": s,
        "radius": s,
        "pole": "Pole 0" if s == 0 else "Pole 1" if s == M else None,
        "compressed_units": s,
        "uncompressed_units": M - s,
        "compressed": s / M,
        "uncompressed": 1 - s / M,
        "total": 1,
        "observer_0": {
            "radius_meters": s * METERS_PER_POSITION,
            "compressed_joules": s * JOULES_PER_ENERGY_UNIT,
            "uncompressed_joules": (M - s) * JOULES_PER_ENERGY_UNIT,
        },
    }


# --------------------------------------------------
# NEST 5: DENSE MATTER POCKET / VOID
# --------------------------------------------------
def local(local_compression: float, s: int) -> dict:
    """Compare a local compression (0 to 1) with the whole-sphere value s / M."""
    if not 0 <= local_compression <= 1:
        raise ValueError("local compression must be from 0 to 1")
    if not isinstance(s, int) or isinstance(s, bool) or not 0 <= s <= M:
        raise ValueError("position must be a whole number from 0 to 2,147,483,647")
    whole = Fraction(s, M)
    here = Fraction(local_compression)
    if here > whole:
        kind = "dense matter pocket"
    elif here < whole:
        kind = "void"
    else:
        kind = "even"
    return {
        "position": s,
        "whole_sphere_value": s / M,
        "local_compression": local_compression,
        "result": kind,
    }


# --------------------------------------------------
# TOTALS (Header, Nest 0, Nest 8)
# --------------------------------------------------
def totals() -> dict:
    mass = JOULES_PER_ENERGY_UNIT / C**2
    return {
        "M": M,
        "positions": POSITIONS,
        "cycle_count": CYCLE_COUNT,
        "transition_count": TRANSITION_COUNT,
        "reversals_per_cycle": 2,
        "master_chain": {
            "meters_per_position": METERS_PER_POSITION,
            "seconds_per_transition": SECONDS_PER_TRANSITION,
            "joules_per_energy_unit": JOULES_PER_ENERGY_UNIT,
        },
        "whole_sphere": {
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
    }


# --------------------------------------------------
# SELF TEST
# --------------------------------------------------
def selftest() -> list[str]:
    """Check the formulas against a step-by-step walk, and check the 32-bit ends."""
    done = []

    # 1. Counts (Header, Nest 0)
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
        assert st["compressed_units"] + st["uncompressed_units"] == m
    assert sum(1 for operation, _ in walk if operation == "P") == 2
    nxt = _state(2 * m + 3, m)
    assert (nxt["cycle"], nxt["op_in_cycle"], nxt["operation"]) == (1, 1, "P")
    done.append("walk: formulas match a step-by-step loop, 2 reversals, loop closes")

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
        assert st["compressed_units"] + st["uncompressed_units"] == M
    done.append("conservation: compressed + uncompressed = M at every tested operation")

    return done


# --------------------------------------------------
# COMMAND LINE
# --------------------------------------------------
def _show(data) -> None:
    print(json.dumps(data, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Canonical Substrate Engine (CSE) v1.0")
    sub = parser.add_subparsers(dest="command")
    p = sub.add_parser("state", help="state after counted operation OP (1 or larger)")
    p.add_argument("op", type=int)
    p = sub.add_parser("position", help="energy at position S (0 to 2147483647)")
    p.add_argument("s", type=int)
    p = sub.add_parser("local", help="pocket / void test: local compression V (0 to 1) at position S")
    p.add_argument("v", type=float)
    p.add_argument("s", type=int)
    sub.add_parser("totals", help="counts, master chain, whole-sphere values")
    sub.add_parser("selftest", help="check the engine against the model")
    args = parser.parse_args()

    if args.command == "state":
        _show(state(args.op))
    elif args.command == "position":
        _show(position(args.s))
    elif args.command == "local":
        _show(local(args.v, args.s))
    elif args.command == "selftest":
        for line in selftest():
            print("PASS ", line)
    else:
        _show(totals())


if __name__ == "__main__":
    main()
