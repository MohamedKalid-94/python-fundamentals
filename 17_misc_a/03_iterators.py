import sys
from io import BytesIO
from itertools import (accumulate, chain, combinations, combinations_with_replacement, count,
                       cycle, dropwhile, groupby, islice, pairwise, permutations, product,
                       repeat, starmap, takewhile, tee, zip_longest)

# ITERABLE : an object you can loop over (list, str, dict, file ...). It has __iter__().
# ITERATOR : the object that does the looping. It has __next__() and remembers its position.

# 1. iter() gives the iterator, next() gives the next item
it = iter([1, 2, 3])
print(next(it), next(it), next(it))             # 1 2 3
try:
    next(it)
except StopIteration:
    print("exhausted")                          # exhausted
print(next(it, "default"))                      # default      a fallback instead of the exception
print(iter(it) is it)                           # True         an iterator is its own iterator
print(hasattr([1], "__next__"), hasattr(iter([1]), "__next__"))     # False True

# 2. This is what a for loop does
it = iter(["a", "b"])
while True:
    try:
        item = next(it)
    except StopIteration:
        break
    print(item)
# a
# b

# 3. Your own iterator class
class Countdown:
    def __init__(self, start):
        self.n = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.n <= 0:
            raise StopIteration
        value = self.n
        self.n -= 1
        return value

c = Countdown(3)
print(list(c), list(c))                         # [3, 2, 1] []       an iterator is used up after one pass

# 4. An iterable that gives a FRESH iterator every time can be looped many times
class Evens:
    def __init__(self, limit):
        self.limit = limit

    def __iter__(self):
        return iter(range(0, self.limit, 2))

e = Evens(5)
print(list(e), list(e))                         # [0, 2, 4] [0, 2, 4]

# 5. The old protocol: an object with __getitem__ and IndexError is iterable too
class Seq:
    def __getitem__(self, i):
        if i >= 3:
            raise IndexError
        return i * 10

print(list(Seq()))                              # [0, 10, 20]

# 6. Many built-ins are LAZY: they produce items only when asked
print(type(map(str, [1])).__name__, type(enumerate("ab")).__name__, type(zip()).__name__)
# map enumerate zip
m = map(str, [1, 2])
print(list(m), list(m))                         # ['1', '2'] []
print(sys.getsizeof(range(10 ** 9)) < 100)      # True      a range stores 3 numbers, not a billion

# 7. itertools: building blocks for iterators
print(list(islice(count(10, 5), 3)))            # [10, 15, 20]        count() never ends, islice() cuts it
print(list(islice(cycle("ab"), 5)))             # ['a', 'b', 'a', 'b', 'a']
print(list(repeat("x", 3)))                     # ['x', 'x', 'x']
print(list(chain([1, 2], (3,), "ab")))          # [1, 2, 3, 'a', 'b']
print(list(chain.from_iterable([[1], [2, 3]]))) # [1, 2, 3]
print(list(islice(range(10), 2, 8, 2)))         # [2, 4, 6]           slicing for any iterator
print(list(zip_longest([1, 2, 3], ["a"], fillvalue="-")))       # [(1, 'a'), (2, '-'), (3, '-')]
print(list(accumulate([1, 2, 3, 4])))           # [1, 3, 6, 10]       running total
print(list(accumulate([3, 1, 4, 1, 5], max)))   # [3, 3, 4, 4, 5]     running maximum
print([(k, len(list(g))) for k, g in groupby("aabbbc")])        # [('a', 2), ('b', 3), ('c', 1)]
# groupby groups NEIGHBOURS only: sort the data first when you want one group per key

print(list(product([1, 2], "ab")))              # [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]
print(list(product(range(2), repeat=2)))        # [(0, 0), (0, 1), (1, 0), (1, 1)]
print(list(permutations([1, 2, 3], 2)))         # [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]
print(list(combinations([1, 2, 3], 2)))         # [(1, 2), (1, 3), (2, 3)]
print(list(combinations_with_replacement([1, 2], 2)))           # [(1, 1), (1, 2), (2, 2)]

print(list(takewhile(lambda n: n < 3, [1, 2, 3, 1])), list(dropwhile(lambda n: n < 3, [1, 2, 3, 1])))
# [1, 2] [3, 1]
print(list(starmap(pow, [(2, 3), (3, 2)])))     # [8, 9]
print(list(pairwise([1, 2, 3, 4])))             # [(1, 2), (2, 3), (3, 4)]       Python 3.10+
a, b = tee([1, 2, 3])                           # two independent iterators from one
print(list(a), list(b))                         # [1, 2, 3] [1, 2, 3]

# 8. iter(function, sentinel): call the function until it returns the sentinel
f = BytesIO(b"abcdef")
print(list(iter(lambda: f.read(2), b"")))       # [b'ab', b'cd', b'ef']      reading a file in chunks