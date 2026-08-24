import argparse, collections, inspect, itertools, json, random, sys
from pathlib import Path

import generate
import solver

HERE = Path(__file__).parent
ENUM_LIMIT = 200_000
MC_DRAWS = 4_000


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
    doms = domains(t)
    cases = t.get("cases") or [None]
    raw = len(cases)
    for _, vs in doms:
        raw *= len(vs)
    sym = any(isinstance(x, str)
              for r in (t.get("vars") or {}).values() for x in r.get("exclude", []))
    if not t.get("constraints") and not sym:
        return raw, True
    if raw <= ENUM_LIMIT:
        n = 0
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
                for name, expr in (t.get("derive") or {}).items():
                    vals[name] = generate.evaluate(expr, vals)
                if all(generate.evaluate(c, vals) for c in (t.get("constraints") or [])):
                    n += 1
        return n, True
    hits = 0
    for _ in range(MC_DRAWS):
        try:
            generate.sample(t)
            hits += 1
        except Exception:
            pass
    return round(raw * hits / MC_DRAWS), False


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
            key = json.dumps(a, sort_keys=True, default=str)
            if seen.setdefault(q, key) != key:
                bad("determinism", t["id"], "same question, two different answers")
                break

    for c in comp:
        g = c.get("graph")
        if not g:
            bad("graphs", c["id"], "no graph annotation")
            continue
        for p in check_graph(g):
            bad("graphs", c["id"], p)
        used = {n["atom_id"] for n in g["nodes"]}
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
                if nid != final and isinstance(o, (list, tuple, dict, bool)):
                    bad("graphs", c["id"],
                        f"node {nid} emits a non-scalar {type(o).__name__}; "
                        f"intermediate outputs must round-trip as text")
                    break
            question = c["template"].format(**vals)
            for node in c["graph"]["nodes"]:
                for name, src in node["inputs"].items():
                    if src["source"] != "question":
                        continue
                    val = str(vals.get(src["field"], ""))
                    if val and val not in question:
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

    small = []
    for t in tem + comp:
        n, exact = support(t)
        if n < 128:
            small.append((t["id"], n, "exact" if exact else "approx"))
    print(f"\ntemplates that cannot make 128 distinct questions: {len(small)}")
    for i, n, e in sorted(small, key=lambda x: x[1])[:15]:
        print(f"   {i:<46} {n:>6}  ({e})")
    if len(small) > 15:
        print(f"   ... and {len(small) - 15} more")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
