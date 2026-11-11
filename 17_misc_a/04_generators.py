import inspect
import sys
from itertools import islice

# A GENERATOR is an iterator written as a function with "yield".
# Each next() runs the function up to the next yield, then PAUSES it with all its variables.

# 1. The basics
def countdown(n):
    while n > 0:
        yield n
        n -= 1

gen = countdown(3)
print(type(gen).__name__)                       # generator
print(next(gen), next(gen), next(gen))          # 3 2 1
try:
    next(gen)
except StopIteration:
    print("done")                               # done
print(list(countdown(3)))                       # [3, 2, 1]

# 2. Nothing runs until you ask for the first value
def noisy():
    print("start")
    yield 1
    print("middle")
    yield 2
    print("end")

g = noisy()
print("created")
print(next(g))
print(next(g))
try:
    next(g)
except StopIteration:
    print("finished")
# created
# start
# 1
# middle
# 2
# end
# finished

# 3. An endless generator, cut with islice
def fib():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

print(list(islice(fib(), 10)))                  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

# 4. yield from: hand over to another iterable
def chain_gen(*iterables):
    for it in iterables:
        yield from it

print(list(chain_gen([1, 2], "ab")))            # [1, 2, 'a', 'b']

def flatten(nested):
    for x in nested:
        if isinstance(x, list):
            yield from flatten(x)               # recursion with generators
        else:
            yield x

print(list(flatten([1, [2, [3, 4]], 5])))       # [1, 2, 3, 4, 5]

# 5. send(): push values INTO a generator (a running average)
def averager():
    total, count, average = 0, 0, None
    while True:
        value = yield average
        total += value
        count += 1
        average = total / count

avg = averager()
next(avg)                                       # run to the first yield ("prime" it)
print(avg.send(10), avg.send(20), avg.send(30)) # 10.0 15.0 20.0

# 6. close() and throw()
def worker():
    try:
        while True:
            yield
    except GeneratorExit:
        print("cleanup")                        # runs when the generator is closed

w = worker()
next(w)
w.close()                                       # cleanup

def catcher():
    try:
        yield 1
    except ValueError:
        yield "handled"

c = catcher()
next(c)
print(c.throw(ValueError))                      # handled

# 7. A generator can return a value (it travels inside StopIteration)
def with_result():
    yield 1
    return "result"

r = with_result()
next(r)
try:
    next(r)
except StopIteration as e:
    print(e.value)                              # result

def outer():
    res = yield from with_result()              # yield from gives you the returned value
    yield res

print(list(outer()))                            # [1, 'result']

# 8. A pipeline: each stage handles one item at a time, nothing is stored
def read_numbers():
    yield from [1, 2, 3, 4, 5, 6]

def evens(numbers):
    for n in numbers:
        if n % 2 == 0:
            yield n

def squares(numbers):
    for n in numbers:
        yield n * n

print(list(squares(evens(read_numbers()))))     # [4, 16, 36]

# 9. The state of a generator
g = countdown(2)
print(inspect.getgeneratorstate(g))             # GEN_CREATED
next(g)
print(inspect.getgeneratorstate(g))             # GEN_SUSPENDED
list(g)
print(inspect.getgeneratorstate(g))             # GEN_CLOSED

# 10. Memory: a list stores everything, a generator stores almost nothing
def numbers(n):
    for i in range(n):
        yield i

print(sys.getsizeof(list(range(1_000_000))) > 1_000_000,
      sys.getsizeof(numbers(1_000_000)) < 300)  # True True

# WHEN TO USE A GENERATOR
#   - big or endless data: log files, sensor streams, database rows, pages of an API
#   - pipelines that transform data step by step
#   - a generator is used ONCE: to loop again, call the function again