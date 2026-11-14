import pytest

# LESSON 05: FIXTURES prepare what a test needs. A test asks for one by naming it as a PARAMETER.
# RUN:  pytest test_05_fixtures.py -v          SEE THE ORDER:  pytest test_05_fixtures.py --setup-show
#
# SCOPE: how long a fixture lives
#   function (default)  new for every test        class   once per class
#   module              once per file             session once per run
# yield: code before it is SETUP, code after it is TEARDOWN (it runs even when the test fails).


# 1. The simplest fixture
@pytest.fixture
def user():
    return {"name": "Ann", "roles": ["admin"]}


def test_user_name(user):
    assert user["name"] == "Ann"


# 2. Function scope gives every test a FRESH object: tests do not affect each other
@pytest.fixture
def items():
    return []


def test_items_isolated_a(items):
    items.append(1)
    assert items == [1]


def test_items_isolated_b(items):
    assert items == []                          # a new list, not the one from the test above


# 3. Module scope: created ONCE, shared by every test in the file
created = []


@pytest.fixture(scope="module")
def shared():
    created.append("made")
    return len(created)


def test_shared_a(shared):
    assert shared == 1


def test_shared_b(shared):
    assert shared == 1                          # the same fixture result: it ran only once


# 4. Setup and teardown with yield
@pytest.fixture
def temp_file(tmp_path):                        # a fixture can use other fixtures
    path = tmp_path / "data.txt"
    path.write_text("hello", encoding="utf-8")  # setup
    yield path                                  # the test runs here
    path.unlink()                               # teardown: runs after the test, pass or fail


def test_temp_file(temp_file):
    assert temp_file.read_text(encoding="utf-8") == "hello"


# 5. autouse: applied to every test in the file, without naming it
@pytest.fixture(autouse=True)
def app_mode(monkeypatch):
    monkeypatch.setenv("APP_MODE", "test")


def test_autouse_applied():
    import os
    assert os.environ["APP_MODE"] == "test"


# 6. A factory fixture: returns a FUNCTION, so a test can build several objects
@pytest.fixture
def make_user():
    def _make(name, admin=False):
        return {"name": name, "admin": admin}
    return _make


def test_factory(make_user):
    assert make_user("Bo")["admin"] is False
    assert make_user("Cy", admin=True)["admin"] is True


# 7. Fixtures from conftest.py need no import
def test_conftest_fixture(numbers, app_config):
    assert sum(numbers) == 10
    assert app_config["name"] == "demo"


# RULES
#  - Fixtures are better than a shared global: they are explicit, and cleaned up for you.
#  - Use the smallest scope that is fast enough. Expensive setups (a database, a model) get a bigger scope.
#  - A test must not depend on the ORDER of other tests.
#  - Share fixtures between files by putting them in conftest.py, not by importing them.