"""Model: бизнес-логика калькулятора, не знает ни про HTTP, ни про консоль."""
import math
import operator
from dataclasses import dataclass


class CalculatorError(ValueError):
    """Ошибка вычисления, понятная пользователю."""


@dataclass(frozen=True)
class Record:
    operation: str
    a: float
    b: float | None
    result: float


def _divide(a, b):
    if b == 0:
        raise CalculatorError("деление на ноль")
    return a / b


def _power(a, b):
    try:
        result = a ** b
    except (OverflowError, ZeroDivisionError) as error:
        raise CalculatorError(f"не удалось возвести в степень: {error}")
    if isinstance(result, complex):
        raise CalculatorError("результат не является вещественным числом")
    return result


def _sqrt(a):
    if a < 0:
        raise CalculatorError("корень из отрицательного числа")
    return math.sqrt(a)


BINARY = {
    "add": operator.add,
    "subtract": operator.sub,
    "multiply": operator.mul,
    "divide": _divide,
    "power": _power,
}
UNARY = {
    "sqrt": _sqrt,
    "negate": operator.neg,
}


class Calculator:
    def __init__(self, history_limit=100):
        self.history_limit = history_limit
        self._history = []

    @staticmethod
    def operations():
        return sorted([*BINARY, *UNARY])

    @property
    def history(self):
        return list(self._history)

    def clear_history(self):
        self._history.clear()

    def calculate(self, operation, a, b=None):
        if operation in BINARY:
            if b is None:
                raise CalculatorError(f"операции {operation} нужны два числа")
            result = BINARY[operation](a, b)
        elif operation in UNARY:
            if b is not None:
                raise CalculatorError(f"операции {operation} нужно одно число")
            result = UNARY[operation](a)
        else:
            raise CalculatorError(f"неизвестная операция: {operation}")

        self._remember(Record(operation, a, b, result))
        return result

    def _remember(self, record):
        self._history.append(record)
        if len(self._history) > self.history_limit:
            del self._history[0]

    # короткие методы для использования как библиотеки
    def add(self, a, b):
        return self.calculate("add", a, b)

    def subtract(self, a, b):
        return self.calculate("subtract", a, b)

    def multiply(self, a, b):
        return self.calculate("multiply", a, b)

    def divide(self, a, b):
        return self.calculate("divide", a, b)
