"""Find a slot order for the chart palette whose adjacent pairs all clear the
CVD separation floor.

The validator checks *adjacent* slot pairs by default, so slot order is part of
the specification, not an afterthought. Rather than guess orderings by eye, this
imports the validator's own deltaE and searches for the permutation that
maximises the weakest adjacent pair.

Usage: find-chart-order.py "#hex,#hex,..." [--surface HEX] [--mode light|dark]
"""
import argparse
import importlib.util
import itertools
import os
import sys

SKILL = os.environ.get("DATAVIZ_SKILL")
if not SKILL or not os.path.exists(os.path.join(SKILL, "scripts/validate_palette.py")):
    sys.exit("set DATAVIZ_SKILL to the dataviz skill base directory")

spec = importlib.util.spec_from_file_location(
    "vp", os.path.join(SKILL, "scripts/validate_palette.py"))
vp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vp)

ap = argparse.ArgumentParser()
ap.add_argument("palette")
ap.add_argument("--surface", default="#FBF8F1")
ap.add_argument("--mode", default="light")
ap.add_argument("--top", type=int, default=5)
a = ap.parse_args()

cols = [c.strip() for c in a.palette.split(",") if c.strip()]
n = len(cols)

# worst-case separation for a pair across the simulated vision types the
# validator scores, plus unsimulated
KINDS = [None, "protan", "deutan", "tritan"]


def pair_score(x, y):
    return min(vp.deltaE(x, y, k) for k in KINDS)


P = {(i, j): pair_score(cols[i], cols[j]) for i in range(n) for j in range(n) if i != j}

best = []
first = 0  # anchor slot 1 so the brand colour keeps position 1
for perm in itertools.permutations(range(1, n)):
    order = (first,) + perm
    worst = min(P[(order[k], order[k + 1])] for k in range(n - 1))
    best.append((worst, order))
best.sort(key=lambda t: -t[0])

seen = set()
print(f"anchored slot 1 = {cols[first]}; {len(best)} orderings scored\n")
for worst, order in best[: a.top]:
    key = tuple(order)
    if key in seen:
        continue
    seen.add(key)
    pal = ",".join(cols[i] for i in order)
    print(f"worst adjacent ΔE {worst:5.1f}   {pal}")

print("\nweakest pairs overall (any position):")
flat = sorted({tuple(sorted((i, j))): P[(i, j)] for i in range(n) for j in range(n) if i != j}.items(),
              key=lambda kv: kv[1])
for (i, j), v in flat[:5]:
    print(f"  {cols[i]} <-> {cols[j]}  ΔE {v:.1f}")
