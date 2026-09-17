Поздняков Никита Сергеевич, группа 221141, вариант 4, лабораторная №8

# Лабораторная работа №8. Экосистемы Python

Вариант 4: средней сложности — 4, 6, 10; повышенной — 5, 9.

| № | Задание | Где реализовано |
|---|---------|-----------------|
| Средн. 4 | TDD для калькулятора | `tests/test_calculator.py` → `src/calc_tdd/model.py` |
| Средн. 6 | Настроить flake8 | `.flake8`, `.github/workflows/ci.yml` |
| Средн. 10 | Описать архитектуру MVC | `docs/MVC.md`, код разделён на model / view / controller |
| Повыш. 5 | TDD к API | `tests/test_api.py` → `src/calc_tdd/controller.py` |
| Повыш. 9 | Пакет на TestPyPI | `pyproject.toml`, инструкция `docs/PUBLISHING.md` |

## Установка

```bash
python -m venv venv
venv\Scripts\activate
pip install -e ".[api,dev]"
```

## Использование

Командная строка (entry point из `pyproject.toml`):

```bash
calc-tdd 2 + 3
calc-tdd 2 ^ 10
calc-tdd sqrt 16
```

Веб-API:

```bash
uvicorn calc_tdd.controller:app --reload
```

Swagger: http://127.0.0.1:8000/docs

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/health` | проверка работы сервиса |
| GET | `/operations` | список поддерживаемых операций |
| POST | `/calculate` | `{"operation": "add", "a": 2, "b": 3}` → результат |
| GET | `/history` | история вычислений |
| DELETE | `/history` | очистить историю |

Как библиотека:

```python
from calc_tdd import Calculator

calc = Calculator()
calc.calculate("divide", 10, 4)  # 2.5
```

## Проверки

```bash
flake8
pytest -v
```

Те же команды запускаются в GitHub Actions при каждом push
(`.github/workflows/ci.yml`).

## TDD

Работа велась циклами «красный → зелёный → рефакторинг», это видно по
истории коммитов: сначала коммит `test:` с падающими тестами, затем
`feat:` с минимальной реализацией, затем `refactor:`. Подробнее —
`docs/TDD.md`.

## Публикация на TestPyPI

Пакет: `calc-tdd-pozdnyakov`. Сборка и загрузка описаны в
`docs/PUBLISHING.md`.

Ссылка на опубликованный пакет: _добавить после публикации_

```bash
pip install -i https://test.pypi.org/simple/ calc-tdd-pozdnyakov
```
