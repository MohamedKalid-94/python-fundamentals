# *args collects EXTRA POSITIONAL arguments into a TUPLE
def total(*numbers):
    print(numbers, type(numbers).__name__)
    return sum(numbers)

print(total(1, 2, 3))
# (1, 2, 3) tuple
# 6
print(total())
# () tuple
# 0

# **kwargs collects EXTRA KEYWORD arguments into a DICT
def show_profile(**info):
    print(info)
    for key, value in info.items():
        print(f"{key}: {value}")

show_profile(name="Ann", age=30)
# {'name': 'Ann', 'age': 30}
# name: Ann
# age: 30

# ORDER of parameters:
#   positional, defaults, *args, keyword-only, **kwargs
def demo(a, b=2, *args, c=3, **kwargs):
    print(a, b, args, c, kwargs)

demo(1)                                      # 1 2 () 3 {}
demo(1, 10, 20, 30, c=99, x=5, y=6)          # 1 10 (20, 30) 99 {'x': 5, 'y': 6}

# At the CALL, * and ** UNPACK a sequence / dict into arguments
def add3(a, b, c):
    return a + b + c

print(add3(*[1, 2, 3]))                      # 6
print(add3(**{"a": 1, "b": 2, "c": 3}))      # 6

# Forwarding arguments to another function (common in wrappers)
def log_call(func, *args, **kwargs):
    print("calling", func.__name__)
    return func(*args, **kwargs)

print(log_call(add3, 1, 2, c=3))
# calling add3
# 6

# The names "args" and "kwargs" are only a convention; the * and ** matter.
# print(*items) and max(*values) work because they take *args.