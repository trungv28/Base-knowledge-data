import argparse, ast, collections, inspect, random, re, sys
from pathlib import Path

import generate
import solver
import validate

HERE = Path(__file__).parent
DRAWS = 200


def parents(nodes):
    ids = {n["node_id"] for n in nodes}
    return {n["node_id"]: {x.id for x in ast.walk(ast.parse(n["expr"], mode="eval"))
                           if isinstance(x, ast.Name)} & ids for n in nodes}


def shown(t):
    names = set(re.findall(r"\{(\w+)\}", t["template"]))
    for _ in range(len(t.get("derive") or {})):
        for nm, ex in (t.get("derive") or {}).items():
            if nm in names:
                names |= {x.id for x in ast.walk(ast.parse(ex, mode="eval"))
                          if isinstance(x, ast.Name)}
    return names


def check(t, covered):
    nodes = t["graph"]["nodes"]
    ids = [n["node_id"] for n in nodes]
    par = parents(nodes)
    qvars = set(t.get("vars") or {}) | set(t.get("derive") or {})
    out = []

    def rule(n, name, ok, detail=""):
        out.append((n, name, ok, detail))

    rule(1, "connected and acyclic", not validate.check_graph(t["graph"]),
         "; ".join(validate.check_graph(t["graph"])))
    dead = [f"{n['node_id']} = {n['expr']}" for n in nodes
            if n["expr"].strip() in par[n["node_id"]]
            or n["expr"].strip() in {f"str({p})" for p in par[n["node_id"]]}]
    rule(2, "every step computes something", not dead, ", ".join(dead))

    copies = {n["node_id"] for n in nodes if n["expr"].strip() in qvars}

    def depth(nid):
        return 0 if nid in copies else 1 + max([depth(p) for p in par[nid]], default=0)
    d = max(depth(n) for n in ids)
    rule(3, "depth at least two", d >= 2, f"depth {d}, {len(copies)} copied from question")

    atoms = {n["atom_id"] for n in nodes if n["atom_id"] and n["atom_id"] != "arithmetic"}
    rule(4, "at least two different atoms", len(atoms) >= 2, f"{len(atoms)} real atoms")
    rule(7, "every atom has an atomic template", not (atoms - covered),
         ", ".join(sorted(atoms - covered)))

    fn = getattr(solver, t["solver"])
    params = inspect.signature(fn).parameters
    answers = collections.Counter()
    equal_parent = collections.Counter()
    missing = set()
    crash = ""
    for _ in range(DRAWS):
        try:
            vals = generate.sample(t)
            got, outs = generate.run_graph(t, vals)
            gold = fn(**{k: vals[k] for k in params if k in vals})
        except Exception as e:
            crash = f"{type(e).__name__}: {e}"
            break
        if str(got) != str(gold):
            crash = f"graph={got!r} solver={gold!r}"
            break
        answers[str(gold)] += 1
        for n in nodes:
            for p in par[n["node_id"]]:
                if str(outs[n["node_id"]]) == str(outs[p]):
                    equal_parent[f"{n['node_id']}=={p}"] += 1
        q = t["template"].format(**vals)
        seen = shown(t)
        for n in nodes:
            for nm, src in n["inputs"].items():
                if src["source"] == "question" and str(vals.get(src["field"], "")) \
                        not in q and src["field"] not in seen:
                    missing.add(src["field"])
    rule(10, "exact, and graph agrees with solver", not crash, crash)
    rule(11, "every value a step reads is in the question", not missing, ", ".join(sorted(missing)))
    noop = [f"{k} on {v * 100 // DRAWS}% of draws"
            for k, v in equal_parent.items() if v > DRAWS * 0.9]
    rule(12, "no step repeats its input", not noop, ", ".join(noop))
    if answers:
        top, n = answers.most_common(1)[0]
        rule(13, "final answer varies", n / DRAWS <= 0.6,
             f"{top!r} on {n / DRAWS:.0%}, {len(answers)} distinct")
    return out, answers, identity_candidates(t)


def identity_candidates(t):
    read = set()
    for n in t["graph"]["nodes"]:
        read |= {x.id for x in ast.walk(ast.parse(n["expr"], mode="eval"))
                 if isinstance(x, ast.Name)}
    for ex in (t.get("derive") or {}).values():
        read |= {x.id for x in ast.walk(ast.parse(ex, mode="eval"))
                 if isinstance(x, ast.Name)}
    out = []
    for k, r in (t.get("vars") or {}).items():
        if k not in read:
            continue
        vals = (r["values"] if r["type"] == "choice"
                else [v for v in range(r["min"], r["max"] + 1)
                      if v not in {x for x in r.get("exclude", []) if not isinstance(x, str)}])
        hit = sorted({v for v in vals if v in (0, 1)})
        if hit:
            out.append(f"{k} can be {', '.join(map(str, hit))}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("id", nargs="?")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    random.seed(args.seed)

    tem = generate.load(HERE / "templates.jsonl")
    comp = generate.load(HERE / "composite.jsonl")
    covered = {t["atom"] for t in tem if hasattr(solver, t["solver"])}
    if args.id:
        comp = [c for c in comp if c["id"] == args.id]
        if not comp:
            raise SystemExit(f"no composite with id {args.id!r}")

    worst = 0
    for t in comp:
        out, answers, ident = check(t, covered)
        failed = [r for r in out if not r[2]]
        worst = max(worst, len(failed))
        print(f"\n{t['id']}   {'OK' if not failed else str(len(failed)) + ' FAILED'}")
        for n, name, ok, detail in out:
            tag = "test " + str(n)
            print(f"  {'pass' if ok else 'FAIL'}  {tag:8} {name}"
                  + (f"   [{detail}]" if detail else ""))
        if ident:
            print("  test 12 by eye: " + "; ".join(ident)
                  + "  -- does any of these make a step do nothing?")
        if args.id and answers:
            print("  answers: " + ", ".join(f"{a!r}x{c}" for a, c in answers.most_common(5)))
    return 1 if worst else 0


if __name__ == "__main__":
    sys.exit(main())
