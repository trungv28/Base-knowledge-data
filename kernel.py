from fractions import Fraction
import math

import sympy as sp


REGISTRY = {}


KIND = {}


def kernel(op_id):
    def deco(f):
        REGISTRY[op_id] = f
        KIND[op_id] = "kernel"
        return f
    return deco


def atom(atom_id):
    def deco(f):
        REGISTRY[atom_id] = f
        KIND[atom_id] = "knowledge"
        f.atom_id = atom_id
        return f
    return deco


def render(v):
    if isinstance(v, tuple):
        return "(" + ", ".join(render(x) for x in v) + ")"
    if isinstance(v, Fraction):
        return str(v.numerator) if v.denominator == 1 else f"{v.numerator}/{v.denominator}"
    return str(v)


@kernel("kernel.add")
def _add(x, y): return x + y


@kernel("kernel.subtract")
def _subtract(x, y): return x - y


@kernel("kernel.multiply")
def _multiply(x, y): return x * y


@kernel("kernel.divide")
def _divide(x, y):
    if y == 0:
        raise ValueError("kernel.divide by zero")
    return Fraction(x, y) if isinstance(x, int) and isinstance(y, int) else x / y


@kernel("kernel.negate")
def _negate(x): return -x


@kernel("kernel.integer_power")
def _integer_power(x, n): return x ** n


@kernel("kernel.equal")
def _equal(x, y): return x == y


@kernel("kernel.less_than")
def _less_than(x, y): return x < y


@kernel("kernel.make_point")
def _make_point(x, y): return (x, y)


@kernel("kernel.make_vector")
def _make_vector(xs): return tuple(xs)


@kernel("kernel.get_coordinate")
def _get_coordinate(p, i): return p[i]


@kernel("kernel.get_entry")
def _get_entry(v, i): return v[i]


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


def coeff_poly(coeffs):
    top = len(coeffs) - 1
    return poly([(top - i, k) for i, k in enumerate(coeffs)])


def display(v, mode=None):
    if mode == "polynomial":
        return coeff_poly(v)
    if mode == "capitalize":
        return str(v).capitalize()
    if mode and "{}" in mode:
        return mode.format(render(v))
    return render(v)
