d = {"a": 1, "b": 2}

# keys(), values() and items() return VIEW objects, not lists
k = d.keys()
v = d.values()
i = d.items()
print(k, v, i)
# dict_keys(['a', 'b']) dict_values([1, 2]) dict_items([('a', 1), ('b', 2)])
print(type(k))                              # <class 'dict_keys'>

# Views are LIVE: they follow later changes to the dictionary
d["c"] = 3
print(k)                                    # dict_keys(['a', 'b', 'c'])
print(list(v), len(i))                      # [1, 2, 3] 3

# Membership
print("a" in k, 2 in v, ("a", 1) in i)      # True True True

# No indexing: convert first
try:
    k[0]
except TypeError as e:
    print(e)                                # 'dict_keys' object is not subscriptable
print(list(k), tuple(v))                    # ['a', 'b', 'c'] (1, 2, 3)

# keys() and items() behave like SETS
d1 = {"a": 1, "b": 2}
d2 = {"b": 3, "c": 4}
print(sorted(d1.keys() | d2.keys()))        # ['a', 'b', 'c']
print(d1.keys() & d2.keys())                # {'b'}            keys in both
print(d1.keys() - d2.keys())                # {'a'}            keys only in d1
print(sorted(d1.keys() ^ d2.keys()))        # ['a', 'c']
print(d1.items() & {("a", 1), ("z", 9)})    # {('a', 1)}       identical pairs
print(d.keys() == {"a", "b", "c"})          # True
# values() is NOT set-like (values can repeat and may be unhashable)

# Handy combinations
print(sum(d.values()), max(d.values()))     # 6 3
print(sorted(d.items(), key=lambda kv: kv[1], reverse=True))
# [('c', 3), ('b', 2), ('a', 1)]

# Reversed (Python 3.8+)
print(list(reversed(d)))                    # ['c', 'b', 'a']
print(list(reversed(d.items())))            # [('c', 3), ('b', 2), ('a', 1)]

# A SNAPSHOT is a list made from the view
snapshot = list(d.items())
d["z"] = 26
d["a"] = 100
print(snapshot)                             # [('a', 1), ('b', 2), ('c', 3)]
print(v)                                    # dict_values([100, 2, 3, 26])