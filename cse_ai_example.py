#!/usr/bin/env python3
"""
cse_ai_example.py - how to wire cse_engine.py into an AI system (CSE v1.0)

THE RULE
    The engine computes. The LLM only translates.
    The engine decides the state. The LLM gives that state a voice.

WHAT THIS FILE SHOWS
    WIRE POINT 1  your own prose prompt, written for your target field
    WIRE POINT 2  the translator rule that keeps the LLM from computing
    WIRE POINT 3  tiers: mapping a real cycle (a day, a year, your own) onto the engine
    WIRE POINT 4  direct engine questions (exact answers, no LLM arithmetic)
    WIRE POINT 5  the bridge to science: Nest 8 conversions to human units
    WIRE POINT 6  where each piece goes in the message list
    WIRE POINT 7  the call to your own LLM

RUN IT
    python3 cse_ai_example.py
    No LLM is needed. It prints exactly what your LLM would receive.

SCOPE
    cse_engine.py has rules about its own cycle and its own conversions only.
    Anything outside that is answered by your LLM and your prompt, not by the engine.
"""
from __future__ import annotations

import json
from datetime import datetime

import cse_engine as cse


# ==================================================
# WIRE POINT 1: YOUR PROSE PROMPT
# Write this for your own target field. Keep it constant from turn to turn,
# so your LLM runtime can cache it.
# ==================================================
BASE_PROMPT = (
    "You are an assistant for <YOUR TARGET FIELD>.\n"
    "Speak plainly. Say only what you know."
)


# ==================================================
# WIRE POINT 2: THE TRANSLATOR RULE
# This is what makes the LLM a translator and not a calculator.
# Suggested LLM settings for this role: low temperature (0.2 to 0.4).
# ==================================================
TRANSLATOR_RULE = (
    "ENGINE RULE: Lines that start with ENGINE come from cse_engine.py and are exact. "
    "Never compute, change, round or guess an engine value yourself. "
    "Your task is to put the engine values into words for the reader, in the voice "
    "this prompt gives you. If no ENGINE line answers the question, say that the "
    "engine has no value for it."
)


# ==================================================
# WIRE POINT 3: TIERS
# A tier is one closed cycle mapped onto the engine (Nest 10, Rule 2).
# You give a fraction from 0 to 1: how far the cycle has run.
#   0.0 = Pole 0 (start)      0.5 = Pole 1 (the far turn)      1.0 = Pole 0 again
# The engine returns the exact state for that fraction.
# ==================================================
def tier_state(fraction: float) -> dict:
    """Exact engine state for a cycle that is `fraction` (0 to 1) complete."""
    op = min(int(fraction * cse.CYCLE_COUNT) + 1, cse.CYCLE_COUNT)
    return cse.state(op)


def tier_words(fraction: float) -> str:
    """The same state in plain words, for an LLM that must not speak numbers."""
    st = tier_state(fraction)
    setting_out = st["phase"] == 1
    along = st["compressed"] if setting_out else st["uncompressed"]  # 0 to 1 along this arc
    if along < 0.1:
        where = "at the start"
    elif along < 0.4:
        where = "early"
    elif along < 0.6:
        where = "half-way"
    elif along < 0.9:
        where = "past half-way"
    else:
        where = "nearly at the far turn" if setting_out else "nearly home"
    return ("setting out, " if setting_out else "returning, ") + where


def day_fraction(now: datetime) -> float:
    """Day tier: midnight = Pole 0, noon = Pole 1."""
    return (now.hour * 3600 + now.minute * 60 + now.second) / 86400


def year_fraction(now: datetime) -> float:
    """Year tier: December 21 = Pole 0, the midpoint (about June 21) = Pole 1."""
    start = datetime(now.year, 12, 21)
    if now < start:
        start = datetime(now.year - 1, 12, 21)
    end = datetime(start.year + 1, 12, 21)
    return (now - start) / (end - start)


# ADD YOUR OWN TIER HERE.
# Any closed cycle in your field works the same way:
#     fraction = (time since the cycle started) / (length of the cycle)
# Examples: a tide, a heartbeat, a machine duty cycle, an orbit, a school term.
# Then call tier_state(fraction) or tier_words(fraction).


def engine_line(now: datetime | None = None, words: bool = True) -> str:
    """One ENGINE line per turn: where each tier stands right now."""
    now = now or datetime.now()
    tiers = {"YEAR": year_fraction(now), "DAY": day_fraction(now)}
    if words:
        body = " ".join(f"{name}: {tier_words(f)}." for name, f in tiers.items())
    else:
        body = " ".join(
            f"{name}: phase {tier_state(f)['phase']}, compressed {tier_state(f)['compressed']:.6f}."
            for name, f in tiers.items())
    return "ENGINE: " + body


# ==================================================
# WIRE POINT 4: DIRECT ENGINE QUESTIONS
# For questions about the model itself, call the engine and hand the LLM the
# exact result. The LLM never does this arithmetic.
#   "totals"          counts, master chain, whole-sphere values
#   "state N"         state after counted operation N
#   "position S"      energy at position S
#   "local V S"       dense matter pocket or void (Nest 5)
# ==================================================
def engine_answer(query: str) -> str | None:
    """Return an exact ENGINE block for an engine query, or None if it is not one."""
    parts = query.strip().lower().replace(",", "").split()
    try:
        if parts == ["totals"]:
            result = cse.totals()
        elif len(parts) == 2 and parts[0] == "state":
            result = cse.state(int(parts[1]))
        elif len(parts) == 2 and parts[0] == "position":
            result = cse.position(int(parts[1]))
        elif len(parts) == 3 and parts[0] == "local":
            result = cse.local(float(parts[1]), int(parts[2]))
        else:
            return None
    except ValueError as e:
        return f"ENGINE: error: {e}"
    return "ENGINE:\n" + json.dumps(result, indent=2)


# ==================================================
# WIRE POINT 5: THE BRIDGE TO SCIENCE
# Nest 8 converts substrate units to human units. The engine already returns
# them under "observer_0". Use ratios when you compare with measurements;
# see EXAMPLES.md for the pattern and for its limits.
# ==================================================
def bridge(s: int) -> dict:
    """Position s in substrate units and in Observer 0 units (meters, joules)."""
    p = cse.position(s)
    return {
        "position": p["position"],
        "compressed_fraction": p["compressed"],
        "uncompressed_fraction": p["uncompressed"],
        "radius_meters": p["observer_0"]["radius_meters"],
        "compressed_joules": p["observer_0"]["compressed_joules"],
    }


# ==================================================
# WIRE POINT 6: THE MESSAGE LIST
# Order matters.
#   first : the constant prompt + the translator rule   (cached by the runtime)
#   then  : the conversation history
#   then  : the user's message
#   last  : the ENGINE lines for this turn              (nothing comes after them)
# ==================================================
def build_messages(user_message: str, history: list | None = None,
                   now: datetime | None = None) -> list:
    engine_parts = [engine_line(now)]
    exact = engine_answer(user_message)
    if exact:
        engine_parts.append(exact)
    return (
        [{"role": "system", "content": BASE_PROMPT + "\n\n" + TRANSLATOR_RULE}]
        + list(history or [])
        + [{"role": "user", "content": user_message}]
        + [{"role": "system", "content": "\n".join(engine_parts)}]
    )


# ==================================================
# WIRE POINT 7: YOUR LLM
# Replace the body with the call for your own runtime. Two common shapes:
#
#   llama-cpp-python:
#       out = model.create_chat_completion(messages=messages, temperature=0.3)
#       return out["choices"][0]["message"]["content"]
#
#   any OpenAI-style HTTP API:
#       POST {"model": "...", "messages": messages, "temperature": 0.3}
# ==================================================
def call_your_llm(messages: list) -> str:
    raise NotImplementedError("Wire your own LLM here. See WIRE POINT 7.")


# ==================================================
# DEMO: prints what your LLM would receive. No LLM is needed.
# ==================================================
if __name__ == "__main__":
    fixed_now = datetime(2026, 10, 1, 9, 30)   # a fixed moment, so the output is repeatable

    for question in ("Where does the day stand?", "position 676457349"):
        print("=" * 60)
        print("USER:", question)
        for m in build_messages(question, now=fixed_now):
            print(f"--- {m['role']} ---")
            print(m["content"])

    print("=" * 60)
    print("BRIDGE (WIRE POINT 5):")
    print(json.dumps(bridge(676457349), indent=2))
