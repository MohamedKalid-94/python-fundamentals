def power(base, exponent=2):
    return base ** exponent

print(power(5))                 # 25      exponent uses the default
print(power(2, 10))             # 1024
print(power(3, exponent=3))     # 27

def greet(name, greeting="Hello", punctuation="!"):
    return f"{greeting}, {name}{punctuation}"

print(greet("Ann"))                      # Hello, Ann!
print(greet("Ann", "Hi"))                # Hi, Ann!
print(greet("Ann", punctuation="?"))     # Hello, Ann?

# RULE: parameters with defaults must come AFTER those without
# def bad(a=1, b):      -> SyntaxError

# Defaults are evaluated ONCE, when the function is defined
x = 10
def show(v=x):
    print(v)

x = 99
show()                          # 10      (not 99)

# TRAP: a mutable default is shared between calls
def add_item(item, items=[]):
    items.append(item)
    return items

print(add_item("a"))            # ['a']
print(add_item("b"))            # ['a', 'b']        surprise!
print(add_item("c"))            # ['a', 'b', 'c']
print(add_item.__defaults__)    # (['a', 'b', 'c'],)

# FIX: use None as the default and create the list inside
def add_item_safe(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

print(add_item_safe("a"))       # ['a']
print(add_item_safe("b"))       # ['b']