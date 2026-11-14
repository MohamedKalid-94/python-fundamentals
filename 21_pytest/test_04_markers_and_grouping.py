import pytest

# LESSON 04: grouping tests with MARKERS and classes.
#
# A marker is a label. Register every marker in pytest.ini (we did: slow, smoke).
# With --strict-markers (also in pytest.ini) an unregistered marker is an ERROR, so typos are caught.
#
#   pytest -m smoke                    4 selected, 2 deselected
#   pytest -m slow                     2 selected, 4 deselected
#   pytest -m "smoke and not slow"     3 selected, 3 deselected
#   pytest -m "smoke or slow"
#   pytest --markers                   list every marker, including yours
#
# A marker on a CLASS applies to every method in it.
# pytestmark = pytest.mark.smoke at the top of a file marks every test in the file.
# Classes group related tests; plain functions are fine too. Use a class when tests share a topic.


@pytest.mark.smoke
def test_start_up():
    assert True


@pytest.mark.slow
def test_big_calculation():
    assert sum(range(1_000_000)) == 499_999_500_000


@pytest.mark.smoke
@pytest.mark.slow
def test_both_markers():
    assert True


class TestUnits:
    def test_one(self):
        assert 1 + 1 == 2


@pytest.mark.smoke
class TestGroupMarked:
    def test_a(self):
        assert True

    def test_b(self):
        assert True