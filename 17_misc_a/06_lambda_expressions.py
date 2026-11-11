import functools
from functools import partial, reduce
from operator import itemgetter, mul

# lambda arguments: expression       a tiny anonymous function with ONE expression

# 1. The basics
add = lambda a, b: a + b
print(add(2, 3), (lambda x: x * 2)(4), type(add), add.__name__)
# 5 8 <class 'function'> <lambda>

# 2. As a key function
print(sorted(["pear", "fig", "apple"], key=lambda w: len(w)))           # ['fig', 'pear', 'apple']
print(sorted(["ab", "ba", "cc"], key=lambda s: s[-1]))                  # ['ba', 'ab', 'cc']
people = [("Ann", 30), ("Bob", 25)]
print(sorted(people, key=lambda p: p[1]))                               # [('Bob', 25), ('Ann', 30)]
print(max(people, key=lambda p: p[1]))                                  # ('Ann', 30)
print(sorted(["pear", "fig", "apple", "kiwi"], key=lambda w: (len(w), w)))
# ['fig', 'kiwi', 'pear', 'apple']

# 3. With map, filter and reduce
print(list(map(lambda x: x ** 2, [1, 2, 3])), list(filter(lambda n: n % 2, range(6))))
# [1, 4, 9] [1, 3, 5]
print(reduce(lambda a, b: a * b, [1, 2, 3, 4]))                         # 24

# 4. Conditional expression, default values, *args
parity = lambda n: "even" if n % 2 == 0 else "odd"
print([parity(n) for n in (3, 4)])              # ['odd', 'even']
power = lambda x, n=2: x ** n
print(power(3), power(3, 3))                    # 9 27
total = lambda *nums: sum(nums)
print(total(1, 2, 3))                           # 6

# 5. A table of actions (a dispatch table)
ops = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b,
}
print(ops["*"](3, 4))                           # 12

# 6. THE LATE-BINDING TRAP: the lambda reads i when it is CALLED, not when it is created
funcs = [lambda: i for i in range(3)]
print([f() for f in funcs])                     # [2, 2, 2]
funcs = [lambda i=i: i for i in range(3)]       # a default argument captures the value now
print([f() for f in funcs])                     # [0, 1, 2]

# 7. Alternatives that are often clearer
print(sorted(people, key=itemgetter(1)))        # [('Bob', 25), ('Ann', 30)]
print(reduce(mul, [1, 2, 3, 4]))                # 24
to_int = partial(int, base=2)                   # partial fixes some arguments of a function
print(to_int("101"))                            # 5

# LIMITS
#  - Only ONE expression: no statements, no assignments (no "x = 1", no "for", no "return").
#  - If it needs a name or more than one line, write a normal "def" (PEP 8: do not do  f = lambda ...).
#  - Error messages show "<lambda>", which is harder to debug.
# Typical uses: key= functions, short callbacks (buttons, event handlers), dispatch tables.