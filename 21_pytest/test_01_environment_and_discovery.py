# LESSON 01: how pytest FINDS tests.
#
# RUN:      pytest test_01_environment_and_discovery.py -v
# LIST:     pytest test_01_environment_and_discovery.py --collect-only -q
#
# DISCOVERY RULES (the defaults)
#   files       test_*.py  or  *_test.py
#   functions   names that start with  test
#   classes     names that start with  Test  and have no __init__ method
#   methods     names that start with  test   (inside a Test class)
# Anything else is ignored: helper functions, other classes, other file names.
# A test PASSES when it finishes without an exception. A failing "assert" is an exception.
# pytest starts from the folder (or file) you give it, and goes down into sub-folders.


def test_function_is_collected():
    assert True


def helper_not_a_test():
    return 42                                   # no "test" prefix: pytest ignores it


def check_not_collected():
    assert False                                # never runs: the name does not start with "test"


class TestGroup:
    def test_method_is_collected(self):
        assert helper_not_a_test() == 42

    def helper_inside_class(self):              # ignored
        return 1


class NotCollected:
    def test_never_runs(self):                  # the class name does not start with "Test"
        assert False