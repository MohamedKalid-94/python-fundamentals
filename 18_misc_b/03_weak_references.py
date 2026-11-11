import gc
import sys
import weakref

# A normal reference KEEPS an object alive. A WEAK reference does not:
# when the last normal reference goes away, the object is destroyed and the weak reference
# becomes None. Use it for caches, observer lists and parent links.

class Node:
    def __init__(self, name):
        self.name = name

# 1. weakref.ref: call it to get the object (or None)
n = Node("a")
r = weakref.ref(n)
print(r() is n)                                 # True
del n
gc.collect()
print(r())                                      # None

# 2. A callback runs when the object dies
log = []
n = Node("b")
r = weakref.ref(n, lambda ref: log.append("collected"))
del n
gc.collect()
print(log)                                      # ['collected']

# 3. weakref.proxy: use it like the object itself
n = Node("c")
p = weakref.proxy(n)
print(p.name)                                   # c
del n
gc.collect()
try:
    p.name
except ReferenceError:
    print("ReferenceError")                     # ReferenceError

# 4. Not every object can have a weak reference
for obj in (5, "text", [1], {"a": 1}, (1, 2)):
    try:
        weakref.ref(obj)
    except TypeError:
        print(type(obj).__name__, end=" ")
print()                                         # int str list dict tuple   (a space follows the last name)

class MyList(list):                             # but a SUBCLASS of list can
    pass

print(weakref.ref(MyList()) is not None)        # True

# 5. WeakValueDictionary: a cache that does not keep its values alive
cache = weakref.WeakValueDictionary()
obj = Node("x")
cache["k"] = obj
print("k" in cache, len(cache))                 # True 1
del obj
gc.collect()
print(len(cache))                               # 0

# 6. WeakSet: a list of observers that forgets the dead ones
observers = weakref.WeakSet()
a, b = Node("a"), Node("b")
observers.add(a)
observers.add(b)
print(len(observers))                           # 2
del a
gc.collect()
print(sorted(o.name for o in observers))        # ['b']

# 7. WeakKeyDictionary: extra data attached to objects, without keeping them alive
meta = weakref.WeakKeyDictionary()
item = Node("i")
meta[item] = {"hits": 1}
print(len(meta))                                # 1
del item
gc.collect()
print(len(meta))                                # 0

# 8. Parent <-> child links without a reference cycle
class Parent:
    def __init__(self):
        self.children = []

class Child:
    def __init__(self, parent):
        self._parent = weakref.ref(parent)      # a weak link back to the parent
        parent.children.append(self)

    @property
    def parent(self):
        return self._parent()

parent = Parent()
child = Child(parent)
print(child.parent is parent)                   # True
del parent
gc.collect()
print(child.parent)                             # None

# 9. finalize: run a cleanup when an object is destroyed (safer than __del__)
events = []
res = Node("res")
fin = weakref.finalize(res, events.append, "cleaned")
print(fin.alive)                                # True
del res
gc.collect()
print(events, fin.alive)                        # ['cleaned'] False

# 10. How many references does an object have?
x = []
print(sys.getrefcount(x))                       # 2     (the name x, and the argument of getrefcount)
y = x
print(sys.getrefcount(x))                       # 3

# 11. Objects that point at each other need the cycle collector (gc), not just reference counting
class Cycle:
    pass

c1, c2 = Cycle(), Cycle()
c1.other, c2.other = c2, c1
probe = weakref.ref(c1)
del c1, c2
gc.collect()
print(probe())                                  # None

# WHEN TO USE WEAK REFERENCES
#   caches of big objects     WeakValueDictionary
#   observer / listener lists WeakSet
#   back-pointers (child -> parent) to avoid cycles
# In CPython objects usually die the moment the last reference goes; other Python
# implementations may wait, which is why the examples call gc.collect().