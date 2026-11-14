from calculator import add, average, divide, is_even

# LESSON 02: a basic test is a function with a plain "assert". No class, no self.assertEqual.
# RUN:  pytest test_02_basic_tests.py -v
#
# On a failure pytest REWRITES the assert and shows the values:
#       def test_add_wrong():
#   >       assert add(2, 2) == 5
#   E       assert 4 == 5
#   E        +  where 4 = add(2, 2)
#
# ARRANGE - ACT - ASSERT: set up the data, call the code, check the result.
# One test checks one behaviour, and its name says which (test_divide_by_zero_raises ...).


def test_add():
    assert add(2, 3) == 5


def test_add_strings():
    assert add("a", "b") == "ab"                # add() works for any type that supports +


def test_divide():
    assert divide(10, 4) == 2.5


def test_is_even():
    assert is_even(4)                           # truthy values pass
    assert not is_even(7)


def test_average():
    assert average([1, 2, 3, 4]) == 2.5