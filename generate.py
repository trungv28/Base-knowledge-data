import argparse, inspect, json, math, random
from fractions import Fraction
from pathlib import Path
import sympy
import solver

def term(coef, suffix=""):
    if coef == 0:
        return ""
    body = suffix if abs(coef) == 1 and suffix else f"{abs(coef)}{suffix}"
    return f" {'−' if coef < 0 else '+'} {body}"


def linfac(a, v="x"):
    return f"({v} − {a})" if a > 0 else f"({v} + {-a})"


def shift(v, pos, neg):
    return f"{abs(v)} unit{'' if abs(v) == 1 else 's'} {pos if v > 0 else neg}"


SAFE = {
    "abs": abs, "min": min, "max": max, "int": int, "str": str, "len": len,
    "sum": sum, "sorted": sorted, "set": set, "range": range, "bool": bool,
    "all": all, "any": any,
    "comb": math.comb, "gcd": math.gcd,
    "Fraction": Fraction, "sqrt": sympy.sqrt,
    "pi": sympy.pi, "ceiling": sympy.ceiling,
    "pf": solver.pf,
    "ordinal": solver.ordinal,
    "pi_coeff": solver._pi_coeff_str,
    "sin_base_angle": solver.sin_base_angle,
    "poly_factor_theorem": solver.poly_factor_theorem,
    "poly_degree": solver.poly_degree,
    "poly_leading_coefficient": solver.poly_leading_coefficient,
    "poly_coefficient": solver.poly_coefficient,
    "poly_cubic_factor_quotient": solver.poly_cubic_factor_quotient,
    "term": term, "linfac": linfac, "shift": shift,
}

MAX_TRIES = 500


def run_graph(t, vals):
    g = t.get("graph")
    if not g:
        return None, None
    env, outs = dict(vals), {}
    for node in g["nodes"]:
        v = evaluate(node["expr"], env)
        outs[node["node_id"]] = v
        env[node["node_id"]] = v
    return outs[g["final"].split(".")[0]], outs


def load(path):
    with open(path) as f:
        return [json.loads(x) for x in f if x.strip()]


def evaluate(expr, vals):
    return eval(expr, {"__builtins__": {}}, {**SAFE, **vals})


def sample_var(rule, ctx):
    if rule["type"] == "choice":
        return random.choice(rule["values"])
    if rule["type"] == "int":
        drop = {ctx[x] if isinstance(x, str) else x for x in rule.get("exclude", [])
                if not isinstance(x, str) or x in ctx}
        vals = [v for v in range(rule["min"], rule["max"] + 1) if v not in drop]
        if not vals:
            raise ValueError("empty domain")
        return random.choice(vals)
    raise ValueError(rule["type"])


def sample(t):
    for _ in range(MAX_TRIES):
        vals = {}
        if t.get("cases"):
            vals.update(random.choice(t["cases"]))
        for k, r in (t.get("vars") or {}).items():
            vals[k] = sample_var(r, vals)
        for name, expr in (t.get("derive") or {}).items():
            vals[name] = evaluate(expr, vals)
        if all(evaluate(c, vals) for c in (t.get("constraints") or [])):
            return enrich(vals)
    raise RuntimeError(f"{t['id']}: no assignment satisfied constraints in {MAX_TRIES} tries")


def pi_frac(n, d=1):
    from fractions import Fraction
    f = Fraction(n, d)
    if f == 0:
        return "0"
    if f == 1:
        return "pi"
    if f == -1:
        return "-pi"
    if f.denominator == 1:
        return f"{f.numerator}*pi"
    if f.numerator == 1:
        return f"pi/{f.denominator}"
    if f.numerator == -1:
        return f"-pi/{f.denominator}"
    return f"{f.numerator}*pi/{f.denominator}"


def lin_x(b, c):
    if b == 1:
        s = "x"
    elif b == -1:
        s = "-x"
    else:
        s = f"{b}x"
    if c > 0:
        return f"{s}+{c}"
    if c < 0:
        return f"{s}{c}"
    return s


def shift_x(c):
    return lin_x(1, c)


def term_x(coef, c):
    if coef == "1":
        s = "x"
    elif coef == "-1":
        s = "-x"
    else:
        s = f"{coef}*x"
    if c > 0:
        return f"{s}+{c}"
    if c < 0:
        return f"{s}{c}"
    return s


def sin_model(A, arg, d0):
    if A == 1:
        s = f"sin({arg})"
    elif A == -1:
        s = f"-sin({arg})"
    else:
        s = f"{A}sin({arg})"
    if d0 > 0:
        return f"{s}+{d0}"
    if d0 < 0:
        return f"{s}{d0}"
    return s


def enrich(vals):
    if "b" in vals and "c" in vals:
        vals["lin"] = lin_x(int(vals["b"]), int(vals["c"]))
    if "c" in vals:
        vals["xshift"] = shift_x(int(vals["c"]))
    if {"bn", "bd", "c"}.issubset(vals):
        vals["omega"] = pi_frac(int(vals["bn"]), int(vals["bd"]))
        vals["arg"] = term_x(vals["omega"], int(vals["c"]))
    if {"A", "arg", "d0"}.issubset(vals):
        vals["model"] = sin_model(int(vals["A"]), vals["arg"], int(vals["d0"]))
    return vals


def make(t):
    vals = sample(t)
    fn = getattr(solver, t["solver"])
    names = inspect.signature(fn).parameters
    args = {k: vals[k] for k in names if k in vals}
    return t["template"].format(**vals), fn(**args)


def instances(t, want, tries_per_hit=40):
    fn = getattr(solver, t["solver"])
    params = inspect.signature(fn).parameters
    seen, rows = set(), []
    for _ in range(want * tries_per_hit):
        if len(rows) >= want:
            break
        vals = sample(t)
        q = t["template"].format(**vals)
        if q in seen:
            continue
        seen.add(q)
        answer = fn(**{k: vals[k] for k in params if k in vals})
        _, node_outputs = run_graph(t, vals)
        rows.append((q, answer, node_outputs, vals))
    return rows


def all_templates(d):
    rows = []
    for name in ("templates.jsonl", "composite.jsonl"):
        f = d / name
        if f.exists():
            rows += load(f)
    return rows


def main():
    p = argparse.ArgumentParser(
        description="Generate sample questions from the templates.")
    p.add_argument("--id", help="only this template id")
    p.add_argument("-n", "--num", type=int, default=3,
                   help="samples per template (default 3)")
    p.add_argument("--seed", type=int, default=1)
    p.add_argument("--data", default=str(Path(__file__).parent))
    p.add_argument("--out", help="write JSONL here instead of printing")
    p.add_argument("--steps", action="store_true",
                   help="also show each graph step's output")
    args = p.parse_args()

    random.seed(args.seed)
    d = Path(args.data)
    templates = all_templates(d)
    if args.id:
        templates = [t for t in templates if t["id"] == args.id]
        if not templates:
            raise SystemExit(f"no template with id {args.id!r}")

    rows, failed = [], []
    for t in templates:
        try:
            got = instances(t, args.num)
        except Exception as e:
            failed.append((t["id"], f"{type(e).__name__}: {e}"))
            continue
        if len(got) < args.num:
            failed.append((t["id"], f"only {len(got)}/{args.num} distinct"))
        for q, answer, node_outputs, vals in got:
            rows.append({"template_id": t["id"], "question": q,
                         "answer": answer, "node_outputs": node_outputs,
                         "question_vars": {k: str(v) for k, v in vals.items()}})

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False, default=str) + "\n")
        print(f"{len(rows)} samples from {len(templates)} templates -> {args.out}")
    else:
        current = None
        for r in rows:
            if r["template_id"] != current:
                current = r["template_id"]
                print(f"\n=== {current}")
            print(f"  Q: {r['question']}")
            print(f"  A: {r['answer']}")
            if args.steps and r["node_outputs"]:
                for nid, v in r["node_outputs"].items():
                    print(f"       {nid} = {v}")

    if failed:
        print(f"\n{len(failed)} template(s) with problems:")
        for tid, why in failed[:20]:
            print(f"   {tid:<46} {why}")


if __name__ == "__main__":
    main()
