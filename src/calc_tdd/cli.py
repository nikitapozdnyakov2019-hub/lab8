"""Консольный интерфейс: calc-tdd 2 + 3, calc-tdd sqrt 16."""
import argparse
import sys

from calc_tdd.model import Calculator, CalculatorError
from calc_tdd.views import SYMBOLS, as_text

OPERATION_BY_SYMBOL = {symbol: name for name, symbol in SYMBOLS.items()}


def parse_args(argv):
    parser = argparse.ArgumentParser(
        prog="calc-tdd",
        description="Калькулятор. Примеры: '2 + 3', '2 ^ 8', 'sqrt 16'.",
    )
    parser.add_argument("tokens", nargs="+",
                        help="выражение: A OP B или FUNC A")
    return parser.parse_args(argv)


def to_call(tokens):
    """['2', '+', '3'] -> ('add', 2.0, 3.0); ['sqrt', '9'] -> ('sqrt', 9.0)."""
    if len(tokens) == 3 and tokens[1] in OPERATION_BY_SYMBOL:
        return OPERATION_BY_SYMBOL[tokens[1]], float(tokens[0]), float(
            tokens[2])
    if len(tokens) == 2:
        return tokens[0], float(tokens[1]), None
    raise CalculatorError("не удалось разобрать выражение")


def main(argv=None):
    args = parse_args(sys.argv[1:] if argv is None else argv)
    calc = Calculator()
    try:
        calc.calculate(*to_call(args.tokens))
    except (CalculatorError, ValueError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1
    print(as_text(calc.history[-1]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
