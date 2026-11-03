# Python looks up a name in this order (LEGB):
#   L  Local      inside the current function
#   E  Enclosing  inside any outer function
#   G  Global     at the top of the file (module level)
#   B  Built-in   len, print, sum ...

x = "global"

def show():
    x = "local"                 # a NEW local variable, not the global one
    print(x)

show()                          # local
print(x)                        # global

# Reading a global from inside a function is fine
def read():
    print(x)

read()                          # global

# Assigning makes the name local for the WHOLE function
counter = 0

def bad():
    counter += 1                # UnboundLocalError

try:
    bad()
except UnboundLocalError as e:
    print(type(e).__name__)     # UnboundLocalError

# global: say you want the module-level variable
def increment():
    global counter
    counter += 1

increment()
increment()
print(counter)                  # 2
# Prefer parameters and return values over global.

# nonlocal: change a variable of the ENCLOSING function
def outer():
    count = 0
    def inner():
        nonlocal count
        count += 1
        return count
    print(inner(), inner())     # 1 2
    print(count)                # 2

outer()

# if, for and while do NOT create a new scope (only functions do)
for i in range(3):
    last = i * 10
print(i, last)                  # 2 20

if True:
    y = 5
print(y)                        # 5

# Parameters are local names. Rebinding them does not affect the caller.
def bump(n):
    n = n + 1
    return n

v = 1
bump(v)
print(v)                        # 1

# But a MUTABLE argument can be changed in place
def add_one(lst):
    lst.append(1)

def rebind(lst):
    lst = [99]                  # only the local name now points elsewhere

data = []
add_one(data)
print(data)                     # [1]
rebind(data)
print(data)                     # [1]
# Python passes references to objects ("call by assignment").

# Inspecting scopes
print("x" in globals())         # True
def local_demo():
    a = 1
    print(locals())             # {'a': 1}
local_demo()

# Do not reuse built-in names for variables
sum = 10
try:
    sum([1, 2])
except TypeError as e:
    print(type(e).__name__)     # TypeError   (sum is now an int)
del sum                         # the built-in is visible again
print(sum([1, 2]))              # 3