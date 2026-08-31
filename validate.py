import ast, re
import argparse, collections, inspect, itertools, json, random, sys
from pathlib import Path

import generate
import annotate_graphs
import solver

HERE = Path(__file__).parent
ENUM_LIMIT = 200_000
MC_DRAWS = 4_000
MIN_SUPPORT = 128


def domains(t):
    out = []
    for k, r in (t.get("vars") or {}).items():
        if r["type"] == "choice":
            out.append((k, list(r["values"])))
        else:
            drop = {x for x in r.get("exclude", []) if not isinstance(x, str)}
            out.append((k, [v for v in range(r["min"], r["max"] + 1) if v not in drop]))
    return out


def support(t):
    """Distinct rendered questions, per guide 8.4 -- not distinct parameter
    assignments. Two assignments that render the same text are one question, so
    a variable the template never prints inflates the assignment count without
    adding a single instance."""
    doms = domains(t)
    cases = t.get("cases") or [None]
    raw = len(cases)
    for _, vs in doms:
        raw *= len(vs)
    if raw <= ENUM_LIMIT:
        seen = set()
        for case in cases:
            for combo in itertools.product(*[vs for _, vs in doms]):
                vals = dict(case) if case else {}
                ok = True
                for (k, _), v in zip(doms, combo):
                    rule = t["vars"][k]
                    bad = {vals[x] for x in rule.get("exclude", [])
                           if isinstance(x, str) and x in vals}
                    if v in bad:
                        ok = False
                        break
                    vals[k] = v
                if not ok:
                    continue
                try:
                    for name, expr in (t.get("derive") or {}).items():
                        vals[name] = generate.evaluate(expr, vals)
                    if not all(generate.evaluate(c, vals)
                               for c in (t.get("constraints") or [])):
                        continue
                    seen.add(t["template"].format(**generate.enrich(dict(vals))))
                except Exception:
                    continue
        return len(seen), True
    # too large to enumerate: draw until MIN_SUPPORT distinct questions actually
    # appear. Never extrapolate from the raw domain -- scaling by an unconstrained
    # domain reported 25,000 for a template whose true support was 100.
    seen = set()
    for _ in range(MC_DRAWS):
        try:
            seen.add(t["template"].format(**generate.sample(t)))
        except Exception:
            pass
        if len(seen) >= MIN_SUPPORT:
            return len(seen), True          # threshold met: no estimate needed
    return len(seen), False                 # a floor, not an estimate


def canonical(v):
    """One exact value that survives being written out and read back.

    Scalars (int, str, Fraction, sympy) pass; a tuple passes only if canon() and
    parse_struct() reproduce it. dict, list, set, bool and float never do."""
    if isinstance(v, bool) or isinstance(v, float):
        return False
    if isinstance(v, tuple):
        return generate.round_trips(v)
    if isinstance(v, (dict, list, set)):
        return False
    return True


def graph_edges(g):
    ids = [n["node_id"] for n in g["nodes"]]
    edges = set()
    for n in g["nodes"]:
        for spec in n["inputs"].values():
            if spec["source"] in ids:
                edges.add((spec["source"], n["node_id"]))
    return ids, edges


def check_graph(g):
    problems = []
    ids, edges = graph_edges(g)
    if len(set(ids)) != len(ids):
        problems.append("duplicate node_id")
    final = g["final"].split(".")[0]
    if final not in ids:
        problems.append(f"final {final!r} is not a node")
        return problems
    adj = collections.defaultdict(set)
    for a, b in edges:
        adj[a].add(b)
    pos = {n: i for i, n in enumerate(ids)}
    if any(pos[a] >= pos[b] for a, b in edges):
        problems.append("cycle or forward reference")
    reaches = {final}
    for n in reversed(ids):
        if adj[n] & reaches:
            reaches.add(n)
    orphans = [n for n in ids if n not in reaches]
    if orphans:
        problems.append(f"nodes not on a path to final: {orphans}")
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--draws", type=int, default=25, help="samples per template")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    random.seed(args.seed)

    atoms = generate.load(HERE / "atoms.jsonl")
    tem = generate.load(HERE / "templates.jsonl")
    comp = generate.load(HERE / "composite.jsonl")
    atom_ids = {a["id"] for a in atoms}
    fail = []

    def bad(kind, tid, msg):
        fail.append(f"[{kind}] {tid}: {msg}")

    # 12.1: a name in both cases and vars is sampled over its case value, so a
    # question can state a premise the answer contradicts.
    for t in tem + comp:
        for case in (t.get("cases") or []):
            ov = sorted(set(case) & set(t.get("vars") or {}))
            if ov:
                bad("cases", t["id"], f"also sampled in vars: {', '.join(ov)}")
                break

    # 5: a string exclusion silently does nothing if the name it reads has not
    # been sampled yet, and a derive that reads an undeclared name only shows up
    # as a mystery rejection. Both are declaration-order traps -- fail on them.
    for t in tem + comp:
        seen_vars = set(t.get("cases") and t["cases"][0] or {})
        for k, rule in (t.get("vars") or {}).items():
            for e in rule.get("exclude", []):
                if isinstance(e, str) and e not in seen_vars:
                    bad("order", t["id"],
                        f"{k} excludes {e!r}, which is not sampled before it")
            seen_vars.add(k)
        known = seen_vars | set(generate.SAFE)
        try:
            for name in generate.derive_order(t.get("derive") or {}):
                expr = t["derive"][name]
                for n in ast.walk(ast.parse(expr, mode="eval")):
                    if isinstance(n, ast.Name) and n.id not in known:
                        bad("order", t["id"],
                            f"derive {name} reads {n.id!r}, which is not defined")
                known.add(name)
        except ValueError as e:
            bad("order", t["id"], str(e))

    # A pack is one unit; eight are merged later, so the merge key is
    # (unit, id). That is unique only if every record names its unit and ids do
    # not repeat inside the pack.
    for kind, rows in (("atoms", atoms), ("atomic", tem), ("composite", comp)):
        seen = set()
        for r in rows:
            if not r.get("unit"):
                bad("unit", r["id"], "no unit field")
            if r["id"] in seen:
                bad("unit", r["id"], f"duplicate {kind} id")
            seen.add(r["id"])
    dup = ({t["id"] for t in tem} & {c["id"] for c in comp}) | \
          ({a["id"] for a in atoms} & ({t["id"] for t in tem} | {c["id"] for c in comp}))
    for d in sorted(dup):
        bad("unit", d, "id used by more than one record kind")
    units = {r.get("unit") for r in atoms + tem + comp if r.get("unit")}
    if len(units) > 1:
        bad("unit", "pack", f"one pack is one unit, found {sorted(units)}")

    # graphs.jsonl is the source; composite.jsonl carries an expansion of it.
    # Rebuild in memory and diff, so an edited spec that was never re-annotated
    # fails here instead of silently validating the old graph.
    specs = {g["id"]: g["nodes"] for g in generate.load(HERE / "graphs.jsonl")}
    for gid in sorted(set(specs) - {c["id"] for c in comp}):
        bad("graphs", gid, "graph spec has no composite in composite.jsonl")
    fresh, ungraphed = annotate_graphs.expand(comp, specs)
    for cid in ungraphed:
        bad("graphs", cid, "composite has no graph spec in graphs.jsonl")
    for old, new in zip(comp, fresh):
        if old.get("graph") != new.get("graph") or old.get("atoms") != new.get("atoms"):
            bad("graphs", old["id"],
                "stale against graphs.jsonl -- run: python3 annotate_graphs.py")

    for t in tem:
        if t["atom"] not in atom_ids:
            bad("references", t["id"], f"unknown atom {t['atom']}")
        if not hasattr(solver, t["solver"]):
            bad("references", t["id"], f"missing solver {t['solver']}")
    for c in comp:
        for a in c["atoms"]:
            if a not in atom_ids:
                bad("references", c["id"], f"unknown atom {a}")
        if not hasattr(solver, c["solver"]):
            bad("references", c["id"], f"missing solver {c['solver']}")

    for t in tem + comp:
        seen = {}
        for _ in range(args.draws):
            try:
                q, a = generate.make(t)
            except Exception as e:
                bad("generation", t["id"], f"{type(e).__name__}: {e}")
                break
            if not canonical(a):
                bad("answer", t["id"],
                    f"answer is {type(a).__name__} {a!r}; an answer must be one "
                    f"canonical value (no dict, list, set, bool or float)")
                break
            key = json.dumps(a, sort_keys=True, default=str)
            if seen.setdefault(q, key) != key:
                bad("determinism", t["id"], "same question, two different answers")
                break

    # 10: the same question under two templates -- worse when their atom labels
    # differ, since the two rows then teach contradictory credit for one question
    origin = {}
    for t in tem + comp:
        for _ in range(args.draws):
            try:
                q = t["template"].format(**generate.sample(t))
            except Exception:
                break
            prev = origin.setdefault(q, t["id"])
            if prev != t["id"]:
                bad("duplicate", t["id"], f"renders a question {prev} also renders: {q!r}")
                break

    for c in comp:
        g = c.get("graph")
        if not g:
            bad("graphs", c["id"], "no graph annotation")
            continue
        for p in check_graph(g):
            bad("graphs", c["id"], p)
        for n in g["nodes"]:
            if not n.get("atom_id"):
                bad("graphs", c["id"],
                    f"node {n['node_id']} has no atom_id; name the atom it applies, "
                    f"or \"arithmetic\" if the step is only arithmetic")
        used = {n["atom_id"] for n in g["nodes"]
                if n.get("atom_id") and n["atom_id"] != "arithmetic"}
        if used - set(c["atoms"]):
            bad("graphs", c["id"], f"graph uses atoms not declared: {used - set(c['atoms'])}")
        if set(c["atoms"]) - used:
            bad("graphs", c["id"], f"declared atoms unused by graph: {set(c['atoms']) - used}")
        fn = getattr(solver, c["solver"])
        params = inspect.signature(fn).parameters
        for _ in range(args.draws):
            try:
                vals = generate.sample(c)
                gold = fn(**{k: vals[k] for k in params if k in vals})
                got, _ = generate.run_graph(c, vals)
            except Exception as e:
                bad("crosscheck", c["id"], f"{type(e).__name__}: {e}")
                break
            if json.dumps(got, sort_keys=True, default=str) != \
               json.dumps(gold, sort_keys=True, default=str):
                bad("crosscheck", c["id"], f"solver={gold!r} graph={got!r}")
                break
            _, outs = generate.run_graph(c, vals)
            final = c["graph"]["final"].split(".")[0]
            for nid, o in outs.items():
                # every node, final included: what a node emits has to survive the
                # model's text trace, and a float is never exact
                if not canonical(o):
                    bad("graphs", c["id"],
                        f"node {nid} emits {type(o).__name__} {o!r}, which is not one "
                        f"canonical exact value")
                    break
            question = c["template"].format(**vals)
            # a value can be shown through a derived display string ("3 units left"
            # encodes shift_val=-3), so treat vars feeding a printed derive as shown
            shown_vars = set(re.findall(r"\{(\w+)\}", c["template"]))
            for _ in range(len(c.get("derive") or {})):
                for nm, ex in (c.get("derive") or {}).items():
                    if nm in shown_vars:
                        shown_vars |= {x.id for x in ast.walk(ast.parse(ex, mode="eval"))
                                       if isinstance(x, ast.Name)}
            for node in c["graph"]["nodes"]:
                for name, src in node["inputs"].items():
                    if src["source"] != "question":
                        continue
                    val = str(vals.get(src["field"], ""))
                    shown = question.replace("−", "-").replace("+ ", "+")
                    shown = re.sub(r"- (?=\d)", "-", shown)
                    if val and val not in shown and src["field"] not in shown_vars:
                        bad("graphs", c["id"],
                            f"node {node['node_id']} binds {src['field']}={val!r}, "
                            f"which the question never shows")

    covered = {t["atom"] for t in tem if hasattr(solver, t["solver"])}
    for c in comp:
        for a in set(c["atoms"]) - covered:
            bad("coverage", c["id"], f"atom {a} has no working atomic template")

    print(f"atoms {len(atoms)}   atomic {len(tem)}   composite {len(comp)}")
    if fail:
        print(f"\nFAILED ({len(fail)}):")
        for f in fail:
            print("  " + f)
    else:
        print("all checks passed")

    # 8.4: a standard template must make 128 distinct questions. A genuinely
    # finite one is allowed through only if it says so, and the lead reviews the
    # flag -- an undeclared shortfall is a failure, not a note.
    small, stale = [], []
    for t in tem + comp:
        n, exact = support(t)
        if n < MIN_SUPPORT and not t.get("finite_support"):
            small.append((t["id"], n, "exact" if exact else "approx"))
        elif n >= MIN_SUPPORT and t.get("finite_support"):
            stale.append((t["id"], n))
    declared = sum(1 for t in tem + comp if t.get("finite_support"))
    print(f"\nfinite_support declared: {declared}   "
          f"(excluded from the 8.4 target; lead must approve each)")
    if small:
        print(f"\nFAILED: {len(small)} templates make under {MIN_SUPPORT} distinct "
              f"questions and are not marked finite_support")
        for i, n, e in sorted(small, key=lambda x: x[1]):
            print(f"   {i:<46} {n:>6}  ({e})")
    if stale:
        print(f"\nFAILED: {len(stale)} marked finite_support but reach "
              f"{MIN_SUPPORT}; drop the flag")
        for i, n in stale:
            print(f"   {i:<46} {n:>6}")
    return 1 if (fail or small or stale) else 0


if __name__ == "__main__":
    sys.exit(main())
