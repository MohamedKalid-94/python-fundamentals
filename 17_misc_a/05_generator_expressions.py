import itertools
import sys

# A generator expression looks like a list comprehension with () instead of [].
# It builds NO list: it produces one item at a time.

# 1. The basics
gen = (x * x for x in range(5))
print(type(gen).__name__)                       # generator
print(list(gen), list(gen))                     # [0, 1, 4, 9, 16] []      used up after one pass

# 2. As the only argument of a function you may drop the extra parentheses
print(sum(x * x for x in range(5)),
      max(len(w) for w in ["a", "abc", "ab"]),
      ",".join(str(n) for n in range(3)))       # 30 3 0,1,2

# 3. any() and all() stop as soon as the answer is known: even an endless source works
print(any(n > 3 for n in itertools.count()), all(n % 2 == 0 for n in [2, 4]))   # True True

# 4. "The first match": next() with a default
print(next((x for x in [1, 3, 5, 6] if x % 2 == 0), None),
      next((x for x in [1, 3] if x % 2 == 0), None))                            # 6 None

# 5. A generator has no length and cannot be indexed
try:
    len(x for x in range(3))
except TypeError:
    print("TypeError")                          # TypeError

# 6. LATE evaluation
data = [1, 2, 3]
g = (x for x in data)
data.append(99)                                 # the list is read when the items are pulled
print(list(g))                                  # [1, 2, 3, 99]

threshold = 2
g = (x for x in range(5) if x > threshold)
threshold = 3                                   # the condition sees the NEW value
print(list(g))                                  # [4]

# 7. Memory
print(sys.getsizeof(x * x for x in range(10 ** 6)) < 300,
      sys.getsizeof([x * x for x in range(10 ** 6)]) > 1_000_000)       # True True

# 8. Realistic uses
lines = ["alpha", "be", "gamma"]
print(sum(len(line) for line in lines))         # 12        total characters, without a temporary list
print(sorted(w.upper() for w in lines if len(w) > 2))       # ['ALPHA', 'GAMMA']

# COMPARISON
#   [x for x in data]     list         built at once, can be reused, can be indexed
#   (x for x in data)     generator    built lazily, used once, low memory
#   {x for x in data}     set          unique items
#   {k: v for ...}        dict