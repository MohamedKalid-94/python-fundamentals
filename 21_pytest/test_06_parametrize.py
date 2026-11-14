import pytest

from calculator import add, average, is_even

# LESSON 06: PARAMETRIZE runs ONE test function with MANY inputs. Each case is a separate test.
# RUN:  pytest test_06_parametrize.py -v


# 1. The basic form: names, then a list of tuples
@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
    (2.5, 0.5, 3.0),
])
def test_add_cases(a, b, expected):
    assert add(a, b) == expected
# Test ids:  test_add_cases[1-2-3]   test_add_cases[0-0-0]   test_add_cases[-1-1-0]   test_add_cases[2.5-0.5-3.0]


# 2. pytest.param gives a case its own id (and can carry marks)
@pytest.mark.parametrize("n, even", [
    (0, True),
    (1, False),
    (2, True),
    (-3, False),
    pytest.param(10 ** 12, True, id="huge"),
])
def test_is_even(n, even):
    assert is_even(n) is even


# 3. Stacked decorators: every combination (2 x 2 = 4 tests)
@pytest.mark.parametrize("x", [1, 2])
@pytest.mark.parametrize("y", [10, 20])
def test_grid(x, y):
    assert x * y in (10, 20, 40)
# ids: test_grid[10-1]  test_grid[10-2]  test_grid[20-1]  test_grid[20-2]   (the lower decorator comes first)


# 4. A parametrized FIXTURE: every test that uses it runs once per value
@pytest.fixture(params=["sqlite", "memory"])
def backend(request):
    return request.param


def test_backend(backend):
    assert backend in ("sqlite", "memory")


# 5. Expecting an error for several bad inputs
@pytest.mark.parametrize("bad", [[], ()])
def test_average_empty(bad):
    with pytest.raises(ValueError):
        average(bad)


# TIPS
#  - Run one case:  pytest "test_06_parametrize.py::test_is_even[huge]"      (quote the brackets in PowerShell)
#  - -k works on ids:  pytest -k "huge"
#  - Keep the data in the decorator, the logic in the function. A table of cases reads like a spec.