import logging
import os
from pathlib import Path

# LESSON 09: the fixtures that come WITH pytest.
# RUN:  pytest test_09_builtin_fixtures.py -v        List them all:  pytest --fixtures
#
#   tmp_path       a new, empty temporary folder (a pathlib.Path) for each test
#   monkeypatch    change an attribute, a dictionary item, an environment variable or the working folder;
#                  everything is UNDONE after the test
#   capsys         capture what the code print()s
#   caplog         capture what the code logs
#   request        information about the running test (used inside fixtures)


# 1. tmp_path: real files, no cleanup code, no clash between tests
def test_tmp_path(tmp_path):
    file = tmp_path / "notes.txt"
    file.write_text("hello\nworld\n", encoding="utf-8")
    assert file.read_text(encoding="utf-8").splitlines() == ["hello", "world"]
    assert file.parent == tmp_path


# 2. monkeypatch: environment variables
def test_monkeypatch_env(monkeypatch):
    monkeypatch.setenv("APP_MODE", "prod")
    assert os.environ["APP_MODE"] == "prod"
    monkeypatch.delenv("APP_MODE")
    assert "APP_MODE" not in os.environ


# 3. monkeypatch: replace a function, and see that it is put back afterwards
def test_monkeypatch_attr(monkeypatch):
    import calculator
    monkeypatch.setattr(calculator, "add", lambda a, b: 99)
    assert calculator.add(1, 1) == 99


def test_attr_restored():
    import calculator
    assert calculator.add(1, 1) == 2            # the real function is back


# 4. monkeypatch: the working folder
def test_chdir(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    Path("local.txt").write_text("x", encoding="utf-8")
    assert (tmp_path / "local.txt").exists()


# 5. capsys: check printed output
def greet(name):
    print(f"Hello {name}")


def test_capsys(capsys):
    greet("Ann")
    out, err = capsys.readouterr()
    assert out == "Hello Ann\n"
    assert err == ""


# 6. caplog: check log messages
def work():
    logging.getLogger("app").warning("disk almost full")


def test_caplog(caplog):
    with caplog.at_level(logging.WARNING, logger="app"):
        work()
    assert "disk almost full" in caplog.text
    assert caplog.records[0].levelname == "WARNING"