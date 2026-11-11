import argparse
import doctest
import json
import textwrap
import xml.etree.ElementTree as ET
import zlib
from collections import defaultdict
from dataclasses import asdict, dataclass
from string import Template


# 1. Settings from four sources: defaults < JSON file < environment < command line
@dataclass
class Settings:
    baud: int = 9600
    port: str = "COM1"
    verbose: bool = False


def load_settings(json_text, env, argv):
    values = asdict(Settings())
    values.update(json.loads(json_text))
    if "APP_PORT" in env:
        values["port"] = env["APP_PORT"]
    parser = argparse.ArgumentParser(prog="app")
    parser.add_argument("--baud", type=int)
    parser.add_argument("--verbose", action="store_true", default=None)
    args = parser.parse_args(argv)
    for key in ("baud", "verbose"):
        if getattr(args, key) is not None:
            values[key] = getattr(args, key)
    return Settings(**values)

print(load_settings('{"baud": 19200}', {"APP_PORT": "COM7"}, ["--verbose"]))
# Settings(baud=19200, port='COM7', verbose=True)
print(load_settings("{}", {}, ["--baud", "115200"]))
# Settings(baud=115200, port='COM1', verbose=False)


# 2. XML in, JSON out: average the sensors of each unit
XML = ('<sensors><sensor id="t1" unit="C">25.3</sensor><sensor id="t2" unit="C">26.1</sensor>'
       '<sensor id="p1" unit="hPa">1013</sensor></sensors>')
groups = defaultdict(list)
for sensor in ET.fromstring(XML):
    groups[sensor.get("unit")].append(float(sensor.text))
summary = {unit: round(sum(values) / len(values), 2) for unit, values in groups.items()}
print(json.dumps(summary, sort_keys=True))      # {"C": 25.7, "hPa": 1013.0}


# 3. A text report from a template
report = Template("Device: $device\nStatus: $status\n\n$notes")
print(report.substitute(
    device="uart0",
    status="OK",
    notes=textwrap.fill("The link was stable for the whole test and no frames were lost.", width=30),
))
# Device: uart0
# Status: OK
#
# The link was stable for the
# whole test and no frames were
# lost.


# 4. Compress a log and verify it with a checksum
log = ("INFO ok\n" * 200).encode()
packed = zlib.compress(log, 9)
print(len(packed) < len(log) / 10, zlib.decompress(packed) == log,
      zlib.crc32(zlib.decompress(packed)) == zlib.crc32(log))       # True True True


# 5. A command-line function that is easy to test (and has a doctest)
def main(argv=None):
    """Add the numbers given on the command line.

    >>> main(["1", "2", "3"])
    6
    """
    parser = argparse.ArgumentParser(prog="adder")
    parser.add_argument("numbers", nargs="+", type=int)
    args = parser.parse_args(argv)
    return sum(args.numbers)

print(main(["10", "20"]))                       # 30
print(doctest.testmod())                        # TestResults(failed=0, attempted=1)