"""Controller: HTTP-маршруты принимают запрос, вызывают модель, отдают view."""
from fastapi import Depends, FastAPI, HTTPException, Request, status

from calc_tdd.model import Calculator, CalculatorError
from calc_tdd.views import CalculationRequest, CalculationResponse


def create_app(calculator=None):
    app = FastAPI(title="calc-tdd", version="0.1.0")
    app.state.calculator = calculator or Calculator()

    def get_calculator(request: Request) -> Calculator:
        return request.app.state.calculator

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.get("/operations")
    def operations(calc: Calculator = Depends(get_calculator)):
        return {"operations": calc.operations()}

    @app.post("/calculate", response_model=CalculationResponse)
    def calculate(data: CalculationRequest,
                  calc: Calculator = Depends(get_calculator)):
        try:
            calc.calculate(data.operation, data.a, data.b)
        except CalculatorError as error:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, str(error))
        return CalculationResponse.from_record(calc.history[-1])

    @app.get("/history", response_model=list[CalculationResponse])
    def history(calc: Calculator = Depends(get_calculator)):
        return [CalculationResponse.from_record(r) for r in calc.history]

    @app.delete("/history", status_code=status.HTTP_204_NO_CONTENT)
    def clear_history(calc: Calculator = Depends(get_calculator)):
        calc.clear_history()

    return app


app = create_app()
