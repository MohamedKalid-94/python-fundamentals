# A CLOSURE is a function that REMEMBERS variables of the function it was created in,
# even after that function has finished.

# 1. A function factory
def make_multiplier(factor):
    def multiply(x):
        return x * factor                       # "factor" is a FREE variable
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)
print(double(5), triple(5))                     # 10 15

# Look inside
print(double.__code__.co_freevars, double.__closure__[0].cell_contents)     # ('factor',) 2

# 2. Closures keep state; "nonlocal" lets the inner function CHANGE the variable
def make_counter():
    count = 0

    def increment():
        nonlocal count
        count += 1
        return count

    return increment

c1, c2 = make_counter(), make_counter()
print(c1(), c1(), c2())                         # 1 2 1        each counter has its own variable

# Without nonlocal, "count += 1" would create a local variable and fail
def broken():
    total = 0

    def add():
        total += 1
    return add

try:
    broken()()
except UnboundLocalError:
    print("UnboundLocalError")                  # UnboundLocalError

# 3. Hidden state: nothing outside can touch "series"
def make_averager():
    series = []

    def averager(new_value):
        series.append(new_value)                # changing a list needs no "nonlocal"
        return sum(series) / len(series)

    return averager

avg = make_averager()
print(avg(10), avg(20))                         # 10.0 15.0

# 4. Several functions can share the same variable
def make_account(balance):
    def deposit(n):
        nonlocal balance
        balance += n
        return balance

    def withdraw(n):
        nonlocal balance
        balance -= n
        return balance

    return deposit, withdraw

deposit, withdraw = make_account(100)
print(deposit(50), withdraw(30))                # 150 120

# 5. Configuration: a function with a built-in setting
def make_logger(prefix):
    def log(message):
        return f"[{prefix}] {message}"
    return log

uart_log = make_logger("uart")
print(uart_log("rx ok"))                        # [uart] rx ok

# 6. Memoization: a cache that lives inside the closure
def memoize(func):
    cache = {}

    def wrapper(n):
        if n not in cache:
            cache[n] = func(n)
        return cache[n]

    return wrapper

calls = []

def slow_square(n):
    calls.append(n)
    return n * n

fast_square = memoize(slow_square)
fast_square(4)
fast_square(4)
fast_square(5)
print(calls)                                    # [4, 5]       the second fast_square(4) came from the cache

# 7. THE LOOP TRAP (the same as with lambda)
adders = [lambda x: x + i for i in range(3)]
print([a(10) for a in adders])                  # [12, 12, 12]     every lambda sees the final i

adders = [lambda x, i=i: x + i for i in range(3)]
print([a(10) for a in adders])                  # [10, 11, 12]

# 8. Event handlers (embedded style): one factory, one handler per pin
def make_handler(pin):
    def on_press():
        return f"pin {pin} pressed"
    return on_press

handlers = [make_handler(p) for p in (1, 2)]
print([h() for h in handlers])                  # ['pin 1 pressed', 'pin 2 pressed']

# CLOSURE vs CLASS
#   closure   a function with a little hidden state: short and simple
#   class     several methods, several attributes, inheritance
# In C the same idea is a function pointer plus a "context" struct (user data pointer).