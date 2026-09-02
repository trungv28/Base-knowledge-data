import json, random
import sympy as sp

import common_solvers, generate, program

x = sp.Symbol("x")
DRAWS = 12
CHECKS = {}


def check(cid):
    def deco(f):
        CHECKS[cid] = f
        return f
    return deco


def norm(v):
    return str(v).replace(" ", "").replace("−", "-").replace("*", "")


@check("quad_axis_evaluate")
def _(v):
    q = v["a_val"]*x**2 + v["b_val"]*x + v["c_val"]
    return q.subs(x, sp.solve(sp.diff(q, x), x)[0])


@check("quad_vertex_translate")
def _(v):
    q = v["a_val"]*x**2 + v["b_val"]*x + v["c_val"]
    return q.subs(x, sp.solve(sp.diff(q, x), x)[0]) + v["v_val"]


@check("quad_axis_translate")
def _(v):
    q = v["a_val"]*x**2 + v["b_val"]*x + v["c_val"]
    return sp.solve(sp.diff(q, x), x)[0] + v["h_val"]


@check("quad_vertex_below_intercept")
def _(v):
    q = v["a_val"]*x**2 + v["b_val"]*x + v["c_val"]
    vy = q.subs(x, sp.solve(sp.diff(q, x), x)[0])
    return q.subs(x, 0) - vy


@check("quad_translate_intercept_gap")
def _(v):
    q = v["a_val"]*x**2 + v["b_val"]*x + v["c_val"]
    ax = sp.solve(sp.diff(q, x), x)[0]
    return f"({ax + v['h_val']}, {q.subs(x, ax) + v['v_val']})"


@check("transform_vertical_sequence_eval")
def _(v):
    return (v["c_val"] * x**2 + v["v_val"]).subs(x, v["e_val"])


@check("transform_chain_evaluate")
def _(v):
    g = v["c_val"] * (x - v["h_val"])**2 + v["v_val"]
    return g.subs(x, v["e_val"])


@check("transform_full_chain_evaluate")
def _(v):
    g = v["c_val"] * (v["k_val"] * (x - v["h_val"]))**2 + v["v_val"]
    return g.subs(x, v["e_val"])


@check("transform_deep_chain_evaluate")
def _(v):
    g = v["c2_val"] * (v["c_val"] * (v["k_val"] * (x - v["h_val"]))**2 + v["v_val"])
    return g.subs(x, v["e_val"])


@check("transform_hdilate_translate_eval")
def _(v):
    return ((v["k_val"] * x)**2 + v["v_val"]).subs(x, v["e_val"])


@check("transform_horizontal_dilation_eval")
def _(v):
    return ((v["k_val"] * (x - v["h_val"]))**2).subs(x, v["eval_x"])


@check("transform_chain_inverse")
def _(v):
    g = v["c_val"] * (v["k_val"] * (x - v["h_val"]))**2 + v["v_val"]
    roots = [r for r in sp.solve(sp.Eq(g, v["y_val"]), x) if r.is_real]
    return max(roots)


@check("transform_deep_chain_inverse")
def _(v):
    g = v["c2_val"] * (v["c_val"] * (v["k_val"] * (x - v["h_val"]))**2 + v["v_val"])
    roots = [r for r in sp.solve(sp.Eq(g, v["y_val"]), x) if r.is_real]
    return max(roots)


@check("directprop_evaluate")
def _(v):
    return sp.Rational(v["z1_val"], v["x1_val"]) * v["x2_val"]


@check("invprop_shifted_evaluate")
def _(v):
    return sp.Rational(v["y1_val"] * v["x1_val"], v["x2_val"]) + v["v_val"]


@check("cubic_intercept_translate")
def _(v):
    p = sp.expand((x - v["a_val"]) * (x - v["b_val"]) * (x - v["c_val"])) + v["v_val"]
    return p.subs(x, 0)


@check("cubic_quotient_root_sum")
def _(v):
    p = x**3 + v["b_val"]*x**2 + v["c_val"]*x + v["d_val"]
    q, r = sp.div(p, x - v["a_val"], x)
    assert r == 0
    return sum(root * m for root, m in sp.roots(sp.Poly(q, x)).items())


@check("cubic_quotient_chain")
def _(v):
    return CHECKS["cubic_quotient_root_sum"](v)


@check("cubic_quotient_vertex_translate")
def _(v):
    p = x**3 + v["b_val"]*x**2 + v["c_val"]*x + v["d_val"]
    q, r = sp.div(p, x - v["a_val"], x)
    assert r == 0
    return q.subs(x, sp.solve(sp.diff(q, x), x)[0]) + v["v_val"]


@check("factor_theorem_shift")
def _(v):
    p = x**3 + v["b_val"]*x**2 + v["c_val"]*x + v["d_val"] + v["v_val"]
    return "yes" if p.subs(x, v["a_val"]) == 0 else "no"


@check("quad_two_linear_translate")
def _(v):
    return sp.expand((x - v["a_val"]) * (x - v["b_val"])) + v["v_val"]


@check("quad_repeated_dilate")
def _(v):
    return sp.expand(v["c_val"] * (x - v["a_val"])**2)


@check("hyperbola_translate_evaluate")
def _(v):
    g = sp.Rational(v["a_val"], 1) / (x - (v["b_val"] + v["h_val"])) + v["d_val"]
    return g.subs(x, v["e_val"])


@check("asymptote_vertex_y")
def _(v):
    p, q, a = v["b_val"], v["d_val"], v["a_quad"]
    quad = a*x**2 + (-2*a*p)*x + q
    assert sp.solve(sp.diff(quad, x), x)[0] == p
    return quad.subs(x, p)


@check("quad_hyperbola_intersect")
def _(v):
    k = sp.Symbol("k")
    hyp = k / (x - v["axis_val"]) + v["d_val"]
    return sp.solve(sp.Eq(hyp.subs(x, 0), v["c_val"]), k)[0]


def as_poly(text):
    t = text.replace("^", "**").replace("−", "-").replace(" ", "")
    import re
    t = re.sub(r"(\d)(x)", r"\1*\2", t)
    return sp.sympify(t, locals={"x": x})


def main():
    random.seed(3)
    comps = {json.loads(l)["id"]: json.loads(l) for l in open("composite.jsonl")}
    specs = {json.loads(l)["id"]: json.loads(l) for l in open("graphs.jsonl")}
    bad, ok, missing = [], 0, []
    for cid, spec in specs.items():
        fn = CHECKS.get(cid)
        if fn is None:
            missing.append(cid)
            continue
        for _ in range(DRAWS):
            v = generate.sample(comps[cid])
            got, _n = program.run(spec["nodes"], v, program.returned(spec))
            try:
                want = fn(v)
            except Exception as e:
                bad.append((cid, f"AUDIT ERROR {type(e).__name__}: {e}"))
                break
            shown = common_solvers.render(got)
            hit = norm(shown) == norm(want)
            if not hit and isinstance(got, tuple):
                hit = sp.simplify(as_poly(
                    __import__("solver").coeff_poly(got)) - want) == 0
            if not hit:
                try:
                    hit = sp.simplify(sp.sympify(norm(shown)) - want) == 0
                except Exception:
                    pass
            if not hit:
                bad.append((cid, f"program {shown!r} vs sympy {want!r}  vars={dict(list(v.items())[:5])}"))
                break
        else:
            ok += 1
    print(f"independently re-derived {len(specs) - len(missing)}/{len(specs)} composites; "
          f"agree: {ok}   disagree: {len(bad)}")
    for cid, why in bad:
        print(f"   MISMATCH {cid}: {why}")
    if missing:
        print(f"   no check written: {missing}")
    return 1 if bad or missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
