import os
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).parent
LESSONS = sorted(HERE.glob("lesson_*.py"))
MARKER = "# EXPECTED OUTPUT"

# Every lesson file ends with a block of comment lines that holds the output it must print.
# This test runs each lesson in a separate process and compares what it printed with that block.
# ("#" alone stands for an empty line.)


def expected_output(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    block = lines[lines.index(MARKER) + 1:]
    return [line[2:].rstrip() if line.startswith("# ") else "" for line in block]


def run_lesson(path):
    env = {**os.environ, "PYTHONUTF8": "1", "MPLBACKEND": "Agg"}
    return subprocess.run(
        [sys.executable, path.name], cwd=HERE, env=env,
        capture_output=True, text=True, encoding="utf-8",
    )


def test_all_lessons_were_found():
    assert len(LESSONS) == 13


@pytest.mark.parametrize("path", LESSONS, ids=lambda p: p.stem)
def test_lesson_prints_what_its_comment_says(path):
    result = run_lesson(path)
    assert result.returncode == 0, result.stderr
    actual = [line.rstrip() for line in result.stdout.splitlines()]
    assert actual == expected_output(path)