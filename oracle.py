#!/usr/bin/env python3
# Work Rate Math oracle - mirrors engine.js using Fraction rates (sum of 1/t) instead of hand-rolled integer fractions.
import json, re
from fractions import Fraction

TIME_ERR = "each time must be a positive number of hours with at most 2 decimals, from 0.01 to 10000"

def _t(text):
    t = text.strip() if isinstance(text, str) else ""
    m = re.fullmatch(r"([0-9]+)(?:\.([0-9]{1,2}))?", t)
    if not m:
        raise ValueError(TIME_ERR)
    h = int(m.group(1)) * 100 + int((m.group(2) or "").ljust(2, "0"))
    if h < 1 or h > 1000000:
        raise ValueError(TIME_ERR)
    return t, Fraction(h, 100)  # hours

def time_text(x):  # x: Fraction hours
    s = int((x * 100 * 2 + 1) // 2)  # half up
    if s == 0:
        fig = "under 0.01"
    else:
        whole, frac = divmod(s, 100)
        fr = f"{frac:02d}".rstrip("0")
        fig = ("exactly " if (x * 100).denominator == 1 else "about ") + str(whole) + ("." + fr if fr else "")
    m = int((x * 60 * 2 + 1) // 2)
    return f"{fig} h, or {m // 60} h {m % 60} min to the nearest minute"

def lst(items):
    parts = [t + " h" for t, _ in items]
    return parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + " and " + parts[-1]

def together_truth(times):
    tokens = [x for x in re.split(r"[\s,]+", times if isinstance(times, str) else "") if x != ""]
    if len(tokens) < 2 or len(tokens) > 6:
        raise ValueError("enter 2 to 6 times, " + TIME_ERR)
    ts = [_t(x) for x in tokens]
    rate = sum(1 / h for _, h in ts)
    return f"Working together, {lst(ts)} finish one job in {time_text(1 / rate)}."

def other_truth(alone, together):
    a, ha = _t(alone); t, ht = _t(together)
    if ha <= ht:
        raise ValueError("the one worker's time must be longer than the together time, because working together is always faster than working alone")
    x = 1 / (1 / ht - 1 / ha)
    return f"If one worker alone takes {a} h and both together take {t} h, the other worker alone takes {time_text(x)}."

def pipe_truth(fill, drain):
    f, hf = _t(fill); d, hd = _t(drain)
    head = f"An inlet that fills the tank in {f} h and an outlet that drains it in {d} h, both open, "
    net = 1 / hf - 1 / hd
    if net == 0:
        return head + "cancel out: the level never changes."
    if net > 0:
        return head + f"fill an empty tank in {time_text(1 / net)}."
    return head + f"empty a full tank in {time_text(1 / -net)}."

FNS = {"togetherTruth": together_truth, "otherTruth": other_truth, "pipeTruth": pipe_truth}
CASES = [
    ("togetherTruth", ["6, 3"]), ("togetherTruth", ["6 3"]), ("togetherTruth", ["4,4"]), ("togetherTruth", ["10, 15"]),
    ("togetherTruth", ["3, 4, 5"]), ("togetherTruth", ["1, 1, 1, 1, 1, 1"]), ("togetherTruth", ["0.01, 0.01"]), ("togetherTruth", ["10000, 10000"]),
    ("togetherTruth", ["0.01,0.01,0.01,0.01,0.01,0.01"]), ("togetherTruth", ["2.5, 1.25"]), ("togetherTruth", [" 7 , 9 "]), ("togetherTruth", ["1.5, 2.75, 4"]),
    ("togetherTruth", ["8, 12, 24"]), ("togetherTruth", ["9999.99, 10000"]), ("togetherTruth", ["1, 2, 3, 4"]), ("togetherTruth", ["5, 7"]),
    ("togetherTruth", ["6"]), ("togetherTruth", ["1, 1, 1, 1, 1, 1, 1"]), ("togetherTruth", [""]), ("togetherTruth", ["6, 0"]),
    ("togetherTruth", ["6, -3"]), ("togetherTruth", ["6, abc"]), ("togetherTruth", ["6, 10000.01"]), ("togetherTruth", ["6, 1.234"]),
    ("otherTruth", ["6", "2"]), ("otherTruth", ["10", "4"]), ("otherTruth", ["3", "2"]), ("otherTruth", ["5", "4"]),
    ("otherTruth", ["10000", "0.01"]), ("otherTruth", ["0.02", "0.01"]), ("otherTruth", ["7", "3.5"]), ("otherTruth", ["9999.99", "9999.98"]),
    ("otherTruth", ["2", "2"]), ("otherTruth", ["2", "3"]), ("otherTruth", ["abc", "2"]), ("otherTruth", ["6", "0"]),
    ("pipeTruth", ["3", "6"]), ("pipeTruth", ["6", "3"]), ("pipeTruth", ["4", "4"]), ("pipeTruth", ["5", "7"]),
    ("pipeTruth", ["7", "5"]), ("pipeTruth", ["0.01", "10000"]), ("pipeTruth", ["10000", "0.01"]), ("pipeTruth", ["1.5", "2.25"]),
    ("pipeTruth", ["2", "2.01"]), ("pipeTruth", ["abc", "2"]), ("pipeTruth", ["2", ""]), ("pipeTruth", ["0", "2"]),
]

out = []
for fn, args in CASES:
    try:
        exp = FNS[fn](*args)
    except ValueError as e:
        exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    json.dump(out, f, indent=1)
    f.write("\n")
print(len(out), "cases")
