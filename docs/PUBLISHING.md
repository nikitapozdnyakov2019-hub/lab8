# Публикация пакета на TestPyPI

1. Зарегистрироваться на https://test.pypi.org/account/register/ и
   подтвердить почту.
2. Account settings → API tokens → Add API token (scope: entire account).
   Токен показывается один раз, **никуда его не коммитить**.
3. Проверить, что имя `calc-tdd-pozdnyakov` свободно:
   https://test.pypi.org/project/calc-tdd-pozdnyakov/ должна вернуть 404.
   Если занято — поменять `name` в `pyproject.toml`.
4. Собрать и проверить пакет:

   ```bash
   pip install build twine
   python -m build
   twine check dist/*
   ```

5. Загрузить (логин `__token__`, пароль — токен):

   ```bash
   twine upload --repository testpypi dist/*
   ```

6. Проверить установку в чистом окружении:

   ```bash
   python -m venv check
   check\Scripts\activate
   pip install -i https://test.pypi.org/simple/ calc-tdd-pozdnyakov
   calc-tdd 2 + 3
   ```

7. Добавить ссылку на страницу пакета в `README.md`, поставить тег:

   ```bash
   git tag -a v0.1.0 -m "Release 0.1.0 (TestPyPI)"
   git push --tags
   ```

Повторно загрузить ту же версию нельзя — для исправлений увеличивать
`version` в `pyproject.toml` и `src/calc_tdd/__init__.py`.
