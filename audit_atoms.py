import json
import sympy as sp
from fractions import Fraction

import common_solvers

x = sp.Symbol("x")
CHECKS = {}


def check(atom_id):
    def deco(f):
        CHECKS[atom_id] = f
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


@check("func.poly.roots_sum")
def _(f):
    for a, b, c in ((1, -5, 6), (2, 7, 3)):
        want = sum(sp.solve(sp.Eq(a * x**2 + b * x + c, 0), x))
        if sp.simplify(want - f(coeffs=(a, b, c))) != 0:
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


@check("func.quad_general.coefficient_from_axis")
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


def main():
    reg = common_solvers.REGISTRY
    knowledge = [a for a, k in common_solvers.KIND.items() if k == "knowledge"]
    bad, missing = [], []
    for a in knowledge:
        fn = CHECKS.get(a)
        if fn is None:
            missing.append(a)
            continue
        try:
            if not fn(reg[a]):
                bad.append((a, "disagrees with sympy"))
        except Exception as e:
            bad.append((a, f"{type(e).__name__}: {e}"))
    print(f"independently audited {len(knowledge) - len(missing)}/{len(knowledge)} "
          f"knowledge atoms; agree: {len(knowledge) - len(missing) - len(bad)}   "
          f"disagree: {len(bad)}")
    for a, why in bad:
        print(f"   MISMATCH {a}: {why}")
    if missing:
        print(f"   no check written: {missing}")
    return 1 if bad or missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
