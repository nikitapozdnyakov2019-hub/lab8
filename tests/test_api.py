import pytest
from fastapi.testclient import TestClient

from calc_tdd.controller import create_app


@pytest.fixture()
def client():
    return TestClient(create_app())


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_operations(client):
    operations = client.get("/operations").json()["operations"]
    assert "add" in operations and "sqrt" in operations


def test_calculate_binary(client):
    response = client.post("/calculate",
                           json={"operation": "multiply", "a": 6, "b": 7})
    assert response.status_code == 200
    assert response.json() == {
        "operation": "multiply",
        "a": 6,
        "b": 7,
        "result": 42,
        "expression": "6 * 7 = 42",
    }


def test_calculate_unary(client):
    body = client.post("/calculate",
                       json={"operation": "sqrt", "a": 2.25}).json()
    assert body["result"] == 1.5
    assert body["expression"] == "sqrt(2.25) = 1.5"


def test_domain_error_returns_400(client):
    response = client.post("/calculate",
                           json={"operation": "divide", "a": 1, "b": 0})
    assert response.status_code == 400
    assert response.json()["detail"] == "деление на ноль"


@pytest.mark.parametrize("payload", [
    {"operation": "modulo", "a": 1, "b": 2},
    {"operation": "add", "a": "два", "b": 2},
    {"a": 1, "b": 2},
])
def test_invalid_payload_returns_422(client, payload):
    assert client.post("/calculate", json=payload).status_code == 422


def test_history_flow(client):
    assert client.get("/history").json() == []
    client.post("/calculate", json={"operation": "add", "a": 1, "b": 1})
    client.post("/calculate", json={"operation": "divide", "a": 1, "b": 0})
    client.post("/calculate", json={"operation": "negate", "a": 5})

    history = client.get("/history").json()
    assert [h["expression"] for h in history] == ["1 + 1 = 2",
                                                  "negate(5) = -5"]

    assert client.delete("/history").status_code == 204
    assert client.get("/history").json() == []


def test_apps_do_not_share_state():
    first = TestClient(create_app())
    second = TestClient(create_app())
    first.post("/calculate", json={"operation": "add", "a": 1, "b": 1})
    assert second.get("/history").json() == []
