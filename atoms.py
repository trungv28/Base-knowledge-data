from fractions import Fraction
import sympy as sp

from kernel import atom, REGISTRY, KIND, render


@atom("func.direct_proportion.constant_ratio")
def direct_proportion_constant_ratio(y, x):
    return Fraction(y, x)


@atom("func.inv_proportion.definition")
def inv_proportion_constant(x, y):
    return x * y


@atom("func.inv_proportion.evaluate")
def inv_proportion_evaluate(k, x):
    return Fraction(k, x)


@atom("func.linear_solve.one_step")
def linear_solve_one_step(a, b):
    return Fraction(b, a)


@atom("func.quad_general.axis")
def quad_general_axis(coeffs):
    a, b, _ = coeffs
    return Fraction(-b, 2 * a)


@atom("func.quad_general.y_intercept")
def quad_general_y_intercept(coeffs):
    return coeffs[-1]


@atom("func.poly.quadratic_two_linear")
def poly_quadratic_two_linear(a, b):
    return (1, -(a + b), a * b)


@atom("func.poly.quadratic_repeated")
def poly_quadratic_repeated(a):
    return (1, -2 * a, a * a)


@atom("func.poly.factor_theorem")
def poly_factor_theorem(p_at_a):
    return "yes" if p_at_a == 0 else "no"


@atom("func.poly.cubic_factor_quotient")
def poly_cubic_factor_quotient(a, b, c, d):
    if a**3 + b * a**2 + c * a + d != 0:
        raise ValueError("(x - a) is not a factor")
    q1 = b + a
    return (1, q1, c + a * q1)


@atom("func.poly.cubic_three_linear")
def poly_cubic_three_linear(a, b, c):
    return (1, -(a + b + c), a*b + b*c + c*a, -(a * b * c))


@atom("func.transform.poly_vertical_translation")
def poly_vertical_translation(coeffs, a):
    return tuple(coeffs[:-1]) + (coeffs[-1] + a,)


@atom("func.transform.poly_vertical_dilation")
def poly_vertical_dilation(coeffs, c):
    return tuple(c * k for k in coeffs)


@atom("func.hyperbola.evaluate")
def hyperbola_evaluate(a, b, d, x):
    if x == b:
        raise ValueError("x is the vertical asymptote")
    return Fraction(a, x - b) + d


@atom("func.quad_general.axis_coefficient")
def quad_coefficient_from_axis(a, axis):
    return -2 * a * axis


@atom("func.notation.evaluate")
def notation_evaluate(coeffs, x):
    out = 0
    for k in coeffs:
        out = out * x + k
    return out


@atom("func.hyperbola.vertical_asymptote")
def hyperbola_vertical_asymptote(b):
    return b


@atom("func.hyperbola.horizontal_asymptote")
def hyperbola_horizontal_asymptote(d):
    return d


@atom("func.transform.vertical_translation")
def transform_vertical_translation(y, a):
    return y + a


@atom("func.transform.inverse_vertical_translation")
def inverse_vertical_translation(y, a):
    return y - a


@atom("func.transform.horizontal_translation")
def transform_horizontal_translation(x, h):
    return x + h


@atom("func.transform.inverse_horizontal_translation")
def inverse_horizontal_translation(x, h):
    return x - h


@atom("func.transform.vertical_dilation")
def transform_vertical_dilation(y, c):
    return c * y


@atom("func.transform.inverse_vertical_dilation")
def inverse_vertical_dilation(y, c):
    return Fraction(y, c) if isinstance(y, int) and isinstance(c, int) else y / c


@atom("func.direct_proportion.evaluate")
def direct_proportion_evaluate(k, x):
    return k * x


@atom("func.transform.horizontal_dilation")
def transform_horizontal_dilation(x, k):
    return Fraction(x, k)


@atom("func.transform.inverse_horizontal_dilation")
def inverse_horizontal_dilation(x, k):
    return x * k


@atom("func.sqrt.principal")
def sqrt_principal(t):
    return sp.sqrt(t)
