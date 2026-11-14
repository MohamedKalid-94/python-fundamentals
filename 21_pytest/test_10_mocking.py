import pytest

import calculator
import weather

# LESSON 10: MOCKING in pytest. Module 20 taught unittest.mock; pytest-mock wraps it in a fixture
# called "mocker" that UNDOES every patch at the end of the test (no "with" blocks needed).
# RUN:  pytest test_10_mocking.py -v
#
# RULE (same as Module 20): patch the name WHERE IT IS LOOKED UP.
# weather.current_temp() calls fetch_json inside the weather module, so we patch "weather.fetch_json".


# 1. mocker.patch with a canned answer, and a check of the call
def test_with_mocker(mocker):
    fake = mocker.patch("weather.fetch_json", return_value={"main": {"temp": 300.15}})
    assert weather.current_temp("Pune") == 27.0
    fake.assert_called_once_with("https://api.example.com/weather?city=Pune")


# 2. side_effect: make the dependency fail
def test_error_propagates(mocker):
    mocker.patch("weather.fetch_json", side_effect=ConnectionError("down"))
    with pytest.raises(ConnectionError):
        weather.current_temp("Pune")


# 3. The same job with monkeypatch (no extra plugin needed, but no call recording)
def test_with_monkeypatch(monkeypatch):
    monkeypatch.setattr(weather, "fetch_json", lambda url: {"main": {"temp": 273.15}})
    assert weather.current_temp("X") == 0.0


# 4. A spy: the real function runs AND the call is recorded
def test_spy(mocker):
    spy = mocker.spy(calculator, "add")
    assert calculator.add(2, 3) == 5
    spy.assert_called_once_with(2, 3)


# 5. A hand-written FAKE: often clearer than a mock for hardware
class FakeUart:
    def __init__(self):
        self.sent = []

    def write(self, data):
        self.sent.append(data)
        return len(data)


def send_command(uart, command):
    return uart.write(command.encode() + b"\r\n")


def test_fake_uart():
    uart = FakeUart()
    assert send_command(uart, "AT") == 4
    assert uart.sent == [b"AT\r\n"]


# GUIDELINES (same as Module 20)
#  - Replace the BOUNDARIES: network, clock, disk, random numbers, hardware. Do not mock your own logic.
#  - Test what the code DOES (results), not every internal call, or tests break on each refactoring.
#  - Prefer a fake when it is easy to write. Use autospec (mocker.patch(..., autospec=True)) to keep signatures honest.