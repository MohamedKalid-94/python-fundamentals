from calculator import add

# This file FAILS ON PURPOSE, to show what failures and the stop options look like.
# It is not named test_*.py, so a plain "pytest" skips it. Run it by name, from 21_pytest/:
#
#   pytest demos_that_fail/demo_failures.py
#   pytest demos_that_fail/demo_failures.py -x
#   pytest demos_that_fail/demo_failures.py --maxfail=2
#
# The failure report looks like this (shortened):
#
#   def test_fail_a():
#   >       assert add(2, 2) == 5
#   E       assert 4 == 5
#   E        +  where 4 = add(2, 2)
#
#   FAILED demos_that_fail/demo_failures.py::test_fail_a - assert 4 == 5
#   FAILED demos_that_fail/demo_failures.py::test_fail_b - assert [1, 2, 3] == [1, 2, 4]
#   FAILED demos_that_fail/demo_failures.py::test_fail_c - AssertionError: assert 'python' == 'pyhton'
#   ========== 3 failed, 3 passed in 0.03s ==========


def test_pass_1():
    assert True


def test_fail_a():
    assert add(2, 2) == 5


def test_pass_2():
    assert True


def test_fail_b():
    assert [1, 2, 3] == [1, 2, 4]


def test_fail_c():
    assert "python" == "pyhton"


def test_pass_3():
    assert True