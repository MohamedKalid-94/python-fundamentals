![run-lessons](https://github.com/<your-username>/python-fundamentals/actions/workflows/ci.yml/badge.svg)

# Python Fundamentals

A complete, gap-free Python course in 20 modules, written from the point of view of an embedded-systems
engineer moving into AI engineering. Every module has runnable lesson files with the expected output in
comments, an `exercises.py` for practice, a `CONCEPTS.md` summary table, and a short `README.md`.

**Author:** Mohamed Kalid
**Status:** syllabus complete (Modules 01 to 20)

## Modules

| # | Module | Main topics | Status |
|---|--------|-------------|--------|
| 01 | [Python Basics](01_python_basics/) | Syntax, variables, types, casting, literals, input, numbers, booleans, floats | Done |
| 02 | [Operators](02_operators/) | Arithmetic, comparison, assignment, logical, bitwise, membership, identity, walrus, precedence | Done |
| 03 | [Control Flow](03_control_flow/) | `if`, `match`, `for`, `while`, `break`, `continue`, `pass`, nested loops | Done |
| 04 | [Functions & Modules](04_functions_and_modules/) | Arguments, scope, annotations, modules, unpacking, built-ins | Done |
| 05 | [Strings](05_strings/) | Slicing, formatting, escapes, methods | Done |
| 06 | [Lists](06_lists/) | Access, change, comprehension, sort, copy, methods | Done |
| 07 | [Tuples](07_tuples/) | Unpacking, namedtuple | Done |
| 08 | [Sets](08_sets/) | Set operators and methods | Done |
| 09 | [Dictionaries](09_dictionaries/) | Views, nesting, copying | Done |
| 10 | [Arrays](10_arrays/) | The `array` module, buffers, endianness, binary files | Done |
| 11 | [File Handling](11_file_handling/) | Reading, writing, directories, `os`, `os.path`, `pathlib` | Done |
| 12 | [OOP, Part 1](12_oop_part1/) | Classes, constructors, inheritance, polymorphism | Done |
| 13 | [OOP, Part 2](13_oop_part2/) | Abstraction, interfaces, packages, enums, reflection, data classes | Done |
| 14 | [Errors & Exceptions](14_errors_and_exceptions/) | `try`, custom exceptions, logging, assertions, warnings, `pdb` | Done |
| 15 | [Multithreading](15_multithreading/) | Threads, pools, locks, queues, deadlock, cancellation | Done |
| 16 | [Networking](16_networking/) | Sockets, URLs, HTTP, generics | Done |
| 17 | [Miscellaneous A](17_misc_a/) | Date and time, maths, iterators, generators, decorators, recursion, regex | Done |
| 18 | [Miscellaneous B](18_misc_b/) | pip, SQLite, JSON, XML, compression, GUI, CLI, email, `ctypes` | Done |
| 19 | [Advanced A](19_advanced_a/) | ABCs, metaclasses, memory management, higher-order functions | Done |
| 20 | [Advanced B](20_advanced_b/) | Mocking, signals, type hints, `asyncio`, descriptors, DSLs, the data model | Done |

## How to run

```bash
git clone https://github.com/<your-username>/python-fundamentals.git
cd python-fundamentals
python run_all.py                       # run every lesson and report failures
cd 05_strings
python 02_slicing_strings.py            # or run one lesson
```

Requirements: **Python 3.12 recommended** (3.11 is enough for everything except one lesson in Module 16).
Only the standard library is used. The `humanize`, `requests` and similar packages appear in comments only.

## How each module is organised

| File | Purpose |
|------|---------|
| `NN_topic.py` | One lesson per topic, with the expected output in comments |
| `NN_..._examples.py` | Worked examples that combine the topics |
| `exercises.py` | Practice problems for you to solve |
| `CONCEPTS.md` | A one-page summary table of the module |
| `README.md` | The list of files and topics |

## Notes

- Lessons that need the keyboard (`input()`) or a desktop display say so at the top of the file.
- SQL lives in `.sql` files, Python in `.py` files (Module 18).
- Every lesson cleans up the files it creates.

## License

MIT, see [LICENSE](LICENSE).