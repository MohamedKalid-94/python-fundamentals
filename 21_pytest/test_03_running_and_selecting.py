# LESSON 03: file execution, subsets of the suite, and substring matching with -k.
#
# FILES AND FOLDERS
#   pytest                                        everything under testpaths (see pytest.ini)
#   pytest test_03_running_and_selecting.py       one file
#   pytest .                                      one folder, recursively
#   python -m pytest                              the same, and adds the current folder to sys.path
#
# NODE IDS: file::class::function
#   pytest test_03_running_and_selecting.py::test_logout
#   pytest test_03_running_and_selecting.py::TestCart
#   pytest test_03_running_and_selecting.py::TestCart::test_add
#
# -k "expression": run the tests whose NAME contains a substring (not case sensitive).
# It looks at the function name, the class name, and the file name.
#   pytest -k login                  test_login_valid, test_login_invalid         (2 selected, 4 deselected)
#   pytest -k "login and not invalid" test_login_valid                             (1 selected, 5 deselected)
#   pytest -k "login or logout"      3 tests
#   pytest -k cart                   test_add_item_to_cart AND both TestCart tests (3 selected, 3 deselected)
#   pytest -k "TestCart and add"     TestCart::test_add only
#
# OTHER USEFUL OPTIONS
#   -v / -q / -vv     more / less / even more detail        -s    show print() output
#   -x                stop at the first failure              --maxfail=2   stop after 2 failures
#   --lf              run only the tests that failed last time      --ff   failed ones first
#   --tb=short        shorter failure messages               --durations=3  the 3 slowest tests
#   --collect-only    list the tests, do not run them
#   -m smoke          run by marker (lesson 04)


def test_login_valid():
    assert "ann".isalpha()


def test_login_invalid():
    assert not "a1".isalpha()


def test_logout():
    assert True


def test_add_item_to_cart():
    cart = []
    cart.append("pen")
    assert cart == ["pen"]


class TestCart:
    def test_empty(self):
        assert [] == []

    def test_add(self):
        items = ["pen"]
        items.append("ink")
        assert len(items) == 2