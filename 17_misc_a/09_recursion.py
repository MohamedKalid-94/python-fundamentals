import functools
import sys

# RECURSION: a function that calls itself.
# Every recursive function needs
#   1. a BASE CASE      the simplest input, answered directly (it stops the recursion)
#   2. a RECURSIVE CASE a call on a SMALLER problem, moving toward the base case

# 1. Factorial
def factorial(n):
    if n <= 1:                                  # base case
        return 1
    return n * factorial(n - 1)                 # smaller problem

print(factorial(5))                             # 120

# 2. Fibonacci (this version repeats a lot of work: fine for small n)
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print([fib(i) for i in range(10)])              # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

@functools.lru_cache(maxsize=None)              # a cache makes it fast
def fib_fast(n):
    return n if n < 2 else fib_fast(n - 1) + fib_fast(n - 2)

print(fib_fast(80))                             # 23416728348467685

# 3. Recursion on lists and strings
def sum_list(items):
    return 0 if not items else items[0] + sum_list(items[1:])

def power(base, exp):
    if exp == 0:
        return 1
    half = power(base, exp // 2)
    return half * half if exp % 2 == 0 else half * half * base

def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)

def reverse(s):
    return s if len(s) <= 1 else reverse(s[1:]) + s[0]

def is_palindrome(s):
    return len(s) < 2 or (s[0] == s[-1] and is_palindrome(s[1:-1]))

def sum_digits(n):
    return n if n < 10 else n % 10 + sum_digits(n // 10)

print(sum_list([1, 2, 3, 4]), power(2, 10), gcd(48, 18))    # 10 1024 6
print(reverse("hello"), is_palindrome("racecar"), sum_digits(1234))     # olleh True 10

# 4. Nested data (recursion is natural here)
def flatten(nested):
    result = []
    for x in nested:
        if isinstance(x, list):
            result.extend(flatten(x))
        else:
            result.append(x)
    return result

def depth(x):
    if not isinstance(x, list):
        return 0
    return 1 + max((depth(i) for i in x), default=0)

print(flatten([1, [2, [3, [4]]]]), depth([1, [2, [3]]]))        # [1, 2, 3, 4] 3

tree = {"a.txt": None, "src": {"main.py": None, "util": {"x.py": None}}}

def count_files(t):
    return sum(1 if v is None else count_files(v) for v in t.values())

print(count_files(tree))                        # 3

# 5. Binary search, recursive version
def bsearch(items, target, lo=0, hi=None):
    hi = len(items) - 1 if hi is None else hi
    if lo > hi:
        return -1
    mid = (lo + hi) // 2
    if items[mid] == target:
        return mid
    if items[mid] < target:
        return bsearch(items, target, mid + 1, hi)
    return bsearch(items, target, lo, mid - 1)

print(bsearch([1, 3, 5, 7, 9, 11], 7), bsearch([1, 3, 5, 7, 9, 11], 4))    # 3 -1

# 6. Towers of Hanoi
def hanoi(n, src, dst, aux, moves):
    if n == 0:
        return
    hanoi(n - 1, src, aux, dst, moves)
    moves.append((src, dst))
    hanoi(n - 1, aux, dst, src, moves)

m2, m3 = [], []
hanoi(2, "A", "C", "B", m2)
hanoi(3, "A", "C", "B", m3)
print(m2, len(m3))                              # [('A', 'B'), ('A', 'C'), ('B', 'C')] 7

# 7. Backtracking: all subsets and all permutations
def subsets(items):
    if not items:
        return [[]]
    rest = subsets(items[1:])
    return rest + [[items[0]] + s for s in rest]

def perms(s):
    if len(s) <= 1:
        return [s]
    return [c + p for i, c in enumerate(s) for p in perms(s[:i] + s[i + 1:])]

print(subsets(["a", "b"]))                      # [[], ['b'], ['a'], ['a', 'b']]
print(perms("abc"))                             # ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

# 8. Mutual recursion
def is_even(n):
    return True if n == 0 else is_odd(n - 1)

def is_odd(n):
    return False if n == 0 else is_even(n - 1)

print(is_even(10), is_odd(7))                   # True True

# 9. THE LIMIT: Python allows about 1000 nested calls
print(sys.getrecursionlimit())                  # 1000

depth_reached = 0

def go():
    global depth_reached
    depth_reached += 1
    go()                                        # no base case!

try:
    go()
except RecursionError:
    print("RecursionError", 500 < depth_reached <= sys.getrecursionlimit())     # RecursionError True

# Python does NOT optimise "tail calls". For deep recursion use a loop (or a stack of your own):
def factorial_loop(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

print(factorial_loop(5))                        # 120

# sys.setrecursionlimit(n) can raise the limit, but a too large value crashes the interpreter
# (the C stack overflows). Prefer a loop.

# WHEN TO USE RECURSION
#   good    trees, nested data, divide and conquer, backtracking (the code mirrors the problem)
#   avoid   simple repetition (use a loop) and very deep chains
# Embedded note: on a microcontroller recursion is usually forbidden (the stack is tiny).