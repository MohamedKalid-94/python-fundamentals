# Lesson 12: reports, parallel runs, coverage, stopping and debugging

## XML report (for CI tools such as Jenkins and GitHub test summaries)

```powershell
pytest --junitxml=report.xml
```

The file starts like this (shortened):

```xml
<?xml version="1.0" encoding="utf-8"?><testsuites name="pytest tests"><testsuite name="pytest"
errors="0" failures="0" skipped="3" tests="74" time="0.4"> <testcase classname="test_02_basic_tests"
name="test_add" time="0.001" /> ...
```

Every test is one `<testcase>`; a failure holds a `<failure message="...">` inside it.

## Stop early

| Option | Meaning |
|---|---|
| `-x` | stop at the first failure |
| `--maxfail=3` | stop after 3 failures |
| `--lf` | run only the tests that failed last time |
| `--ff` | run the failed ones first, then the rest |
| `--sw` | stepwise: stop at a failure, continue from it next time |

Try them on the demo file, which fails on purpose:

```powershell
pytest demos_that_fail/demo_failures.py                 # 3 failed, 3 passed
pytest demos_that_fail/demo_failures.py -x              # 1 failed, 1 passed   (stopping after 1 failures)
pytest demos_that_fail/demo_failures.py --maxfail=2     # 2 failed, 2 passed
```

## Parallel runs (pytest-xdist)

```powershell
pytest -n auto          # one worker per CPU core
pytest -n 4             # exactly 4 workers
pytest -n 0             # turn it off again
```

- Tests must be independent: no shared files with fixed names (use `tmp_path`), no order assumptions.
- A `session` fixture runs once per worker, not once per run.
- The output order changes between runs; the results do not.
- With a suite of 74 tiny tests it is slower than a plain run, because starting workers takes time. It pays off for slow suites.

## Coverage (pytest-cov)

```powershell
pytest --cov=calculator --cov-report=term-missing
pytest --cov=calculator --cov-report=html          # open htmlcov\index.html
pytest --cov=calculator --cov-fail-under=90        # fail the run below 90 percent
```

Expected table:

```
Name            Stmts   Miss  Cover   Missing
-----------------------------------------------
calculator.py      12      0   100%
```

100 percent means every line RAN. It does not mean every behaviour is checked.

## Debugging a failing test

| Option | Meaning |
|---|---|
| `-vv` | full diffs of long values |
| `-l` | show local variables in the failure |
| `--tb=short` / `--tb=no` | shorter or no tracebacks |
| `--pdb` | open the debugger at the failure (Module 14) |
| `-s` | show `print()` output while the tests run |
| `-p no:cacheprovider` | do not write `.pytest_cache` |