import io
import os
import sys
import time
import unittest
from unittest.mock import MagicMock, Mock, PropertyMock, create_autospec, mock_open, patch

this = sys.modules[__name__]            # this file as a module (so we can patch its functions)

# A TEST DOUBLE replaces a real part of the system during a test, so the test is
# fast, repeatable, and does not touch the network, the clock, the disk or hardware.
#
#   dummy   fills a parameter, never used        stub   returns canned answers
#   fake    a working simple version (in-memory)  mock   records calls so you can CHECK them
#   spy     wraps the real thing and records calls

# 1. Mock: a stand-in that accepts any call and remembers it
m = Mock(return_value=5)
print(m(1, 2), m.call_count, m.call_args, m.called)     # 5 1 call(1, 2) True
m.assert_called_once_with(1, 2)
m(3)
print(m.call_args_list)                         # [call(1, 2), call(3)]
m.assert_any_call(3)
print(type(m.anything).__name__, type(m.anything(5)).__name__)      # Mock Mock    attributes appear on demand

n = Mock()
n.assert_not_called()
n(1)
try:
    n.assert_called_with(2)
except AssertionError:
    print("AssertionError")                     # the mock was NOT called with 2

# MagicMock also supports the "magic" methods (len(), [], str() ...)
mm = MagicMock()
mm.__len__.return_value = 3
mm.__getitem__.return_value = "x"
mm.__str__.return_value = "magic"
print(len(mm), mm[0], str(mm))                  # 3 x magic

# 2. side_effect: a sequence of results, an exception, or a function
seq = Mock(side_effect=[1, 2, ValueError("boom")])
print(seq(), seq())                             # 1 2
try:
    seq()
except ValueError as e:
    print(e)                                    # boom
print(Mock(side_effect=lambda x: x * 2)(4))     # 8

# 3. DEPENDENCY INJECTION: pass the dependency in, so a test can pass a stub
def get_temperature(city, fetch):
    data = fetch(f"https://api.example.com/weather?city={city}")
    return round(data["main"]["temp"] - 273.15, 1)

stub = Mock(return_value={"main": {"temp": 298.15}})
print(get_temperature("Pune", stub))            # 25.0
stub.assert_called_once_with("https://api.example.com/weather?city=Pune")

# 4. patch: replace something that is NOT injected, for the length of a "with" block
def fetch_json(url):
    raise RuntimeError("real network call!")

def current_temp(city):
    data = fetch_json(f"https://api.example.com/weather?city={city}")
    return round(data["main"]["temp"] - 273.15, 1)

with patch.object(this, "fetch_json", return_value={"main": {"temp": 300.15}}) as fake:
    print(current_temp("Pune"))                 # 27.0
    print(fake.call_args)                       # call('https://api.example.com/weather?city=Pune')
try:
    current_temp("Pune")                        # the patch is gone: the real function runs again
except RuntimeError as e:
    print(e)                                    # real network call!

@patch.object(this, "fetch_json", return_value={"main": {"temp": 273.15}})
def check(fake_fetch):                          # as a decorator, the mock arrives as an argument
    return current_temp("X"), fake_fetch.call_count

print(check())                                  # (0.0, 1)
# RULE: patch the name WHERE IT IS LOOKED UP (file 02 shows why).

# 5. spec: a mock that copies the shape of a real class
class Service:
    def get(self, ident):
        return ident

loose = Mock(spec=Service)
loose.get(1)
try:
    loose.missing()
except AttributeError:
    print("AttributeError")                     # Service has no method "missing"

strict = create_autospec(Service, instance=True)    # also checks the ARGUMENTS
strict.get(1)
try:
    strict.get()
except TypeError:
    print("TypeError")                          # get() needs one argument

# 6. patch.dict: change a dictionary (environment variables, settings) for a while
with patch.dict(os.environ, {"DEMO_APP_MODE": "test"}):
    print(os.environ["DEMO_APP_MODE"])          # test
print("DEMO_APP_MODE" in os.environ)            # False

# 7. mock_open: fake a file
def read_settings(path):
    with open(path, encoding="utf-8") as f:
        return dict(line.split("=") for line in f.read().splitlines())

with patch("builtins.open", mock_open(read_data="a=1\nb=2")):
    print(read_settings("anything.cfg"))        # {'a': '1', 'b': '2'}

# 8. Time: freeze it, or skip waiting
with patch("time.time", return_value=1000.0):
    print(time.time())                          # 1000.0
print(time.time() > 1000.0)                     # True
with patch("time.sleep") as fake_sleep:
    time.sleep(10)                              # returns at once
    print(fake_sleep.call_args)                 # call(10)

# 9. PropertyMock: fake a property (a sensor that needs hardware)
class Device:
    @property
    def temp(self):
        raise RuntimeError("no hardware")

with patch.object(Device, "temp", new_callable=PropertyMock, return_value=36.6):
    print(Device().temp)                        # 36.6

# 10. Spy: call the real thing AND record the call
spy = Mock(wraps=len)
print(spy("abc"))                               # 3
spy.assert_called_once_with("abc")

# 11. A hand-written FAKE (often better than a mock for hardware and databases)
class FakeUart:
    def __init__(self):
        self.sent = []

    def write(self, data):
        self.sent.append(data)
        return len(data)

def send_command(uart, command):
    return uart.write(command.encode() + b"\r\n")

fake_uart = FakeUart()
print(send_command(fake_uart, "AT"), fake_uart.sent)    # 4 [b'AT\r\n']

# 12. Mocks inside a real test class
class WeatherTests(unittest.TestCase):
    def test_converts_kelvin(self):
        with patch.object(this, "fetch_json", return_value={"main": {"temp": 300.15}}):
            self.assertEqual(current_temp("Pune"), 27.0)

    def test_network_error_propagates(self):
        with patch.object(this, "fetch_json", side_effect=ConnectionError("down")):
            with self.assertRaises(ConnectionError):
                current_temp("Pune")

suite = unittest.defaultTestLoader.loadTestsFromTestCase(WeatherTests)
result = unittest.TextTestRunner(stream=io.StringIO()).run(suite)
print(result.testsRun, result.wasSuccessful())  # 2 True

# GUIDELINES
#  - Replace the BOUNDARIES (network, clock, disk, random numbers, hardware), not your own logic.
#  - Prefer injecting dependencies; use patch when you cannot.
#  - Prefer a fake to a mock when a simple working version is easy to write.
#  - Test what the code DOES (results), not how it does it (the exact calls), or tests break on every refactoring.
#  - Use spec / autospec so a mock cannot accept calls the real object would reject.
# pytest users: the "monkeypatch" fixture and the pytest-mock plugin ("mocker") wrap these same tools.
# EMBEDDED: a FakeUart / FakeGpio lets you test firmware logic on a PC, with no board.