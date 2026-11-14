# Module 21: pytest, Concepts Summary

| # | Topic | Concept | Remember |
|---|---|---|---|
| 01 | Setup | Install | `python -m venv .venv`, activate it, `pip install -r requirements.txt`, `pytest --version` |
| 01 | Discovery | Rules | Files `test_*.py` or `*_test.py`; functions `test*`; classes `Test*` without `__init__` |
| 01 | Discovery | Node id | `file::Class::function`; list tests with `--collect-only -q` |
| 02 | Basic test | Plain `assert` | No `self.assertEqual`; pytest shows the values when it fails |
| 02 | Basic test | Structure | Arrange, act, assert; one behaviour per test; the name says which |
| 03 | Running | Where | `pytest`, a file, a folder, a node id, `python -m pytest` |
| 03 | Selecting | `-k` | Substring of the function, class or file name; `and`, `or`, `not` |
| 03 | Selecting | Options | `-v`, `-q`, `-s`, `--tb=short`, `--lf`, `--ff`, `--durations=3`, `--collect-only` |
| 04 | Markers | Grouping | `@pytest.mark.smoke`; `-m "smoke and not slow"`; a marker on a class marks all its methods |
| 04 | Markers | Register | List them in `pytest.ini`; `--strict-markers` catches typos; `pytest --markers` |
| 05 | Fixtures | Use | `@pytest.fixture`; a test asks for it by parameter name |
| 05 | Fixtures | Scope | `function` (default), `class`, `module`, `session`; smallest scope that is fast enough |
| 05 | Fixtures | Teardown | Code after `yield` runs even when the test fails |
| 05 | Fixtures | Kinds | `autouse=True`, factory fixtures (return a function), fixtures that use fixtures |
| 05 | conftest.py | Sharing | Fixtures there are available to all tests in the folder, with no import |
| 06 | Parametrize | Basic | `@pytest.mark.parametrize("a, b, expected", [...])`; every case is its own test |
| 06 | Parametrize | Ids | `pytest.param(..., id="name")`; stacked decorators multiply; `fixture(params=[...])` |
| 07 | Skip | Forms | `skip`, `skipif(condition, reason=...)`, `pytest.skip(...)`, `pytest.importorskip("module")` |
| 07 | Xfail | Meaning | Expected to fail: XFAIL is fine, XPASS is a surprise; `strict=True` makes XPASS a failure |
| 07 | Reports | `-rsx` | Shows skip and xfail reasons |
| 08 | Errors | `pytest.raises` | `match="regex"`; `as info` gives `info.value` and `info.type`; "DID NOT RAISE" fails |
| 08 | Floats | `pytest.approx` | `rel=`, `abs=`; works on lists and dictionaries |
| 08 | Warnings | `pytest.warns` | The code must issue the warning |
| 09 | Built-in fixtures | `tmp_path` | A fresh temporary folder (a `Path`) per test |
| 09 | Built-in fixtures | `monkeypatch` | `setenv`, `delenv`, `setattr`, `chdir`; undone after the test |
| 09 | Built-in fixtures | `capsys`, `caplog` | Check printed output and log messages |
| 10 | Mocking | `mocker` | `patch`, `side_effect`, `spy`, `assert_called_once_with`; undone automatically |
| 10 | Mocking | Rule | Patch the name where it is looked up; replace boundaries, not your own logic |
| 10 | Mocking | Fakes | A small hand-written class (a fake UART) is often clearer than a mock |
| 11 | Async | Tests | `@pytest.mark.asyncio` on an `async def` test |
| 11 | Async | Fixtures | `@pytest_asyncio.fixture` for async fixtures; `AsyncMock` for coroutines |
| 12 | Stopping | Options | `-x`, `--maxfail=N`, `--lf`, `--ff`, `--sw` |
| 12 | Parallel | xdist | `pytest -n auto`; tests must be independent; session fixtures run per worker |
| 12 | Reports | XML | `--junitxml=report.xml` for CI tools |
| 12 | Coverage | pytest-cov | `--cov=module --cov-report=term-missing`, `html`, `--cov-fail-under=N` |
| 12 | Debugging | Options | `-vv`, `-l`, `--tb=short`, `--pdb`, `-s` |