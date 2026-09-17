"""View: представление данных модели для API (JSON) и консоли (текст)."""
from typing import Literal

from pydantic import BaseModel

from calc_tdd.model import Record

Operation = Literal["add", "subtract", "multiply", "divide", "power",
                    "sqrt", "negate"]

SYMBOLS = {
    "add": "+",
    "subtract": "-",
    "multiply": "*",
    "divide": "/",
    "power": "^",
}


class CalculationRequest(BaseModel):
    operation: Operation
    a: float
    b: float | None = None


class CalculationResponse(BaseModel):
    operation: str
    a: float
    b: float | None
    result: float
    expression: str

    @classmethod
    def from_record(cls, record: Record):
        return cls(
            operation=record.operation,
            a=record.a,
            b=record.b,
            result=record.result,
            expression=as_text(record),
        )


def format_number(value):
    if float(value).is_integer():
        return str(int(value))
    return f"{value:.10g}"


def as_text(record: Record):
    a = format_number(record.a)
    result = format_number(record.result)
    if record.b is None:
        return f"{record.operation}({a}) = {result}"
    symbol = SYMBOLS[record.operation]
    return f"{a} {symbol} {format_number(record.b)} = {result}"
