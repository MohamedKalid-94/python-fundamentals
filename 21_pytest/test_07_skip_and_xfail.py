import sys

import pytest

# LESSON 07: SKIP a test that cannot run here, XFAIL a test that is KNOWN to fail.
# RUN:  pytest test_07_skip_and_xfail.py -v -rsx        (-r s = show skip reasons, -r x = show xfail reasons)
#
#   skip    the test is not run. Result: SKIPPED
#   xfail   the test is run and is EXPECTED to fail.   fails -> XFAIL (fine)    passes -> XPASS
#           with strict=True an unexpected pass becomes a real FAILURE
#           (the pytest.ini default is not strict; you can set xfail_strict = true there)


@pytest.mark.skip(reason="not implemented yet")
def test_future_feature():
    assert False


@pytest.mark.skipif(sys.platform == "win32", reason="Unix only")
def test_unix_only():
    import os
    assert os.sep == "/"


@pytest.mark.skipif(sys.version_info < (3, 12), reason="needs Python 3.12")
def test_python_312():
    assert True


@pytest.mark.xfail(reason="known bug: float rounding")
def test_known_bug():
    assert round(2.675, 2) == 2.68              # Python gives 2.67, so this fails: XFAIL


@pytest.mark.xfail(reason="may fail on old systems")
def test_unexpectedly_passes():
    assert True                                 # XPASS


def test_skip_inside():
    pytest.skip("decided at run time")          # skip from inside the test
    assert False                                # never reached


def test_importorskip():
    pytest.importorskip("module_that_does_not_exist")
    assert False                                # skipped: the module is not installed


# WHEN
#   skip     the test needs a platform, a package, a device or a network that is missing
#   xfail    a bug is known and tracked, but you want the test in place (it will tell you when it is fixed)
#   NEVER use skip to hide a test that is broken and forgotten.