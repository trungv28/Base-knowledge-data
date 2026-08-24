import ast, json
from pathlib import Path

HERE = Path(__file__).parent
ORDER = ["id", "atoms", "template", "cases", "vars", "derive", "constraints",
         "solver", "graph"]


def load(path):
    return [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]


def wiring(expr, prior, question_vars):
    names = {n.id for n in ast.walk(ast.parse(expr, mode="eval"))
             if isinstance(n, ast.Name)}
    ins = {}
    for nm in sorted(names):
        if nm in prior:
            ins[nm] = {"source": nm, "field": "value", "type": "expression"}
        elif nm in question_vars:
            ins[nm] = {"source": "question", "field": nm, "type": "expression"}
    return ins


def build(composite_path=None, graphs_path=None):
    composite_path = composite_path or HERE / "composite.jsonl"
    graphs_path = graphs_path or HERE / "graphs.jsonl"
    graphs = {g["id"]: g["nodes"] for g in load(graphs_path)}

    out, done, missing = [], 0, []
    for c in load(composite_path):
        spec = graphs.get(c["id"])
        if spec is None:
            missing.append(c["id"])
            out.append(json.dumps(c, separators=(",", ":"),
                                  ensure_ascii=False) + "\n")
            continue
        qvars = set(c.get("vars") or {}) | set(c.get("derive") or {})
        for case in (c.get("cases") or []):
            qvars |= set(case)
        nodes, prior = [], set()
        for n in spec:
            nid, expr = n["node_id"], n["expr"]
            nodes.append({
                "node_id": nid,
                "atom_id": n["atom_id"],
                "inputs": wiring(expr, prior, qvars),
                "expr": expr,
                "outputs": {"value": {"type": "expression"}},
                "executor": f"expr:{c['id']}.{nid}",
                "verifier": f"exact:{c['id']}.{nid}",
            })
            prior.add(nid)
        c["graph"] = {"nodes": nodes, "final": f"{spec[-1]['node_id']}.value"}
        c = {k: c[k] for k in ORDER if k in c}
        out.append(json.dumps(c, separators=(",", ":"),
                              ensure_ascii=False) + "\n")
        done += 1

    open(composite_path, "w", encoding="utf-8").writelines(out)
    print(f"annotated {done} composites; unannotated: {len(missing)} {missing}")


if __name__ == "__main__":
    build()
