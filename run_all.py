"""Run every lesson file of every module and report which ones fail.

    python run_all.py                       run everything
    python run_all.py --only 05_strings     run one module folder
    python run_all.py --timeout 120         change the time limit per file (seconds)
"""
import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Files that need a person at the keyboard
SKIP = {
    "01_python_basics/09_user_input.py": "needs keyboard input",
    "03_control_flow/05_conditional_user_inputs.py": "needs keyboard input",
    "03_control_flow/09_while_loops.py": "needs keyboard input",
}
if sys.version_info < (3, 12):
    SKIP["16_networking/05_generics_python312.py"] = "needs Python 3.12 or newer"


def lesson_files(only=None):
    for module in sorted(ROOT.glob("[0-9][0-9]_*")):
        if not module.is_dir() or (only and module.name != only):
            continue
        for path in sorted(module.glob("[0-9][0-9]_*.py")):     # lesson files only, not exercises.py
            yield module, path


def run(module, path, timeout):
    env = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
    start = time.perf_counter()
    try:
        result = subprocess.run(
            [sys.executable, path.name], cwd=module, env=env, stdin=subprocess.DEVNULL,
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return "TIMEOUT", time.perf_counter() - start, f"more than {timeout} s"
    elapsed = time.perf_counter() - start
    if result.returncode == 0:
        return "ok", elapsed, ""
    lines = result.stderr.strip().splitlines()
    return "FAIL", elapsed, lines[-1] if lines else f"exit code {result.returncode}"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--only", help="run only this module folder, e.g. 05_strings")
    parser.add_argument("--timeout", type=int, default=60)
    args = parser.parse_args()

    counts = {"ok": 0, "FAIL": 0, "TIMEOUT": 0, "skipped": 0}
    problems = []
    for module, path in lesson_files(args.only):
        key = f"{module.name}/{path.name}"
        if key in SKIP:
            counts["skipped"] += 1
            print(f"{key:<62} skipped ({SKIP[key]})")
            continue
        status, seconds, detail = run(module, path, args.timeout)
        counts[status] += 1
        print(f"{key:<62} {status:<8} {seconds:5.1f}s")
        if status != "ok":
            problems.append((key, status, detail))

    print()
    print("  ".join(f"{name}: {number}" for name, number in counts.items()))
    for key, status, detail in problems:
        print(f"  {status}  {key}\n        {detail}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())