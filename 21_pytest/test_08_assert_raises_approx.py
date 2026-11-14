import warnings

import pytest

from calculator import average, divide

# LESSON 08: checking ERRORS, FLOATS and WARNINGS.
# RUN:  pytest test_08_assert_raises_approx.py -v


# 1. pytest.raises: the test PASSES only if the code raises that exception
def test_raises():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)


# match= is a regular expression that must be found in the message
def test_raises_message():
    with pytest.raises(ZeroDivisionError, match="cannot divide"):
        divide(1, 0)


# keep the exception to look at it
def test_raises_inspect():
    with pytest.raises(ValueError) as info:
        average([])
    assert "empty" in str(info.value)
    assert info.type is ValueError
# A DIFFERENT exception type is not caught: the test fails with that exception.
# No exception at all: the test fails with "DID NOT RAISE".


# 2. pytest.approx: compare floats (binary floats cannot store 0.1 exactly)
def test_approx():
    assert 0.1 + 0.2 != 0.3                     # True: 0.30000000000000004
    assert 0.1 + 0.2 == pytest.approx(0.3)
    assert [0.1 + 0.2, 1.0] == pytest.approx([0.3, 1.0])    # works on lists and dictionaries
    assert 100.4 == pytest.approx(100, rel=0.01)            # within 1 percent
    assert 5.05 == pytest.approx(5, abs=0.1)                # within 0.1
# EMBEDDED: ADC voltages, filtered sensor values and PID outputs are floats. Always use approx.


# 3. pytest.warns: the code must issue a warning
def old_function():
    warnings.warn("use new_function", DeprecationWarning)
    return 1


def test_warns():
    with pytest.warns(DeprecationWarning, match="new_function"):
        assert old_function() == 1


# 4. Plain assert works for everything. On failure pytest shows a DIFF for lists, dicts, sets and strings:
#       assert [1, 2, 3] == [1, 2, 4]
#       E   At index 2 diff: 3 != 4