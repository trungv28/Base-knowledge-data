from fractions import Fraction


import math


from sympy import sqrt, Rational


import kernel, atoms


def ordinal(n):
    n = int(n)
    if 10 <= n % 100 <= 20:
        return f"{n}th"
    return f"{n}{ {1:'st', 2:'nd', 3:'rd'}.get(n % 10, 'th') }"


def poly(pairs, v="x"):
    terms = {}
    for p, k in pairs:
        terms[p] = terms.get(p, 0) + k
    out = ""
    for p in sorted((p for p, k in terms.items() if k), reverse=True):
        k = terms[p]
        body = "" if p == 0 else v if p == 1 else f"{v}^{p}"
        mag = "" if abs(k) == 1 and body else str(abs(k))
        piece = f"{mag}{body}"
        if not out:
            out = f"−{piece}" if k < 0 else piece
        else:
            out += f" {'−' if k < 0 else '+'} {piece}"
    return out or "0"


def bracket(pairs, v="x"):
    return "(" + poly(pairs, v) + ")"


def quad(a, b, c, v="x"):
    return poly([(2, a), (1, b), (0, c)], v)


def cubic(a, b, c, d, v="x"):
    return poly([(3, a), (2, b), (1, c), (0, d)], v)


def lineq(m, x1, y1):
    m = Fraction(m)
    b = Fraction(y1) - m * Fraction(x1)
    if m == 0:
        return f"y = {pf(b.numerator, b.denominator)}"
    ms = "x" if m == 1 else "-x" if m == -1 else f"{pf(m.numerator, m.denominator)}x"
    if b == 0:
        return f"y = {ms}"
    sign = "+" if b > 0 else "−"
    return f"y = {ms} {sign} {pf(abs(b.numerator), b.denominator)}"


def _collect(a, n, b, m, c, d):
    terms = {}
    for power, coeff in ((n, a), (m, b), (1, c), (0, d)):
        terms[power] = terms.get(power, 0) + coeff
    return {p: k for p, k in terms.items() if k != 0}


def poly_degree(a, n, b, m, c, d):
    terms = _collect(a, n, b, m, c, d)
    return max(terms) if terms else 0


def poly_leading_coefficient(a, n, b, m, c, d):
    terms = _collect(a, n, b, m, c, d)
    return terms[max(terms)] if terms else 0


def poly_coefficient(a, n, b, m, c, d, k):
    return _collect(a, n, b, m, c, d).get(k, 0)


def pf(num, den):
    f = Fraction(num, den)
    if f.denominator == 1:
        return str(f.numerator)
    return f"{f.numerator}/{f.denominator}"


def _pi_coeff_str(f):
    f = Fraction(f)
    if f == 0:
        return "0"
    if f == 1:
        return "π"
    if f == -1:
        return "-π"
    if f.denominator == 1:
        return f"{f.numerator}π"
    if f.numerator == 1:
        return f"π/{f.denominator}"
    if f.numerator == -1:
        return f"-π/{f.denominator}"
    return f"{f.numerator}π/{f.denominator}"


def quad_hyperbola_intersect(c_val, axis_val, d_val):
    h = axis_val
    d = d_val
    y_int = c_val
    k = (y_int - d) * (-h)
    return str(int(k)) if k == int(k) else str(k)


def transform_horizontal_dilation_eval(k_val, h_val, eval_x):
    transformed_x = k_val * (eval_x - h_val)
    y_at_eval = transformed_x**2
    return str(int(y_at_eval)) if y_at_eval == int(y_at_eval) else str(y_at_eval)


import sympy as _sp


_SIN_BASE_BY_VALUE = {
    "0": (Fraction(0), Fraction(1)),
    "1/2": (Fraction(1, 6), Fraction(5, 6)),
    "1": (Fraction(1, 2), Fraction(1, 2)),
    "\u221a3/2": (Fraction(1, 3), Fraction(2, 3)),
    "-1/2": (Fraction(7, 6), Fraction(11, 6)),
    "-\u221a3/2": (Fraction(4, 3), Fraction(5, 3)),
}


def sin_base_angle(a_value, which):
    return _SIN_BASE_BY_VALUE[str(a_value)][which]


INF, NEG_INF = "∞", "−∞"


def quad_axis_evaluate(a_val, b_val, c_val):
    axis = Fraction(-b_val, 2 * a_val)
    return str(a_val * axis**2 + b_val * axis + c_val)


def cubic_intercept_translate(b_val, c_val, d_val, e_val, v_val):
    y = e_val**3 + b_val * e_val**2 + c_val * e_val + d_val
    return str(y + v_val)


def transform_vertical_sequence_eval(c_val, v_val, e_val):
    return str(c_val * e_val**2 + v_val)


def transform_hdilate_translate_eval(k_val, v_val, e_val):
    return str((k_val * e_val) ** 2 + v_val)


def hyperbola_translate_evaluate(a_val, b_val, d_val, h_val, e_val):
    return str(Fraction(a_val, e_val - (b_val + h_val)) + d_val)


def invprop_shifted_evaluate(y1_val, x1_val, v_val, x2_val):
    return str(Fraction(y1_val * x1_val, x2_val) + v_val)


def directprop_evaluate(z1_val, x1_val, x2_val):
    return str(Fraction(z1_val, x1_val) * x2_val)


def quad_vertex_below_intercept(a_val, b_val, c_val):
    axis = Fraction(-b_val, 2 * a_val)
    return str(c_val - (a_val * axis**2 + b_val * axis + c_val))


def quad_two_linear_translate(a_val, b_val, v_val):
    return poly([(2, 1), (1, -(a_val + b_val)), (0, a_val * b_val + v_val)])


def quad_repeated_dilate(a_val, c_val):
    return poly([(2, c_val), (1, -2 * a_val * c_val), (0, a_val * a_val * c_val)])


def transform_chain_evaluate(c_val, v_val, h_val, e_val):
    return str(c_val * (e_val - h_val) ** 2 + v_val)


def transform_full_chain_evaluate(k_val, c_val, h_val, v_val, e_val):
    return str(c_val * (k_val * (e_val - h_val)) ** 2 + v_val)


def transform_chain_inverse(k_val, c_val, h_val, v_val, y_val):
    import sympy as _s
    inner = _s.sqrt(Fraction(y_val - v_val, c_val))
    return str(Fraction(int(inner), k_val) + h_val)


def quad_translate_intercept_gap(a_val, b_val, c_val, h_val, v_val):
    axis = Fraction(-b_val, 2 * a_val)
    vertex_y = a_val * axis**2 + b_val * axis + c_val
    x, y = axis + h_val, vertex_y + v_val
    return f"({pf(x.numerator, x.denominator)}, {pf(y.numerator, y.denominator)})"


def quad_axis_translate(a_val, b_val, h_val):
    return str(Fraction(-b_val, 2 * a_val) + h_val)


def quad_vertex_translate(a_val, b_val, c_val, v_val):
    axis = Fraction(-b_val, 2 * a_val)
    return str(a_val * axis**2 + b_val * axis + c_val + v_val)


def factor_theorem_shift(a_val, b_val, c_val, d_val, v_val):
    p_at_a = a_val**3 + b_val * a_val**2 + c_val * a_val + d_val
    return "yes" if p_at_a + v_val == 0 else "no"


def cubic_quotient_vertex_translate(a_val, b_val, c_val, d_val, v_val):
    q1 = b_val + a_val
    q0 = c_val + a_val * q1
    axis = Fraction(-q1, 2)
    y = axis * axis + q1 * axis + q0 + v_val
    return pf(y.numerator, y.denominator)


CALL = kernel.REGISTRY


def coeff_poly(coeffs):
    top = len(coeffs) - 1
    return poly([(top - i, k) for i, k in enumerate(coeffs)])


def direct_prop_constant_ratio(y1, x1):
    return kernel.render(CALL["func.direct_proportion.constant_ratio"](y=y1, x=x1))


def inv_proportion_equation(x1, y1):
    return kernel.render(CALL["func.inv_proportion.definition"](x=x1, y=y1))


def func_linear_solve_one_step(a, b):
    return kernel.render(CALL["func.linear_solve.one_step"](a=a, b=b))


def quad_general_axis(a, b, c):
    return kernel.render(CALL["func.quad_general.axis"](coeffs=(a, b, c)))


def quad_general_y_intercept(a, b, c):
    return kernel.render(CALL["func.quad_general.y_intercept"](coeffs=(a, b, c)))


def func_evaluate(a, b, c, k):
    return kernel.render(CALL["func.notation.evaluate"](coeffs=(a, b, c), x=k))


def transform_v_translate_y(q, a):
    return kernel.render(CALL["func.transform.vertical_translation"](y=q, a=a))


def transform_h_translate_x(p, b):
    return kernel.render(CALL["func.transform.inverse_horizontal_translation"](x=p, h=b))


def transform_v_dilate_y(q, c):
    return kernel.render(CALL["func.transform.vertical_dilation"](y=q, c=c))


def transform_h_dilate_x(p, k):
    return kernel.render(CALL["func.transform.horizontal_dilation"](x=p, k=k))


def hyperbola_vertical_asymptote(a, b):
    return f"x = {kernel.render(CALL['func.hyperbola.vertical_asymptote'](b=b))}"


def hyperbola_horizontal_asymptote(a, b, d):
    return f"y = {kernel.render(CALL['func.hyperbola.horizontal_asymptote'](d=d))}"


def sqrt_principal(t_val):
    return kernel.render(CALL["func.sqrt.principal"](t=t_val))


def poly_quadratic_two_linear(a, b):
    return coeff_poly(CALL["func.poly.quadratic_two_linear"](a=a, b=b))


def poly_quadratic_repeated(a):
    return coeff_poly(CALL["func.poly.quadratic_repeated"](a=a))


def poly_factor_theorem(a, b, c, d):
    p_at_a = CALL["func.notation.evaluate"](coeffs=(1, b, c, d), x=a)
    return CALL["func.poly.factor_theorem"](p_at_a=p_at_a).capitalize()


def poly_cubic_factor_quotient(a, b, c, d):
    try:
        quotient = CALL["func.poly.cubic_factor_quotient"](a=a, b=b, c=c, d=d)
    except ValueError:
        return "not a factor"
    return coeff_poly(quotient)


def transform_h_translate_forward(p, h):
    return kernel.render(CALL["func.transform.horizontal_translation"](x=p, h=h))


def transform_inv_h_dilate(p, k):
    return kernel.render(CALL["func.transform.inverse_horizontal_dilation"](x=p, k=k))


def transform_inv_v_translate(q, a):
    return kernel.render(CALL["func.transform.inverse_vertical_translation"](y=q, a=a))


def transform_inv_v_dilate(q, c):
    return kernel.render(CALL["func.transform.inverse_vertical_dilation"](y=q, c=c))


def direct_prop_evaluate_atom(k, x):
    return kernel.render(CALL["func.direct_proportion.evaluate"](k=k, x=x))


def hyperbola_evaluate_atom(a, b, d, x):
    return kernel.render(CALL["func.hyperbola.evaluate"](a=a, b=b, d=d, x=x))


def poly_cubic_three_linear_atom(a, b, c):
    return coeff_poly(CALL["func.poly.cubic_three_linear"](a=a, b=b, c=c))


def quad_coefficient_from_axis_atom(a, axis):
    return kernel.render(CALL["func.quad_general.axis_coefficient"](a=a, axis=axis))


def poly_v_translate_atom(a, b, c, v):
    return coeff_poly(CALL["func.transform.poly_vertical_translation"](coeffs=(a, b, c), a=v))


def poly_v_dilate_atom(a, b, c, k):
    return coeff_poly(CALL["func.transform.poly_vertical_dilation"](coeffs=(a, b, c), c=k))


def inv_prop_evaluate_atom(k, x):
    return kernel.render(CALL["func.inv_proportion.evaluate"](k=k, x=x))


def poly_factor_theorem_atom(a, pa):
    return CALL["func.poly.factor_theorem"](p_at_a=pa).capitalize()
