from fractions import Fraction
import math
from sympy import sqrt, Rational

def ordinal(n):
    n = int(n)
    if 10 <= n % 100 <= 20:
        return f"{n}th"
    return f"{n}{ {1:'st', 2:'nd', 3:'rd'}.get(n % 10, 'th') }"


def midpoint_compute_x(x1, y1, x2, y2):
    return pf(x1 + x2, 2)

def midpoint_compute_y(x1, y1, x2, y2):
    return pf(y1 + y2, 2)

def direct_prop_equation(k, x):
    return str(k * x)

def direct_prop_constant_ratio(y1, x1, x2):
    return pf(y1 * x2, x1)

def linearly_related_equation(m, b, x):
    return str(m * x + b)

def linearly_related_rate(m, dx):
    return str(m * dx)

def direct_prop_vs_linear_identify(m, b):
    if b == 0:
        return "yes"
    else:
        return "no"

def linear_form_find_slope(x1, y1, x2, y2):
    if x2 == x1:
        return "undefined"
    return pf(y2 - y1, x2 - x1)

def linear_form_slope_sign(m, c):
    if m > 0:
        return "rises"
    elif m < 0:
        return "falls"
    else:
        return "horizontal"

def linear_form_x_intercept(m, c):
    if m == 0:
        return "none"
    return pf(-c, m)

def linear_equation_slope_yint(m, c):
    return f"y = {m}x + {c}"

def linear_equation_slope_point(m, x1, y1):
    b = y1 - m * x1
    return f"y = {m}x + {b}"

def linear_equation_two_points(x1, y1, x2, y2):
    if x2 == x1:
        return f"x = {x1}"
    m = Fraction(y2 - y1, x2 - x1)
    b = y1 - m * x1
    ms = pf(m.numerator, m.denominator)
    bs = pf(abs(b.numerator), b.denominator)
    if m == 0:
        return f"y = {pf(b.numerator, b.denominator)}"
    if b == 0:
        return f"y = {ms}x"
    elif b > 0:
        return f"y = {ms}x + {bs}"
    else:
        return f"y = {ms}x - {bs}"

def linear_perpendicular_find_slope(m, c):
    return pf(-1, m)

def linear_perpendicular_check(m1, c1, m2, c2):
    if m1 * m2 == -1:
        return "yes"
    else:
        return "no"

def func_linear_solve_one_step(a, b):
    return pf(b, a)

def func_linear_solve_two_step(a, b, c):
    return pf(c - b, a)

def func_linear_solve_general(a, b, c, d):
    return pf(d - b, a - c)

def quad_relation_second_diff_value(a, b, c):
    return str(2 * a)

def quad_factor_x_intercept_1(a, b, c):
    return str(min(b, c))

def quad_factor_axis(a, b, c):
    return pf(b + c, 2)

def quad_factor_turning_point_y(a, b, c):
    return pf(-a * (b - c) ** 2, 4)

def quad_concavity(a, b, c):
    return "minimum" if a > 0 else "maximum"

def quad_formula_solve_smaller(a, b, c):
    import sympy as _s
    discriminant = b**2 - 4*a*c
    if discriminant < 0:
        return "no real solutions"
    root = (_s.Integer(-b) - _s.sqrt(discriminant)) / (2 * a)
    return str(_s.simplify(root))

def quad_discriminant_value(a, b, c):
    return str(b**2 - 4*a*c)

def quad_complete_square_identity(b):
    p = Fraction(b, 2)
    q = -p * p
    return f"(x + {pf(p.numerator, p.denominator)})² + {pf(q.numerator, q.denominator)}"

def quad_complete_square_p(a, b, c):
    return pf(b, 2 * a)

def quad_general_axis(a, b, c):
    return pf(-b, 2 * a)

def poly_degree(a, n, b, m, c, d):
    powers_with_coeffs = [(n, a), (m, b), (1, c), (0, d)]
    non_zero = [(power, coeff) for power, coeff in powers_with_coeffs if coeff != 0]
    if not non_zero:
        return 0
    return max(power for power, _ in non_zero)


def poly_leading_coefficient(a, n, b, m, c, d):
    powers_with_coeffs = [(n, a), (m, b), (1, c), (0, d)]
    non_zero = [(power, coeff) for power, coeff in powers_with_coeffs if coeff != 0]
    if not non_zero:
        return 0
    max_power = max(power for power, _ in non_zero)
    for power, coeff in non_zero:
        if power == max_power:
            return coeff


def poly_coefficient(a, n, b, m, c, d, k):
    if k == n:
        return a
    elif k == m:
        return b
    elif k == 1:
        return c
    elif k == 0:
        return d
    else:
        return 0

def poly_quadratic_two_linear(a, b):
    return f"x^2 - {a+b}x + {a*b}"


def poly_quadratic_repeated(a):
    return f"x^2 - {2*a}x + {a*a}"


def poly_quadratic_leading(p, q, a, b):
    coeff_x2 = p * q
    coeff_x = -(p * b + q * a)
    const = a * b
    return f"{coeff_x2}x^2 - {-(coeff_x)}x + {const}" if coeff_x < 0 else f"{coeff_x2}x^2 + {coeff_x}x + {const}"


def poly_cubic_three_linear(a, b, c):
    coeff_x2 = -(a + b + c)
    coeff_x = a*b + b*c + c*a
    const = -(a * b * c)
    parts = ["x^3"]
    if coeff_x2 != 0:
        parts.append(f"{coeff_x2}x^2" if coeff_x2 < 0 else f"+ {coeff_x2}x^2")
    if coeff_x != 0:
        parts.append(f"{coeff_x}x" if coeff_x < 0 else f"+ {coeff_x}x")
    if const != 0:
        parts.append(f"{const}" if const < 0 else f"+ {const}")
    return " ".join(parts)


def poly_cubic_repeated(a):
    coeff_x2 = -3 * a
    coeff_x = 3 * a * a
    const = -(a ** 3)
    parts = ["x^3"]
    if coeff_x2 != 0:
        parts.append(f"{coeff_x2}x^2" if coeff_x2 < 0 else f"+ {coeff_x2}x^2")
    if coeff_x != 0:
        parts.append(f"{coeff_x}x" if coeff_x < 0 else f"+ {coeff_x}x")
    if const != 0:
        parts.append(f"{const}" if const < 0 else f"+ {const}")
    return " ".join(parts)


def poly_cubic_repeated_distinct(a, b):
    coeff_x2 = -(2*a + b)
    coeff_x = a*a + 2*a*b
    const = -(a*a * b)
    parts = ["x^3"]
    if coeff_x2 != 0:
        parts.append(f"{coeff_x2}x^2" if coeff_x2 < 0 else f"+ {coeff_x2}x^2")
    if coeff_x != 0:
        parts.append(f"{coeff_x}x" if coeff_x < 0 else f"+ {coeff_x}x")
    if const != 0:
        parts.append(f"{const}" if const < 0 else f"+ {const}")
    return " ".join(parts)

def poly_factor_theorem(a, b, c, d):
    return a**3 + b*a**2 + c*a + d

def poly_cubic_factor_quotient(a, b, c, d):
    coeffs = [1, b, c, d]
    result = []
    carry = 0

    for coeff in coeffs[:-1]:
        val = coeff + carry
        result.append(val)
        carry = val * a

    coeff_x2 = result[0]
    coeff_x = result[1]
    const = result[2]

    parts = []
    if coeff_x2 == 1:
        parts.append("x^2")
    elif coeff_x2 == -1:
        parts.append("-x^2")
    else:
        parts.append(f"{coeff_x2}x^2")

    if coeff_x != 0:
        if coeff_x == 1:
            parts.append("+ x")
        elif coeff_x == -1:
            parts.append("- x")
        elif coeff_x > 0:
            parts.append(f"+ {coeff_x}x")
        else:
            parts.append(f"{coeff_x}x")

    if const != 0:
        if const > 0:
            parts.append(f"+ {const}")
        else:
            parts.append(f"{const}")

    return " ".join(parts)

def poly_repeated_root(a, b):
    return f"x = {a} (repeated), x = {b}"

def func_evaluate(a, b, c, k):
    return a*k**2 + b*k + c


def func_vertical_translation(p, q, a):
    return f"({p}, {q + a})"


def func_horizontal_translation(p, q, b):
    return f"({p - b}, {q})"

def func_vertical_dilation(p, q, c):
    return f"({p}, {c * q})"


def func_horizontal_dilation(p, q, k):
    return f"({pf(p, k)}, {q})"

def comb_evaluate(n, r):
    if r < 0 or r > n:
        return "undefined"
    result = math.comb(n, r)
    return str(result)

def comb_symmetry_apply(n, r, val):
    return str(val)

def binom_expand_specific_term(n, k):
    coefficient = math.comb(n, k)
    n_minus_k = n - k

    if coefficient == 1:
        if n_minus_k == 0:
            return f"y^{k}"
        elif k == 0:
            return f"x^{n_minus_k}"
        else:
            return f"x^{n_minus_k}*y^{k}"
    else:
        if n_minus_k == 0:
            return f"{coefficient}*y^{k}"
        elif k == 0:
            return f"{coefficient}*x^{n_minus_k}"
        else:
            return f"{coefficient}*x^{n_minus_k}*y^{k}"

def binom_coeff_term(n, k):
    coefficient = math.comb(n, k)
    return str(coefficient)

def binom_term_index(r):
    return str(r + 1)

def pascal_structure_entry(n, r):
    if r < 0 or r > n:
        return "undefined"
    result = math.comb(n, r)
    return str(result)

def pascal_recurrence_apply(n, r):
    if r < 0 or r > n:
        return "undefined"
    result = math.comb(n - 1, r - 1) + math.comb(n - 1, r)
    return str(result)

def pascal_recurrence_below(n, r, a, b):
    return str(a + b)

def pascal_row_sum(n):
    return str(2 ** n)

def set_complement_size(n, k):
    return str(n - k)

def set_complement_described(k):
    return str(6 - k)

def set_intersection_size(a, b):
    gcd_val = math.gcd(a, b)
    count = 10 // gcd_val
    return str(count)

def set_intersection_explicit(n, a, b):
    if b <= a:
        return str(a - b + 1)
    else:
        return "0"

def set_union_size(a, b):
    gcd_val = math.gcd(a, b)
    size_a = 10 // a
    size_b = 10 // b
    size_intersection = 10 // gcd_val
    size_union = size_a + size_b - size_intersection
    return str(size_union)

def mutually_exclusive_check_var(n, a, b):
    if a <= b:
        return "Yes"
    else:
        return "No"

def prob_measure_valid(p):
    try:
        x = Fraction(str(p))
    except Exception:
        return "No"
    return "Yes" if 0 <= x <= 1 else "No"

def prob_complement_find(num, den):
    return str(Fraction(den - num, den))

def prob_complement_reverse(num, den):
    return str(Fraction(den - num, den))

def prob_equally_likely_basic(n, k):
    return str(Fraction(k, n))

def prob_addition_find_union(a, b, c, d):
    return str(Fraction(a + b - c, d))

def prob_addition_find_intersection(a, b, u, d):
    return str(Fraction(a + b - u, d))

def prob_rel_freq_estimate(k, n):
    return str(Fraction(k, n))

def prob_conditional_find(num, den, b):
    return str(Fraction(num, b))

def prob_conditional_find_intersection(num, den, b, d):
    return str(Fraction(num * b, den * d))

def prob_independence_check(a, d, c):
    return "Yes" if Fraction(a, d) == Fraction(c, d) else "No"

def prob_product_rule_find(a, b, d):
    return str(Fraction(a, d) * Fraction(b, d))

def prob_product_rule_find_marginal(num, den, a, d):
    return str(Fraction(num, den) / Fraction(a, d))

def pf(num, den):
    f = Fraction(num, den)
    if f.denominator == 1:
        return str(f.numerator)
    return f"{f.numerator}/{f.denominator}"

def arc_sector_theta_rad(theta_deg):
    f = Fraction(theta_deg, 180)
    if f == 1:
        return "π"
    if f == -1:
        return "-π"
    if f.denominator == 1:
        return f"{f.numerator}π"
    return f"{f.numerator}/{f.denominator}π"

def arc_length(r, theta_deg):
    coeff = Fraction(r * theta_deg, 180)
    if coeff == 1:
        return "π"
    if coeff.denominator == 1:
        return f"{coeff.numerator}π"
    return f"{coeff.numerator}/{coeff.denominator}π"

def sector_area(r, theta_deg):
    coeff = Fraction(r * r * theta_deg, 360)
    if coeff == 1:
        return "π"
    if coeff.denominator == 1:
        return f"{coeff.numerator}π"
    return f"{coeff.numerator}/{coeff.denominator}π"


def arc_sector_from_degrees(r, θ):
    theta_rad = arc_sector_theta_rad(θ)
    s = arc_length(r, θ)
    A = sector_area(r, θ)
    return {
        "theta_rad": theta_rad,
        "arc_length": s,
        "sector_area": A,
    }

_UNIT_CIRCLE_TABLE = [
    (0,  Rational(1),      Rational(0)),
    (1,  sqrt(3)/2,        Rational(1,2)),
    (2,  Rational(1,2),    sqrt(3)/2),
    (3,  Rational(0),      Rational(1)),
    (4,  -Rational(1,2),   sqrt(3)/2),
    (5,  -sqrt(3)/2,       Rational(1,2)),
    (6,  -Rational(1),     Rational(0)),
    (7,  -sqrt(3)/2,       -Rational(1,2)),
    (8,  -Rational(1,2),   -sqrt(3)/2),
    (9,  Rational(0),      -Rational(1)),
    (10, Rational(1,2),    -sqrt(3)/2),
    (11, sqrt(3)/2,        -Rational(1,2)),
]

def unit_circle_cos_sin(k):
    k = k % 12
    for kk, c, s in _UNIT_CIRCLE_TABLE:
        if kk == k:
            return c, s
    raise ValueError

def unit_circle_tan(k):
    c, s = unit_circle_cos_sin(k)
    if c == 0:
        return "undefined"
    t = s / c
    return str(t)


def unit_circle_special_angle(k):
    c, s = unit_circle_cos_sin(k)
    t = unit_circle_tan(k)
    is_undefined = "yes" if t == "undefined" else "no"
    explanation = (
        "tan θ is undefined because cos θ = 0, and tan θ = sin θ / cos θ."
        if is_undefined == "yes"
        else "tan θ is defined because cos θ ≠ 0."
    )
    return {
        "cos": str(c),
        "sin": str(s),
        "tan": t,
        "is_undefined": is_undefined,
        "explanation": explanation,
    }

def sinusoid_amplitude(A):
    return str(abs(A))

def sinusoid_period(B):
    return pf(2, abs(B))

def sinusoid_midline(D):
    return str(D)

def sinusoid_max(A, D):
    return str(D + abs(A))

def sinusoid_min(A, D):
    return str(D - abs(A))

def sinusoid_first_midline_crossing(B, C):
    best = None
    for k in range(-12, 13):
        num = k - C
        den = B
        if den == 0:
            continue
        if num * den <= 0:
            continue
        f = Fraction(num, den)
        if best is None or f < best:
            best = f
    if best is None:
        return "none"
    if best == 1:
        return "π"
    if best == -1:
        return "-π"
    if best.denominator == 1:
        return f"{best.numerator}π"
    return f"{best.numerator}/{best.denominator}π"


def sinusoid_features_and_zeros(A, B, C, D):
    amp = sinusoid_amplitude(A)
    period_coeff = sinusoid_period(B)
    mid = sinusoid_midline(D)
    mx = sinusoid_max(A, D)
    mn = sinusoid_min(A, D)
    first_cross = sinusoid_first_midline_crossing(B, C)

    return {
        "amplitude": amp,
        "period": f"{period_coeff}π",
        "midline": f"y = {mid}",
        "maximum": mx,
        "minimum": mn,
        "first_midline_crossing": first_cross,
    }

def cos_to_sin_phase_rewrite(A, B, C, D):
    C_prime = f"{C} + π/2"
    amp = sinusoid_amplitude(A)
    period_coeff = sinusoid_period(B)
    mid = sinusoid_midline(D)

    return {
        "C_prime": C_prime,
        "amplitude": amp,
        "period": f"{period_coeff}π",
        "midline": f"y = {mid}",
        "shift_explanation": (
            "Replacing cos by sin adds a phase of +π/2, so the graph shifts left by π/(2B). "
            "The period and amplitude are unchanged."
        ),
    }


_SIN_SPECIAL_MAP = {
    0: ("0", "π"),
    1: ("π/6", "5π/6"),
    2: ("π/2", "π/2"),
    3: ("π/3", "2π/3"),
    4: ("7π/6", "11π/6"),
    5: ("4π/3", "5π/3"),
}

_SIN_SPECIAL_PI = {
    0: (Fraction(0), Fraction(1)),
    1: (Fraction(1, 6), Fraction(5, 6)),
    2: (Fraction(1, 2), Fraction(1, 2)),
    3: (Fraction(1, 3), Fraction(2, 3)),
    4: (Fraction(7, 6), Fraction(11, 6)),
    5: (Fraction(4, 3), Fraction(5, 3)),
}


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


def _reduce_into_period(t, B, C):
    import sympy as _s
    lo = (_s.Integer(C) - t * _s.pi) / (2 * _s.pi)
    k = int(_s.ceiling(_s.nsimplify(lo)))
    return t + 2 * k


def sin_equation_special_angles_solver(B, C, a_choice):
    t1, t2 = _SIN_SPECIAL_PI[a_choice]
    sol1 = f"({_pi_coeff_str(_reduce_into_period(t1, B, C))} - {C})/{B}"
    sol2 = f"({_pi_coeff_str(_reduce_into_period(t2, B, C))} - {C})/{B}"
    period = f"2π/{abs(B)}"

    return {
        "solution1": sol1,
        "solution2": sol2,
        "period": period,
    }

def sin_equation_special_angles(B, C, a_choice):
    return sin_equation_special_angles_solver(B, C, a_choice)

def tan_period(B):
    return pf(1, abs(B))

def tan_asymptotes(B, C, k_min=-2, k_max=2):
    res = []
    for k in range(k_min, k_max + 1):
        num_coeff = Fraction(1, 2) + k
        coeff = num_coeff / B
        if coeff == 1:
            base = "π"
        elif coeff == -1:
            base = "-π"
        elif coeff.denominator == 1:
            base = f"{coeff.numerator}π"
        else:
            base = f"{coeff.numerator}/{coeff.denominator}π"
        if C == 0:
            res.append(base)
        else:
            shift = pf(-C, B)
            res.append(f"{base} + {shift}")
    return ", ".join(res)

_TAN_SPECIAL_MAP = {
    0: "0",
    1: "π/4",
    2: "-π/4",
    3: "π/3",
}

def tan_equation_special_angles_solver(B, C, a_choice):
    theta0 = _TAN_SPECIAL_MAP[a_choice]
    sol = f"({theta0} - {C})/{B}"
    period = f"{tan_period(B)}π"
    return {
        "solution": sol,
        "period": period,
        "note": "Other solutions are obtained by adding integer multiples of the period.",
    }

def tan_asymptotes_and_equation(B, C, a_choice):
    period = f"{tan_period(B)}π"
    asymptotes = tan_asymptotes(B, C, k_min=-2, k_max=2)
    eq_sol = tan_equation_special_angles_solver(B, C, a_choice)
    return {
        "period": period,
        "asymptotes": asymptotes,
        "equation_solution": eq_sol["solution"],
        "equation_period": eq_sol["period"],
        "equation_note": eq_sol["note"],
    }

def func_midpoint_formula(x1, y1, x2, y2):
    mx = midpoint_compute_x(x1, y1, x2, y2)
    my = midpoint_compute_y(x1, y1, x2, y2)
    return {
        "midpoint_x": mx,
        "midpoint_y": my,
    }


def func_direct_proportion_full(x1, y1, x2):
    k_num = y1
    k_den = x1
    k_str = pf(k_num, k_den)

    equation = f"y = {k_str}x"

    from fractions import Fraction
    k = Fraction(k_num, k_den)
    y_at_x2 = str(k * x2)

    y_at_0 = "0"

    return {
        "k": k_str,
        "equation": equation,
        "y_at_x2": y_at_x2,
        "y_at_0": y_at_0,
    }


def func_linearly_related_full(m, b, dx):
    if b == 0:
        equation = f"y = {m}x"
    elif b > 0:
        equation = f"y = {m}x + {b}"
    else:
        equation = f"y = {m}x - {-b}"

    graph_description = "The graph is a straight line."

    delta_y = linearly_related_rate(m, dx)

    return {
        "equation": equation,
        "graph_description": graph_description,
        "delta_y": delta_y,
    }


def func_direct_prop_vs_linear_full(m, b):
    is_direct = direct_prop_vs_linear_identify(m, b)

    justification = (
        "This is a direct proportion because b = 0, so the equation is y = mx (of the form y = kx)."
        if is_direct == "yes"
        else "This is not a direct proportion because b ≠ 0, so the equation is not of the form y = kx."
    )

    return {
        "is_direct_proportion": is_direct,
        "justification": justification,
    }

def func_linear_form_basics(m, c):
    slope = str(m)

    slope_description = linear_form_slope_sign(m, c)

    y_intercept = f"(0, {c})"

    return {
        "slope": slope,
        "slope_description": slope_description,
        "y_intercept": y_intercept,
    }


def func_linear_form_intercepts(m, c):
    y_intercept = f"(0, {c})"

    x_intercept_x = linear_form_x_intercept(m, c)
    x_intercept = f"({x_intercept_x}, 0)"

    return {
        "y_intercept": y_intercept,
        "x_intercept": x_intercept,
    }


def func_linear_form_from_two_points(x1, y1, x2, y2):
    m_str = linear_form_find_slope(x1, y1, x2, y2)

    m = Fraction(m_str) if "/" in m_str else Fraction(int(m_str), 1)
    x1_f = Fraction(x1, 1)
    y1_f = Fraction(y1, 1)
    c = y1_f - m * x1_f
    c_str = str(c) if c.denominator != 1 else str(c.numerator)

    if c == 0:
        equation = f"y = {m_str}x"
    elif c > 0:
        equation = f"y = {m_str}x + {c_str}"
    else:
        equation = f"y = {m_str}x - {-c_str}"

    return {
        "slope": m_str,
        "y_intercept_value": c_str,
        "equation": equation,
    }


def func_linear_equation_slope_yint(m, c):
    equation = linear_equation_slope_yint(m, c)
    return {
        "equation": equation,
    }


def func_linear_equation_slope_point(m, x1, y1):
    point_slope = f"y - {y1} = {m}(x - {x1})"
    simplified = linear_equation_slope_point(m, x1, y1)
    return {
        "point_slope_form": point_slope,
        "simplified_form": simplified,
    }


def func_linear_equation_two_points(x1, y1, x2, y2):
    equation = linear_equation_two_points(x1, y1, x2, y2)
    return {
        "equation": equation,
    }


def func_linear_equation_horizontal_vertical(a, b):
    horizontal = f"y = {b}"
    vertical = f"x = {a}"
    return {
        "horizontal": horizontal,
        "vertical": vertical,
    }


def func_linear_parallel_perpendicular(m1, m2):
    are_parallel = "yes" if m1 == m2 else "no"

    are_perpendicular = "yes" if m1 * m2 == -1 else "no"

    return {
        "are_parallel": are_parallel,
        "are_perpendicular": are_perpendicular,
    }

def func_quad_relation_basics(a, b, c):
    is_quadratic = "yes"

    second_diff_pattern = "constant"

    second_diff_zero_or_nonzero = "non-zero"

    second_diff_value = quad_relation_second_diff_value(a, b, c)

    return {
        "is_quadratic": is_quadratic,
        "second_diff_pattern": second_diff_pattern,
        "second_diff_zero_or_nonzero": second_diff_zero_or_nonzero,
        "second_diff_value": second_diff_value,
    }

def func_quad_formula_and_discriminant(a, b, c):
    delta_str = quad_discriminant_value(a, b, c)
    delta = int(delta_str)

    if delta > 0:
        num_solutions = "two distinct real solutions"
    elif delta == 0:
        num_solutions = "exactly one real solution"
    else:
        num_solutions = "no real solutions"

    if delta < 0:
        solutions = "none (over the real numbers)"
    elif delta == 0:
        num = -b
        den = 2 * a
        f = Fraction(num, den)
        x_str = str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"
        solutions = f"x = {x_str}"
    else:
        num = -b
        den = 2 * a
        sqrt_delta = f"sqrt({delta})"
        if den < 0:
            num = -num
            den = -den
        if den == 1:
            x1 = f"({num} - {sqrt_delta})"
            x2 = f"({num} + {sqrt_delta})"
        else:
            x1 = f"({num} - {sqrt_delta})/{den}"
            x2 = f"({num} + {sqrt_delta})/{den}"
        solutions = f"x = {x1}  or  x = {x2}"

    return {
        "discriminant": delta_str,
        "num_solutions": num_solutions,
        "solutions": solutions,
    }


def func_quad_complete_square_solve_monic(b, c):
    p = Fraction(b, 2)
    q = c - p * p

    def frac_str(f):
        if f.denominator == 1:
            return str(f.numerator)
        return f"{f.numerator}/{f.denominator}"

    p_str = frac_str(p)
    q_str = frac_str(q)

    completed = f"(x + {p_str})² + {q_str}"

    if q == 0:
        x = -p
        x_str = frac_str(x)
        solutions = f"x = {x_str}"
    elif q > 0:
        solutions = "no real solutions"
    else:
        neg_q = -q
        num = neg_q.numerator
        den = neg_q.denominator
        sqrt_term = f"sqrt({num}/{den})"
        x1 = f"-{p_str} + {sqrt_term}"
        x2 = f"-{p_str} - {sqrt_term}"
        solutions = f"x = {x1}  or  x = {x2}"

    return {
        "completed_square_form": completed,
        "p": p_str,
        "q": q_str,
        "solutions": solutions,
    }


def func_quad_complete_square_general_use(a, b, c):
    h = Fraction(-b, 2 * a)
    k = Fraction(4 * a * c - b * b, 4 * a)

    def frac_str(f):
        if f.denominator == 1:
            return str(f.numerator)
        return f"{f.numerator}/{f.denominator}"

    h_str = frac_str(h)
    k_str = frac_str(k)

    if h >= 0:
        inner = f"x - {h_str}"
    else:
        inner = f"x + {-h_str}"

    if a == 1:
        coeff_str = ""
    else:
        coeff_str = f"{a}"

    completed = f"{coeff_str}({inner})² + {k_str}"

    vertex = f"({h_str}, {k_str})"

    delta = b * b - 4 * a * c
    if delta < 0:
        solutions = "no real solutions"
    elif delta == 0:
        x = Fraction(-b, 2 * a)
        x_str = frac_str(x)
        solutions = f"x = {x_str}"
    else:
        num = -b
        den = 2 * a
        sqrt_delta = f"sqrt({delta})"
        if den < 0:
            num = -num
            den = -den
        if den == 1:
            x1 = f"({num} - {sqrt_delta})"
            x2 = f"({num} + {sqrt_delta})"
        else:
            x1 = f"({num} - {sqrt_delta})/{den}"
            x2 = f"({num} + {sqrt_delta})/{den}"
        solutions = f"x = {x1}  or  x = {x2}"

    return {
        "completed_square_form": completed,
        "h": h_str,
        "k": k_str,
        "vertex": vertex,
        "solutions": solutions,
    }


def quad_hyperbola_intersect(c_val, axis_val, d_val):
    h = axis_val
    d = d_val
    y_int = c_val
    k = (y_int - d) * (-h)
    return str(int(k)) if k == int(k) else str(k)


def hyperbola_limit_direction(a_val, b_val, d_val, large_x):
    asymptote = Fraction(d_val)
    g_val = Fraction(a_val, large_x - b_val) + asymptote
    return "greater" if g_val > asymptote else "less"


def quad_power_vertex(a_val, axis_val, c_val, n_val):
    b = -2 * a_val * axis_val
    vertex_y = a_val * axis_val**2 + b * axis_val + c_val
    power_val = axis_val ** n_val
    return f"{int(vertex_y) if vertex_y == int(vertex_y) else vertex_y}, {power_val}"


def invprop_sqrt_solve(y_val, x_val, target_val):
    k = y_val * x_val
    return pf(k, target_val ** 2)


def hyperbola_quad_axis(b_val, c_val, axis_val):
    b_quad = -2 * 1 * axis_val
    return str(int(b_quad)) if b_quad == int(b_quad) else str(b_quad)


def power_eval_compare(n_even, n_odd, eval_val, neg_val):
    import sympy as _s
    candidates = [("f", _s.Integer(eval_val) ** n_even),
                  ("g", _s.Integer(eval_val) ** n_odd),
                  ("h", _s.sqrt(eval_val))]
    return max(candidates, key=lambda kv: kv[1])[0]

def asymptote_vertex_y(a_val, b_val, d_val, a_quad):
    p = b_val
    q = d_val
    b_quad = -2 * a_quad * p
    vertex_y = a_quad * p**2 + b_quad * p + q
    return str(int(vertex_y)) if vertex_y == int(vertex_y) else str(vertex_y)


def invprop_k_solve(k_val, target_val):
    return pf(k_val, target_val)

def poly_degree_coefficient(a_val, n_val, b_val, m_val, c_val, d_val, k_val):
    degree = poly_degree(a_val, n_val, b_val, m_val, c_val, d_val)
    leading_coeff = poly_leading_coefficient(a_val, n_val, b_val, m_val, c_val, d_val)
    coeff_k = poly_coefficient(a_val, n_val, b_val, m_val, c_val, d_val, k_val)
    return f"{degree}, {leading_coeff}, {coeff_k}"

def quadratic_expand_compare(a_val, b_val, rep_val):
    const_two_linear = a_val * b_val
    const_repeated = rep_val * rep_val
    diff = const_repeated - const_two_linear
    return str(int(diff)) if diff == int(diff) else str(diff)


def quadratic_leading_expand(p_val, a_val, q_val, b_val):
    coeff_x2 = p_val * q_val
    coeff_x = -(p_val * b_val + q_val * a_val)
    const = a_val * b_val
    return f"{coeff_x2}, {coeff_x}, {const}"


def cubic_three_linear_coeffs(a_val, b_val, c_val):
    coeff_x2 = -(a_val + b_val + c_val)
    const = -(a_val * b_val * c_val)
    return f"{coeff_x2}, {const}"


def cubic_repeated_expand(a_val):
    coeff_x2 = -3 * a_val
    verification = "yes" if coeff_x2 == -3 * a_val else "no"
    return f"{coeff_x2}, {verification}"


def cubic_repeated_distinct_coeffs(a_val, b_val):
    coeff_x2 = -(2 * a_val + b_val)
    const = -(a_val * a_val * b_val)
    return f"{coeff_x2}, {const}"


def poly_match_expanded(sum_val, prod_val):
    a_plus_b = sum_val
    a_times_b = prod_val
    degree = 2
    leading_coeff = 1
    return f"{a_plus_b}, {a_times_b}, {degree}, {leading_coeff}"


def cubic_compare_forms(a_val, b_val, c_val, rep_val):
    coeff_three_linear = -(a_val + b_val + c_val)
    coeff_repeated = -3 * rep_val
    larger = "three_linear" if coeff_three_linear > coeff_repeated else "repeated"
    return larger

def cubic_vertex_form(a_val, b_val, c_val, n_val):
    turning_point = f"({b_val}, {c_val})"
    y_at_eval = a_val * n_val**3 + c_val
    return f"{turning_point}, {y_at_eval}"


def cubic_intercepts_endbehavior(k_val, a_val, b_val, c_val, eval_x):
    intercept_sum = a_val + b_val + c_val
    intercept_product = a_val * b_val * c_val
    y_at_eval = k_val * (eval_x - a_val) * (eval_x - b_val) * (eval_x - c_val)
    match = "yes" if (k_val > 0 and y_at_eval > 0) or (k_val < 0 and y_at_eval < 0) else "no"
    return f"{intercept_sum}, {intercept_product}, {y_at_eval}, {match}"


def cubic_endbehavior_compute(a_val, b_val, c_val, d_val, large_x, neg_large_x):
    y_at_large = a_val * large_x**3 + b_val * large_x**2 + c_val * large_x + d_val
    y_at_neg = a_val * neg_large_x**3 + b_val * neg_large_x**2 + c_val * neg_large_x + d_val
    pos_inf = "\u221e" if y_at_large > 0 else "\u2212\u221e"
    neg_inf = "\u221e" if y_at_neg > 0 else "\u2212\u221e"
    return f"{pos_inf}, {neg_inf}"


def cubic_vertex_intercepts(a_val, k_val, int1, int2, int3):
    y_at_h_plus_2 = a_val * 2**3 + k_val
    product_intercepts = int1 * int2 * int3
    return f"{y_at_h_plus_2}, {product_intercepts}"


def cubic_sign_from_eval(a_val, b_val, c_val, d_val, eval_x, large_x):
    y_at_eval = a_val * eval_x**3 + b_val * eval_x**2 + c_val * eval_x + d_val
    y_at_large = a_val * large_x**3 + b_val * large_x**2 + c_val * large_x + d_val
    sign_a = "positive" if a_val > 0 else "negative"
    sign_y_at_large = "positive" if y_at_large > 0 else "negative"
    return f"{y_at_eval}, {sign_a}, {y_at_large}, {sign_y_at_large}"


def cubic_translate_turning(a_val, b_val, c_val, dx_val, dy_val):
    new_b = b_val + dx_val
    new_c = c_val + dy_val
    new_turning = f"({new_b}, {new_c})"
    new_eq = f"y = {a_val}(x−{new_b})³ + {new_c}"
    return f"{new_eq}, {new_turning}"


def cubic_intercept_product(k_val, a_val, b_val, c_val):
    product = a_val * b_val * c_val
    constant_term = -k_val * a_val * b_val * c_val
    return f"{product}, {constant_term}"


def cubic_endbehavior_from_coeffs(a_val, b_val, c_val, d_val, test_x, large_x):
    y_at_test = a_val * test_x**3 + b_val * test_x**2 + c_val * test_x + d_val
    y_at_large = a_val * large_x**3 + b_val * large_x**2 + c_val * large_x + d_val
    sign_at_large = "positive" if y_at_large > 0 else "negative"
    return f"{y_at_test}, {y_at_large}, {sign_at_large}"

def factor_theorem_verify(b_val, c_val, d_val, a_val):
    p_a = poly_factor_theorem(a_val, b_val, c_val, d_val)
    return "factor" if p_a == 0 else "not a factor"

def repeated_root_identify(a_val, b_val):
    coeff_x2 = -(2 * a_val + b_val)
    coeff_x = a_val**2 + 2 * a_val * b_val
    const = -(a_val**2 * b_val)
    check = poly_factor_theorem(a_val, coeff_x2, coeff_x, const)
    quotient_str = poly_cubic_factor_quotient(a_val, coeff_x2, coeff_x, const)
    sum_roots = 2 * a_val + b_val
    return f"{coeff_x2}, {coeff_x}, {const}, {check}, {quotient_str}, {sum_roots}"


def circle_standard_point(r_sq_val, x_val):
    import sympy as _s
    y_sq = r_sq_val - x_val**2
    if y_sq < 0:
        return "undefined"
    y_val = _s.sqrt(y_sq)
    return f"{y_val}, -{y_val}" if y_val != 0 else "0"


def circle_general_center(h_val, k_val, r_sq_val, offset_x, offset_y):
    import sympy as _s
    centre = f"({h_val}, {k_val})"
    r = _s.sqrt(r_sq_val)
    check = offset_x**2 + offset_y**2
    on_circle = "yes" if check == r_sq_val else "no"
    return f"{centre}, {r}, {on_circle}"


def factor_circle_intersect(b_val, c_val, d_val, a_val, r_val):
    p_a = poly_factor_theorem(a_val, b_val, c_val, d_val)
    area = f"{r_val**2}π" if r_val != 1 else "π"
    return f"{p_a}, {area}"


def repeated_root_expanded(a_val, b_val):
    coeff_x2 = -(2 * a_val + b_val)
    coeff_x = a_val**2 + 2 * a_val * b_val
    const = -(a_val**2 * b_val)
    return str(coeff_x2 + coeff_x + const)

def circle_function_eval(h_val, k_val, r_sq_val, offset):
    import sympy as _s
    centre = f"({h_val}, {k_val})"
    x_val = h_val + offset
    y_sq = r_sq_val - (x_val - h_val)**2
    y_val = k_val + _s.sqrt(y_sq) if y_sq >= 0 else "undefined"
    return f"{centre}, {y_val}"

def transform_vertical_sequence(c_val, a_val, eval_x):
    final_eq = f"y = {c_val}x² + {a_val}"
    y_at_eval = c_val * eval_x**2 + a_val
    return f"{final_eq}, {y_at_eval}"


def transform_horizontal_sequence(k_val, shift_val):
    h = shift_val * k_val
    final_eq = f"y = ({k_val}x - {h})²" if h > 0 else f"y = ({k_val}x + {-h})²"
    return final_eq


def transform_combined_order(k_val, c_val, h_val, v_val):
    final_eq = f"y = {c_val}({k_val}x - {k_val*h_val})² + {v_val}"
    vertex = f"({h_val}, {v_val})"
    return f"{final_eq}, {vertex}"


def transform_point_mapping(x_val, y_val, h_val, v_val):
    new_x = x_val + h_val
    new_y = y_val + v_val
    transformed_eq = f"y = f(x - {h_val}) + {v_val}"
    return f"({new_x}, {new_y}), {transformed_eq}"


def transform_dilation_point(x_val, y_val, c_val, k_val):
    return f"({pf(x_val, k_val)}, {c_val * y_val})"


def transform_reverse_find_original(c_val, v_val, h_val, final_h, final_v):
    return f"({final_h - h_val}, {pf(final_v - v_val, c_val)})"


def transform_compare_outputs(c_val, a_val, eval_x):
    y1 = c_val * eval_x**2 + a_val
    y2 = c_val * (eval_x**2 + a_val)
    return "dilation_first" if y1 > y2 else "translation_first"

def transform_horizontal_dilation_eval(k_val, h_val, eval_x):
    transformed_x = k_val * (eval_x - h_val)
    y_at_eval = transformed_x**2
    return str(int(y_at_eval)) if y_at_eval == int(y_at_eval) else str(y_at_eval)


def combination_compute_compare(n_val, r_val, n_minus_r_val):
    c1 = math.comb(n_val, r_val)
    c2 = math.comb(n_val, n_minus_r_val)
    equal = "yes" if c1 == c2 else "no"
    return f"{c1}, {c2}, {equal}"


def combination_boundary_sum(n_val, r_val):
    total = math.comb(n_val, 0) + math.comb(n_val, n_val) + math.comb(n_val, 1)
    return pf(total, math.comb(n_val, r_val))

def combination_range_valid(n_val, r_val):
    if r_val < 0 or r_val > n_val:
        return "invalid, r out of range"
    else:
        result = math.comb(n_val, r_val)
        return f"valid, {result}"


def combination_symmetry_find_r(n_val, r1_val, r2_val):
    c1 = math.comb(n_val, r1_val)
    c2 = math.comb(n_val, r2_val)
    sum_r = r1_val + r2_val
    equals_n = "yes" if sum_r == n_val else "no"
    return f"{c1}, {c2}, {equals_n}"


def combination_ratio(n_val, r_val, r_minus_1_val):
    c_r = math.comb(n_val, r_val)
    c_r_minus_1 = math.comb(n_val, r_minus_1_val)
    ratio = pf(c_r, c_r_minus_1)
    return ratio


def combination_sum_adjacent(n_val, r_val, r_plus_1_val):
    c_r = math.comb(n_val, r_val)
    c_r_plus_1 = math.comb(n_val, r_plus_1_val)
    total = c_r + c_r_plus_1
    return str(total)


def combination_boundary_product(n_val, r_val):
    c0 = math.comb(n_val, 0)
    cn = math.comb(n_val, n_val)
    cr = math.comb(n_val, r_val)
    product = c0 * cn * cr
    comparison = "equal" if product == cr else "different"
    return f"{product}, {comparison}"


def combination_symmetry_application(n_val, r_val, n_minus_r_val, known_val):
    c_r = math.comb(n_val, r_val)
    c_n_minus_r = math.comb(n_val, n_minus_r_val)
    symmetry_holds = "yes" if c_r == c_n_minus_r else "no"
    c0 = math.comb(n_val, 0)
    cn = math.comb(n_val, n_val)
    boundary_check = "yes" if c0 == 1 and cn == 1 else "no"
    return f"{c_r}, {symmetry_holds}, {boundary_check}"

def binom_expand_specific(n_val, k_val, n_minus_k_val):
    coeff = math.comb(n_val, k_val)
    term_number = k_val + 1
    return f"{coeff}, {ordinal(term_number)}"


def binom_coeff_sum(n_val):
    total = 2 ** n_val
    verification = "yes" if total == 2 ** n_val else "no"
    return f"{total}, {verification}"


def pascal_row_entry(n_val, r_val, n_minus_1_val):
    c_n_r = math.comb(n_val, r_val)
    c_n1_r1 = math.comb(n_minus_1_val, r_val - 1) if r_val > 0 else 0
    c_n1_r = math.comb(n_minus_1_val, r_val) if r_val <= n_minus_1_val else 0
    recurrence_check = "yes" if c_n_r == c_n1_r1 + c_n1_r else "no"
    return f"{c_n_r}, {recurrence_check}"


def binom_term_compare(n_val, k1_val, k2_val):
    c1 = math.comb(n_val, k1_val)
    c2 = math.comb(n_val, k2_val)
    return "first" if c1 > c2 else ("second" if c2 > c1 else "equal")

def pascal_recurrence_verify(n_val, r_val, n_minus_1_val, r_minus_1_val):
    c_n_r = math.comb(n_val, r_val)
    c_n1_r1 = math.comb(n_minus_1_val, r_minus_1_val)
    c_n1_r = math.comb(n_minus_1_val, r_val)
    sum_above = c_n1_r1 + c_n1_r
    holds = "yes" if c_n_r == sum_above else "no"
    return f"{c_n_r}, {sum_above}, {holds}"


def binom_row_sum_compare(n_val, m_val):
    sum_n = 2 ** n_val
    sum_m = 2 ** m_val
    ratio = pf(sum_n, sum_m) if sum_n >= sum_m else pf(sum_m, sum_n)
    return f"{sum_n}, {sum_m}, {ratio}"


def binom_specific_term_value(n_val, k_val, n_minus_k_val):
    return str(math.comb(n_val, k_val) * (2 ** n_minus_k_val))

def pascal_symmetry_sum(n_val, r_val, n_minus_r_val):
    total = math.comb(n_val, r_val) + math.comb(n_val, n_minus_r_val)
    return pf(total, 2 ** n_val)

def outcome_sample_space_count(die_faces, coin_sides):
    total_outcomes = die_faces * coin_sides
    return str(total_outcomes)


def event_subset_verify(n_val, e1_val, e2_val, e3_val):
    outcomes = [e1_val, e2_val, e3_val]
    all_in_S = all(1 <= e <= n_val for e in outcomes)
    subset_check = "yes" if all_in_S else "no"
    ratio = pf(len(outcomes), n_val)
    return f"{subset_check}, {ratio}"


def sample_space_cardinality(n_val, sum_val):
    total = n_val * n_val
    count_sum = 0
    for i in range(1, n_val + 1):
        for j in range(1, n_val + 1):
            if i + j == sum_val:
                count_sum += 1
    return f"{total}, {count_sum}"


def event_complement_size(total_val, a_val):
    return pf(total_val - a_val, total_val)

def outcome_event_membership(n_val, mult_val, test_val):
    in_A = "yes" if test_val % mult_val == 0 and test_val <= n_val else "no"
    outcomes_in_A = [i for i in range(1, n_val + 1) if i % mult_val == 0]
    count = len(outcomes_in_A)
    return f"{in_A}, {count}"


def sample_space_union_intersect(n_val, a1_val, a2_val, a3_val, b1_val, b2_val, b3_val):
    A = {a1_val, a2_val, a3_val}
    B = {b1_val, b2_val, b3_val}
    union = A | B
    intersect = A & B
    return f"{len(union)}, {len(intersect)}"


def event_probability_from_count(total_val, a_val, b_val):
    p_a = pf(a_val, total_val)
    p_b = pf(b_val, total_val)
    return f"{p_a}, {p_b}"


def outcome_counting_principle(choice1_val, choice2_val):
    total = choice1_val * choice2_val
    return str(total)

def prob_set_ops_interval(N, d, M):
    size_A = N // d
    size_B = M
    size_D = M // d
    size_E = size_A + size_B - size_D

    description_C = "{x in S : x is NOT divisible by d}"

    mutually_exclusive_DC = "Yes"
    justification_ME = (
        "D = A ∩ B is a subset of A, while C = A' contains only elements not in A. "
        "Hence D ∩ C = ∅, so by definition D and C are mutually exclusive."
    )

    return {
        "description_C": description_C,
        "size_D": size_D,
        "size_E": size_E,
        "mutually_exclusive_DC": mutually_exclusive_DC,
        "justification_ME": justification_ME,
    }

def prob_spinner_partition_complement(N, m):
    size_S = N
    size_A = m
    size_B = N - m

    P_A = Fraction(size_A, size_S)
    P_B = Fraction(size_B, size_S)

    P_A_valid = "Yes"
    P_B_valid = "Yes"

    P_A_if_m0 = Fraction(0, 1)
    type_A_if_m0 = "impossible"

    P_A_if_mN = Fraction(1, 1)
    type_A_if_mN = "certain"

    B_is_complement_of_A = "Yes"
    P_B_via_complement = Fraction(1, 1) - P_A

    return {
        "size_S": size_S,
        "size_A": size_A,
        "size_B": size_B,
        "P_A": str(P_A),
        "P_B": str(P_B),
        "P_A_valid": P_A_valid,
        "P_B_valid": P_B_valid,
        "P_A_if_m0": str(P_A_if_m0),
        "type_A_if_m0": type_A_if_m0,
        "P_A_if_mN": str(P_A_if_mN),
        "type_A_if_mN": type_A_if_mN,
        "B_is_complement_of_A": B_is_complement_of_A,
        "P_B_via_complement": str(P_B_via_complement),
    }


def prob_die_impossible_certain_complement():
    N = 6
    size_A = 3
    size_B = 0
    size_C = N

    P_A = Fraction(size_A, N)
    P_B = Fraction(size_B, N)
    P_C = Fraction(size_C, N)

    impossible_event = "B"
    certain_event = "C"

    P_D = Fraction(1, 1) - P_A

    return {
        "size_S": N,
        "size_A": size_A,
        "size_B": size_B,
        "size_C": size_C,
        "P_A": str(P_A),
        "P_B": str(P_B),
        "P_C": str(P_C),
        "impossible_event": impossible_event,
        "certain_event": certain_event,
        "P_D": str(P_D),
    }


def prob_construct_0_1_general_complement(N, m):
    desc_E0 = "empty set"
    type_E0 = "impossible"
    P_E0 = Fraction(0, 1)

    desc_E1 = "S"
    type_E1 = "certain"
    P_E1 = Fraction(1, 1)

    P_Em = Fraction(m, N)

    P_F_complement = Fraction(1, 1) - P_Em
    P_F_direct = Fraction(N - m, N)

    return {
        "desc_E0": desc_E0,
        "type_E0": type_E0,
        "P_E0": str(P_E0),
        "desc_E1": desc_E1,
        "type_E1": type_E1,
        "P_E1": str(P_E1),
        "P_Em": str(P_Em),
        "P_F_complement": str(P_F_complement),
        "P_F_direct": str(P_F_direct),
    }


def prob_two_nested_events_certain(N, k, m):
    size_A = k
    size_B = m
    size_C = N

    P_A = Fraction(size_A, N)
    P_B = Fraction(size_B, N)
    P_C = Fraction(size_C, N)

    certain_event = "C"

    P_A_if_k0 = Fraction(0, 1)
    type_A_if_k0 = "impossible"

    P_D = Fraction(1, 1) - P_B

    return {
        "size_A": size_A,
        "size_B": size_B,
        "size_C": size_C,
        "P_A": str(P_A),
        "P_B": str(P_B),
        "P_C": str(P_C),
        "certain_event": certain_event,
        "P_A_if_k0": str(P_A_if_k0),
        "type_A_if_k0": type_A_if_k0,
        "P_D": str(P_D),
    }

from fractions import Fraction


def prob_addition_relative_frequency(N, n_A, n_B, n_AB, n_AuB):
    P_A = Fraction(n_A, N)
    P_B = Fraction(n_B, N)
    P_AB = Fraction(n_AB, N)

    P_AuB_via_addition = P_A + P_B - P_AB
    P_AuB_direct = Fraction(n_AuB, N)

    return {
        "P_A": str(P_A),
        "P_B": str(P_B),
        "P_AB": str(P_AB),
        "P_AuB_via_addition": str(P_AuB_via_addition),
        "P_AuB_direct": str(P_AuB_direct),
    }


def prob_conditional_independence_check(N, a, b, c):
    P_A = Fraction(a, N)
    P_B = Fraction(b, N)
    P_AB = Fraction(c, N)

    P_A_given_B = P_AB / P_B
    independent = (P_A_given_B == P_A)

    P_A_times_P_B = P_A * P_B
    product_rule_holds = (P_AB == P_A_times_P_B)

    return {
        "P_A": str(P_A),
        "P_B": str(P_B),
        "P_AB": str(P_AB),
        "P_A_given_B": str(P_A_given_B),
        "independent": "Yes" if independent else "No",
        "P_A_times_P_B": str(P_A_times_P_B),
        "product_rule_holds": "Yes" if product_rule_holds else "No",
    }


def prob_rel_freq_conditional_independence(N, n_A, n_B, n_AB):
    P_A = Fraction(n_A, N)
    P_B = Fraction(n_B, N)
    P_AB = Fraction(n_AB, N)

    P_A_given_B = P_AB / P_B
    independent = (P_A_given_B == P_A)

    P_A_times_P_B = P_A * P_B
    product_rule_holds = (P_AB == P_A_times_P_B)

    return {
        "P_A": str(P_A),
        "P_B": str(P_B),
        "P_AB": str(P_AB),
        "P_A_given_B": str(P_A_given_B),
        "independent": "Yes" if independent else "No",
        "P_A_times_P_B": str(P_A_times_P_B),
        "product_rule_holds": "Yes" if product_rule_holds else "No",
    }


def prob_addition_conditional_independence(N, a, b, c):
    P_A = Fraction(a, N)
    P_B = Fraction(b, N)
    P_AB = Fraction(c, N)

    P_AuB = P_A + P_B - P_AB
    P_A_given_B = P_AB / P_B
    independent = (P_A_given_B == P_A)

    if independent:
        P_AuB_indep = P_A + P_B - P_A * P_B
        P_AuB_indep_str = str(P_AuB_indep)
        simplification_valid = "Yes"
    else:
        P_AuB_indep_str = None
        simplification_valid = "No"

    return {
        "P_A": str(P_A),
        "P_B": str(P_B),
        "P_AB": str(P_AB),
        "P_AuB": str(P_AuB),
        "P_A_given_B": str(P_A_given_B),
        "independent": "Yes" if independent else "No",
        "simplification_valid": simplification_valid,
        "P_AuB_indep": P_AuB_indep_str,
    }


import sympy as _sp


def _pi_str(n, d=1):
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


def exact_value(func, angle):
    theta = _sp.sympify(angle, locals={"pi": _sp.pi})
    fn = {"sin": _sp.sin, "cos": _sp.cos, "tan": _sp.tan}[func]
    v = _sp.simplify(fn(theta))
    if v.has(_sp.zoo) or v.has(_sp.oo):
        return "undefined"
    return str(v)


def period_recall_sin():
    return _pi_str(2)


def period_scale_sin(b):
    return _pi_str(2, abs(b))


def period_scale_cos(b):
    return _pi_str(2, abs(b))


_SIN_EQ_SOLUTIONS = {
    "0": [(0, 1), (1, 1)],
    "1/2": [(1, 6), (5, 6)],
    "sqrt(2)/2": [(1, 4), (3, 4)],
    "sqrt(3)/2": [(1, 3), (2, 3)],
    "-1/2": [(7, 6), (11, 6)],
}


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


def sin_eq_special(val):
    return ", ".join(_pi_str(n, d) for n, d in _SIN_EQ_SOLUTIONS[val])


INF, NEG_INF = "∞", "−∞"


def cubic_end_pos_pos(a, b, c, d):
    return INF if a > 0 else NEG_INF


def cubic_end_pos_neg(a, b, c, d):
    return NEG_INF if a > 0 else INF


def cubic_end_neg_pos(a, b, c, d):
    return NEG_INF if a < 0 else INF


def cubic_end_neg_neg(a, b, c, d):
    return INF if a < 0 else NEG_INF


def cubic_vertex_turning_x(a, b, c):
    return str(b)


def cubic_vertex_turning_y(a, b, c):
    return str(c)


def circle_standard_centre_radius(r):
    return f"(0, 0), {r}"


def hyperbola_vertical_asymptote(a, b):
    return f"x = {b}"


def hyperbola_horizontal_asymptote(a, b, d):
    return f"y = {d}"


def inv_proportion_equation(x1, y1):
    return f"y = {x1 * y1}/x"


def pow_natural_even_limit(n):
    return INF


def pow_natural_odd_limit(n):
    return NEG_INF


def pow_neg1_asymptotes():
    return "x = 0, y = 0"


def power_sqrt_domain():
    return "x >= 0"


def quad_general_y_intercept(a, b, c):
    return f"(0, {c})"


def binom_coeff_name(n):
    return "binomial coefficients"


def comb_boundary_zero(n):
    return str(math.comb(n, 0))


def comb_boundary_self(n):
    return str(math.comb(n, n))


def comb_range(n):
    return f"0 <= r <= {n}"


def prob_certain_type():
    return "certain"


def prob_impossible_type():
    return "impossible"


def prob_event_is_subset():
    return "a subset of the sample space"


def prob_event_membership(n, k):
    return "yes" if 1 <= k <= n else "no"


def prob_sample_space_list(n):
    return "{" + ", ".join(str(i) for i in range(1, n + 1)) + "}"


def prob_sample_space_is():
    return "the set of all possible outcomes"


def prob_outcome_is():
    return "a single possible result of the experiment"
