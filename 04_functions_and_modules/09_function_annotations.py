# Annotations describe the expected types. Python does NOT enforce them.

def add(a: int, b: int) -> int:
    return a + b

print(add(2, 3))                # 5
print(add("a", "b"))            # ab    (no error, hints are not checks)
print(add.__annotations__)
# {'a': <class 'int'>, 'b': <class 'int'>, 'return': <class 'int'>}

# With defaults
def repeat(text: str, times: int = 2) -> str:
    return text * times

print(repeat("ab"))             # abab

# Collections and "or None" (Python 3.10+ syntax)
def average(values: list[float]) -> float:
    return sum(values) / len(values)

print(average([1.0, 2.0, 6.0])) # 3.0

def find(items: list[str], target: str) -> int | None:
    return items.index(target) if target in items else None

print(find(["a", "b"], "b"))    # 1
print(find(["a", "b"], "z"))    # None

# No return value
def log(message: str) -> None:
    print(message)

log("saved")                    # saved

# *args and **kwargs
def total(*nums: int) -> int:
    return sum(nums)

def tag(**attrs: str) -> str:
    return " ".join(f"{k}={v}" for k, v in attrs.items())

print(total(1, 2, 3))           # 6
print(tag(id="a1", cls="box"))  # id=a1 cls=box

# Variable annotations
count: int = 0
name: str = "Sam"
scores: dict[str, int] = {"ann": 90}

# WHO USES THEM
# - Your editor (autocomplete and warnings)
# - Checkers such as mypy and Pyright
# - Libraries such as FastAPI and Pydantic, which read them at run time
# Type hints in depth come in Module 20.