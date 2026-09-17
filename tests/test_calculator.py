import math

import pytest

from calc_tdd import Calculator, CalculatorError, Record


@pytest.fixture()
def calc():
    return Calculator()


@pytest.mark.parametrize("operation, a, b, expected", [
    ("add", 2, 3, 5),
    ("add", -1.5, 0.5, -1),
    ("subtract", 10, 4, 6),
    ("multiply", 3, -4, -12),
    ("divide", 10, 4, 2.5),
    ("power", 2, 10, 1024),
    ("power", 9, 0.5, 3),
])
def test_binary_operations(calc, operation, a, b, expected):
    assert calc.calculate(operation, a, b) == pytest.approx(expected)


def test_unary_operations(calc):
    assert calc.calculate("sqrt", 16) == 4
    assert calc.calculate("negate", 7) == -7


def test_shortcut_methods(calc):
    assert calc.add(1, 2) == 3
    assert calc.subtract(1, 2) == -1
    assert calc.multiply(2, 2) == 4
    assert calc.divide(1, 4) == 0.25


def test_float_precision(calc):
    assert calc.add(0.1, 0.2) == pytest.approx(0.3)


@pytest.mark.parametrize("operation, a, b", [
    ("divide", 1, 0),
    ("sqrt", -4, None),
    ("power", -8, 1 / 3),
    ("power", 0, -1),
    ("modulo", 5, 2),
    ("add", 1, None),
    ("sqrt", 4, 2),
])
def test_errors(calc, operation, a, b):
    with pytest.raises(CalculatorError):
        calc.calculate(operation, a, b)


def test_error_is_value_error():
    assert issubclass(CalculatorError, ValueError)


def test_history_records_successful_calls(calc):
    calc.add(1, 2)
    with pytest.raises(CalculatorError):
        calc.divide(1, 0)
    calc.calculate("sqrt", 9)
    assert calc.history == [Record("add", 1, 2, 3),
                            Record("sqrt", 9, None, 3)]


def test_history_is_copy(calc):
    calc.add(1, 1)
    calc.history.clear()
    assert len(calc.history) == 1


def test_history_limit():
    calc = Calculator(history_limit=3)
    for i in range(5):
        calc.add(i, 0)
    assert [r.a for r in calc.history] == [2, 3, 4]


def test_clear_history(calc):
    calc.add(1, 1)
    calc.clear_history()
    assert calc.history == []


def test_operations_list():
    assert Calculator.operations() == sorted(
        ["add", "subtract", "multiply", "divide", "power", "sqrt", "negate"])


def test_large_power_overflow(calc):
    with pytest.raises(CalculatorError):
        calc.calculate("power", 10.0, 1000)
    assert not math.isinf(calc.calculate("power", 10, 10))
