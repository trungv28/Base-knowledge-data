import argparse, json, random
import sympy as sp
from fractions import Fraction

import common_solvers, generate, program, solver

x = sp.Symbol("x")
ATOM_CHECKS = {}
COMPOSITE_CHECKS = {}
DRAWS = 12


def norm(v):
    return str(v).replace(" ", "").replace("\u2212", "-").replace("*", "")


def check(atom_id):
    def deco(f):
        ATOM_CHECKS[atom_id] = f
        return f
    return deco


def composite(cid):
    def deco(f):
        COMPOSITE_CHECKS[cid] = f
        return f
    return deco


@check("func.direct_proportion.constant_ratio")
def _(f):
    return all(sp.simplify(f(y=y, x=xx) - sp.Rational(y, xx)) == 0
               for y in (-7, 3, 12) for xx in (2, 5, -4))


@check("func.direct_proportion.evaluate")
def _(f):
    return all(sp.simplify(f(k=k, x=xx) - k * xx) == 0
               for k in (Fraction(3, 2), 4) for xx in (2, -5))


@check("func.inv_proportion.definition")
def _(f):
    return all(f(x=xx, y=y) == xx * y for xx in (2, 7) for y in (3, -5))


@check("func.linear_solve.one_step")
def _(f):
    return all(sp.solve(sp.Eq(a * x, b), x)[0] == f(a=a, b=b)
               for a in (2, -3, 7) for b in (6, -5))


@check("func.quad_general.axis")
def _(f):
    for a, b, c in ((1, -6, 5), (2, 3, -1), (-3, 12, 7)):
        want = sp.solve(sp.diff(a * x**2 + b * x + c, x), x)[0]
        if sp.simplify(want - f(coeffs=(a, b, c))) != 0:
            return False
    return True


@check("func.quad_general.y_intercept")
def _(f):
    return all((a * x**2 + b * x + c).subs(x, 0) == f(coeffs=(a, b, c))
               for a, b, c in ((1, -6, 5), (2, 3, -1)))


@check("func.notation.evaluate")
def _(f):
    for co in ((1, -8, 15), (2, 0, -3, 1)):
        p = sum(k * x**(len(co) - 1 - i) for i, k in enumerate(co))
        if any(p.subs(x, v) != f(coeffs=co, x=v) for v in (-2, 0, 3)):
            return False
    return True


@check("func.poly.quadratic_two_linear")
def _(f):
    for a, b in ((3, 5), (-2, 7)):
        want = sp.Poly(sp.expand((x - a) * (x - b)), x).all_coeffs()
        if tuple(want) != f(a=a, b=b):
            return False
    return True


@check("func.poly.quadratic_repeated")
def _(f):
    return all(tuple(sp.Poly(sp.expand((x - a)**2), x).all_coeffs()) == f(a=a)
               for a in (3, -4))


@check("func.poly.factor_theorem")
def _(f):
    return f(p_at_a=0) == "yes" and f(p_at_a=5) == "no" and f(p_at_a=-2) == "no"


@check("func.poly.cubic_factor_quotient")
def _(f):
    for a, r1, r2 in ((1, 2, 3), (-2, 4, -5)):
        p = sp.expand((x - a) * (x - r1) * (x - r2))
        b, c, d = sp.Poly(p, x).all_coeffs()[1:]
        want, rem = sp.div(p, x - a, x)
        assert rem == 0
        if tuple(sp.Poly(want, x).all_coeffs()) != f(a=a, b=b, c=c, d=d):
            return False
    return True


@check("func.hyperbola.vertical_asymptote")
def _(f):
    for a, b in ((3, 4), (-2, -5)):
        poles = sp.singularities(sp.Rational(a) / (x - b), x)
        if list(poles)[0] != f(b=b):
            return False
    return True


@check("func.hyperbola.horizontal_asymptote")
def _(f):
    for a, b, d in ((3, 4, 2), (-2, -5, -7)):
        if sp.limit(sp.Rational(a) / (x - b) + d, x, sp.oo) != f(d=d):
            return False
    return True


@check("func.sqrt.principal")
def _(f):
    return all(f(t=t) == sp.sqrt(t) and f(t=t) >= 0 for t in (0, 4, 25, 7))


def _pt(g, v):
    return sp.simplify(g.subs(x, v))


@check("func.transform.vertical_translation")
def _(f):
    return all(f(y=y, a=a) == _pt(x**2 + a, 0) + y - 0 for y in (3,) for a in (5,)) or \
           all(f(y=y, a=a) == y + a for y in (3, -2) for a in (5, -4))


@check("func.transform.inverse_vertical_translation")
def _(f):
    return all(f(y=common_solvers.REGISTRY["func.transform.vertical_translation"](y=y, a=a), a=a) == y
               for y in (3, -2) for a in (5, -4))


@check("func.transform.vertical_dilation")
def _(f):
    return all(f(y=y, c=c) == c * y for y in (3, -2) for c in (5, -4))


@check("func.transform.inverse_vertical_dilation")
def _(f):
    return all(f(y=common_solvers.REGISTRY["func.transform.vertical_dilation"](y=y, c=c), c=c) == y
               for y in (3, -2) for c in (5, -4))


@check("func.transform.horizontal_translation")
def _(f):
    for h in (3, -4):
        g = (x - h)**2
        for v in (0, 2, -5):
            if sp.simplify(g.subs(x, f(x=v, h=h)) - (v**2)) != 0:
                return False
    return True


@check("func.transform.inverse_horizontal_translation")
def _(f):
    return all(f(x=common_solvers.REGISTRY["func.transform.horizontal_translation"](x=v, h=h), h=h) == v
               for v in (0, 2, -5) for h in (3, -4))


@check("func.transform.horizontal_dilation")
def _(f):
    for k in (2, -3):
        g = (k * x)**2
        for v in (0, 4, -6):
            if sp.simplify(g.subs(x, f(x=v, k=k)) - (v**2)) != 0:
                return False
    return True


@check("func.transform.inverse_horizontal_dilation")
def _(f):
    return all(f(x=common_solvers.REGISTRY["func.transform.horizontal_dilation"](x=v, k=k), k=k) == v
               for v in (0, 4, -6) for k in (2, -3))


@check("func.poly.cubic_three_linear")
def _(f):
    for a, b, c in ((4, 6, 1), (-2, 3, 5)):
        want = sp.Poly(sp.expand((x - a)*(x - b)*(x - c)), x).all_coeffs()
        if tuple(want) != f(a=a, b=b, c=c):
            return False
    return True


@check("func.transform.poly_vertical_translation")
def _(f):
    for co in ((1, -12, 32), (2, 0, -3, 1)):
        p = sum(k * x**(len(co)-1-i) for i, k in enumerate(co))
        for a in (9, -4):
            got = f(coeffs=co, a=a)
            g = sum(k * x**(len(got)-1-i) for i, k in enumerate(got))
            if sp.simplify(g - (p + a)) != 0:
                return False
    return True


@check("func.transform.poly_vertical_dilation")
def _(f):
    for co in ((1, 12, 36), (3, -1, 0, 2)):
        p = sum(k * x**(len(co)-1-i) for i, k in enumerate(co))
        for c in (3, -2):
            got = f(coeffs=co, c=c)
            g = sum(k * x**(len(got)-1-i) for i, k in enumerate(got))
            if sp.simplify(g - c*p) != 0:
                return False
    return True


@check("func.hyperbola.evaluate")
def _(f):
    for a, b, d in ((3, 5, -3), (-2, 1, 4)):
        g = sp.Rational(a, 1)/(x - b) + d
        for v in (-4, 0, 7):
            if v == b:
                continue
            if sp.simplify(g.subs(x, v) - f(a=a, b=b, d=d, x=v)) != 0:
                return False
    return True


@check("func.quad_general.axis_coefficient")
def _(f):
    for a, p in ((2, 1), (-3, sp.Rational(5, 2))):
        b = f(a=a, axis=p)
        if sp.solve(sp.diff(a*x**2 + b*x, x), x)[0] != p:
            return False
    return True


@check("func.inv_proportion.evaluate")
def _(f):
    return all(sp.simplify(f(k=k, x=v) - sp.Rational(k, v)) == 0
               for k in (60, -35) for v in (4, -7))


@composite("quad_axis_evaluate")
def _(v):
    q = v["a_val"]*x**2 + v["b_val"]*x + v["c_val"]
    return q.subs(x, sp.solve(sp.diff(q, x), x)[0])


@composite("quad_vertex_translate")
def _(v):
    q = v["a_val"]*x**2 + v["b_val"]*x + v["c_val"]
    return q.subs(x, sp.solve(sp.diff(q, x), x)[0]) + v["v_val"]


@composite("quad_axis_translate")
def _(v):
    q = v["a_val"]*x**2 + v["b_val"]*x + v["c_val"]
    return sp.solve(sp.diff(q, x), x)[0] + v["h_val"]


@composite("quad_vertex_below_intercept")
def _(v):
    q = v["a_val"]*x**2 + v["b_val"]*x + v["c_val"]
    vy = q.subs(x, sp.solve(sp.diff(q, x), x)[0])
    return q.subs(x, 0) - vy


@composite("quad_translate_intercept_gap")
def _(v):
    q = v["a_val"]*x**2 + v["b_val"]*x + v["c_val"]
    ax = sp.solve(sp.diff(q, x), x)[0]
    return f"({ax + v['h_val']}, {q.subs(x, ax) + v['v_val']})"


@composite("transform_vertical_sequence_eval")
def _(v):
    return (v["c_val"] * x**2 + v["v_val"]).subs(x, v["e_val"])


@composite("transform_chain_evaluate")
def _(v):
    g = v["c_val"] * (x - v["h_val"])**2 + v["v_val"]
    return g.subs(x, v["e_val"])


@composite("transform_full_chain_evaluate")
def _(v):
    g = v["c_val"] * (v["k_val"] * (x - v["h_val"]))**2 + v["v_val"]
    return g.subs(x, v["e_val"])


@composite("transform_hdilate_translate_eval")
def _(v):
    return ((v["k_val"] * x)**2 + v["v_val"]).subs(x, v["e_val"])


@composite("transform_horizontal_dilation_eval")
def _(v):
    return ((v["k_val"] * (x - v["h_val"]))**2).subs(x, v["eval_x"])


@composite("transform_chain_inverse")
def _(v):
    g = v["c_val"] * (v["k_val"] * (x - v["h_val"]))**2 + v["v_val"]
    roots = [r for r in sp.solve(sp.Eq(g, v["y_val"]), x) if r.is_real]
    return max(roots)


@composite("directprop_evaluate")
def _(v):
    return sp.Rational(v["z1_val"], v["x1_val"]) * v["x2_val"]


@composite("invprop_shifted_evaluate")
def _(v):
    return sp.Rational(v["y1_val"] * v["x1_val"], v["x2_val"]) + v["v_val"]


@composite("cubic_intercept_translate")
def _(v):
    p = x**3 + v["b_val"] * x**2 + v["c_val"] * x + v["d_val"]
    return p.subs(x, v["e_val"]) + v["v_val"]


@composite("cubic_quotient_vertex_translate")
def _(v):
    p = x**3 + v["b_val"]*x**2 + v["c_val"]*x + v["d_val"]
    q, r = sp.div(p, x - v["a_val"], x)
    assert r == 0
    return q.subs(x, sp.solve(sp.diff(q, x), x)[0]) + v["v_val"]


@composite("factor_theorem_shift")
def _(v):
    p = x**3 + v["b_val"]*x**2 + v["c_val"]*x + v["d_val"] + v["v_val"]
    return "yes" if p.subs(x, v["a_val"]) == 0 else "no"


@composite("quad_two_linear_translate")
def _(v):
    return sp.expand((x - v["a_val"]) * (x - v["b_val"])) + v["v_val"]


@composite("quad_repeated_dilate")
def _(v):
    return sp.expand(v["c_val"] * (x - v["a_val"])**2)


@composite("hyperbola_translate_evaluate")
def _(v):
    g = sp.Rational(v["a_val"], 1) / (x - (v["b_val"] + v["h_val"])) + v["d_val"]
    return g.subs(x, v["e_val"])


@composite("quad_hyperbola_intersect")
def _(v):
    k = sp.Symbol("k")
    hyp = k / (x - v["axis_val"]) + v["d_val"]
    return sp.solve(sp.Eq(hyp.subs(x, 0), v["c_val"]), k)[0]


def as_poly(text):
    t = text.replace("^", "**").replace("−", "-").replace(" ", "")
    import re
    t = re.sub(r"(\d)(x)", r"\1*\2", t)
    return sp.sympify(t, locals={"x": x})


def audit_atoms():
    reg = common_solvers.REGISTRY
    knowledge = [a for a, k in common_solvers.KIND.items() if k == "knowledge"]
    bad, missing = [], []
    for a in knowledge:
        fn = ATOM_CHECKS.get(a)
        if fn is None:
            missing.append(a)
            continue
        try:
            if not fn(reg[a]):
                bad.append((a, "disagrees with sympy"))
        except Exception as e:
            bad.append((a, f"{type(e).__name__}: {e}"))
    print(f"atoms: independently audited {len(knowledge) - len(missing)}/{len(knowledge)}; "
          f"agree: {len(knowledge) - len(missing) - len(bad)}   disagree: {len(bad)}")
    for a, why in bad:
        print(f"   MISMATCH {a}: {why}")
    if missing:
        print(f"   no check written: {missing}")
    return bad or missing


def audit_composites():
    comps = {json.loads(l)["id"]: json.loads(l) for l in open("composite.jsonl")}
    specs = {json.loads(l)["id"]: json.loads(l) for l in open("graphs.jsonl")}
    bad, ok, missing = [], 0, []
    for cid, spec in specs.items():
        fn = COMPOSITE_CHECKS.get(cid)
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
                hit = sp.simplify(as_poly(solver.coeff_poly(got)) - want) == 0
            if not hit:
                try:
                    hit = sp.simplify(sp.sympify(norm(shown)) - want) == 0
                except Exception:
                    pass
            if not hit:
                bad.append((cid, f"program {shown!r} vs sympy {want!r}  "
                                 f"vars={dict(list(v.items())[:5])}"))
                break
        else:
            ok += 1
    print(f"composites: independently re-derived {len(specs) - len(missing)}/{len(specs)}; "
          f"agree: {ok}   disagree: {len(bad)}")
    for cid, why in bad:
        print(f"   MISMATCH {cid}: {why}")
    if missing:
        print(f"   no check written: {missing}")
    return bad or missing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=3)
    a = ap.parse_args()
    random.seed(a.seed)
    bad_atoms = audit_atoms()
    bad_comps = audit_composites()
    return 1 if (bad_atoms or bad_comps) else 0


if __name__ == "__main__":
    raise SystemExit(main())
