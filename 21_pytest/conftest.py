import pytest

# conftest.py is read by pytest automatically. Fixtures defined here can be used by
# EVERY test file in this folder and below, with no import.

@pytest.fixture
def numbers():
    return [1, 2, 3, 4]


@pytest.fixture(scope="session")
def app_config():
    return {"name": "demo", "debug": False}