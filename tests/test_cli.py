import pytest

from calc_tdd.cli import main, to_call
from calc_tdd.model import CalculatorError


def test_to_call():
    assert to_call(["2", "+", "3"]) == ("add", 2.0, 3.0)
    assert to_call(["sqrt", "9"]) == ("sqrt", 9.0, None)
    with pytest.raises(CalculatorError):
        to_call(["1", "2", "3", "4"])


def test_main_success(capsys):
    assert main(["2", "^", "8"]) == 0
    assert capsys.readouterr().out.strip() == "2 ^ 8 = 256"


def test_main_error(capsys):
    assert main(["1", "/", "0"]) == 1
    assert "деление на ноль" in capsys.readouterr().err
