Write the questions as # comments and your solutions below each one. Create your own test_*.py files for them, so pytest collects them, and put the code under test in a new module such as mylib.py.

Write mylib.py with is_palindrome(text), clamp(value, low, high) and celsius_to_fahrenheit(c). Test each with at least 4 parametrize cases (including an empty string and a boundary value). Use pytest.approx for the temperature.
Run pytest --collect-only -q, then -k palindrome, then -k "clamp and not low". Write in a comment how many tests each selected.
Write a Stack class with push, pop, peek and __len__. Test it with a fixture that returns an empty stack and another that returns a stack with 3 items. Check that popping from an empty stack raises IndexError with a clear message (match=).
Add the markers fast and slow to the tests in exercise 3. Register them in pytest.ini and run -m "not slow". Then remove the registration and read the --strict-markers error.
Write a fixture with yield that creates a temporary settings file with tmp_path, and a function load_settings(path) that reads key=value lines. Test normal lines, blank lines, a line without = (should raise ValueError), and a missing file.
Write a function count_errors(path) that counts lines containing ERROR in a log file. Test it with tmp_path. Then write a logger_demo() function that logs a warning, and test the message with caplog.
Write a function that reads os.environ["API_KEY"] and raises RuntimeError when it is missing. Test both cases with monkeypatch.
Write read_sensor(uart) that sends b"READ\r\n" and parses a reply such as b"T=25.3\r\n" into a float. Test it with a FakeUart class (a fake with a queue of replies), then with a mocker mock. Compare which test is easier to read.
Write get_user(user_id) that calls weather.fetch_json-style code (your own http_get) and returns the name. Test it with mocker.patch, check the URL, and use side_effect to simulate a timeout. Why does patching "requests.get" fail if your code did from requests import get?
Write an async function fetch_all(urls, fetch) that runs the calls with asyncio.gather. Test it with pytest-asyncio and an AsyncMock, including a failing call.
Make one test skipif on a missing package, one xfail(strict=True) for a known bug, and one skip. Run with -rsx and explain each line of the summary.
Use conftest.py to create a session fixture that builds a big list once (for example 100,000 numbers), and use it from two different test files. Prove with --setup-show that it was created once.
Run the suite with --junitxml=report.xml, open the file, and find a skipped test and its reason.
Install pytest-cov, measure the coverage of mylib.py, find a line that is not covered, and write a test for it until you reach 100 percent.
Install pytest-xdist. Add time.sleep(0.2) to 20 tests, then compare pytest with pytest -n 4. Explain the result.
Predict first, then run, and explain each result in a comment:
python
import pytest

@pytest.fixture
def box():
    print("setup")
    yield []
    print("teardown")

@pytest.mark.parametrize("n", [1, 2])
def test_a(box, n):
    box.append(n)
    assert box == [n]

@pytest.mark.xfail(strict=True)
def test_b():
    assert 1 + 1 == 2

def test_c():
    assert 0.1 + 0.2 == 0.3

Which tests pass, fail or xfail? What happens to test_b, and why? Run with -s to see the order of setup and teardown.