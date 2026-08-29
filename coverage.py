import collections, json, sys
from pathlib import Path

import generate

HERE = Path(__file__).parent
FLOOR_COVERED = 0.70      # share of templated atoms that must appear in a composite
FLOOR_REUSE = 2           # composites per atom, once it is used at all
CEILING_SHARE = 0.25      # no single atom in more than this share of composites


def main():
    tem = generate.load(HERE / "templates.jsonl")
    comp = generate.load(HERE / "composite.jsonl")
    templated = {t["atom"] for t in tem}
    use = collections.Counter(a for c in comp for a in c["atoms"])
    used = set(use)

    covered = len(used & templated) / len(templated)
    thin = sorted(a for a, k in use.items() if k < FLOOR_REUSE)
    hot = [(a, k) for a, k in use.most_common() if k / len(comp) > CEILING_SHARE]
    missing = sorted(templated - used)

    print(f"composites {len(comp)}   templated atoms {len(templated)}   "
          f"used by a composite {len(used & templated)}")
    print()
    ok = True
    def check(name, good, detail=""):
        nonlocal ok
        ok = ok and good
        print(f"  {'pass' if good else 'FAIL'}  {name}{('   ' + detail) if detail else ''}")

    check(f"coverage >= {FLOOR_COVERED:.0%}", covered >= FLOOR_COVERED, f"{covered:.0%}")
    check(f"every used atom in >= {FLOOR_REUSE} composites", not thin,
          f"{len(thin)} below: {', '.join(thin[:4])}{' ...' if len(thin) > 4 else ''}")
    check(f"no atom in > {CEILING_SHARE:.0%} of composites", not hot,
          "; ".join(f"{a} {k}/{len(comp)}" for a, k in hot[:3]))

    print(f"\n  atoms with a template but no composite: {len(missing)}")
    for a in missing[:12]:
        print(f"     {a}")
    if len(missing) > 12:
        print(f"     ... and {len(missing) - 12} more")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
