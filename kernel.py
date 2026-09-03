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
