# Built-in functions are always available (no import).

# --- Numbers ---
print(abs(-5), abs(-3.5))                   # 5 3.5
print(round(3.14159, 2), round(2.5), round(1234.5678, -2))   # 3.14 2 1200.0
print(pow(2, 5), pow(2, 3, 5))              # 32 3
print(divmod(17, 5))                        # (3, 2)
print(min(3, 1, 2), max([4, 9, 1]))         # 1 9
print(sum([1, 2, 3]), sum([1, 2, 3], 10))   # 6 16
print(sum(range(1, 101)))                   # 5050
print(max("apple", "banana"))               # banana
print(min([], default=0))                   # 0

# --- Type conversion ---
print(int("42"), float("3.5"), str(10), bool([]))   # 42 3.5 10 False
print(list("abc"), tuple([1, 2]), set([1, 1, 2]))   # ['a', 'b', 'c'] (1, 2) {1, 2}
print(int("ff", 16), bin(10), hex(255), oct(8))     # 255 0b1010 0xff 0o10
print(ord("A"), chr(97), chr(ord("a") + 1))         # 65 a b
print(format(3.14159, ".2f"), repr("hi"))           # 3.14 'hi'

# --- Sequences and iteration ---
print(len("hello"), len([1, 2, 3]), len({"a": 1}))  # 5 3 1
print(sorted([3, 1, 2]), sorted([3, 1, 2], reverse=True))   # [1, 2, 3] [3, 2, 1]
print(sorted(["pear", "fig", "apple"], key=len))    # ['fig', 'pear', 'apple']
print(max(["pear", "fig", "apple"], key=len))       # apple
print(list(reversed([1, 2, 3])))                    # [3, 2, 1]
print(list(enumerate("ab")))                        # [(0, 'a'), (1, 'b')]
print(list(zip([1, 2], ["a", "b"])))                # [(1, 'a'), (2, 'b')]
print(list(map(str, [1, 2, 3])))                    # ['1', '2', '3']
print(list(map(lambda x: x ** 2, [1, 2, 3])))       # [1, 4, 9]
print(list(filter(None, [0, 1, "", 2])))            # [1, 2]
print(list(filter(lambda n: n % 2 == 0, range(6)))) # [0, 2, 4]
# (lambda is covered in Module 17: for now, read it as a tiny nameless function)

# --- Truth tests ---
print(any([0, 0, 1]), all([1, 1, 0]))       # True False
print(any([]), all([]))                     # False True

# --- Iterators ---
it = iter([1, 2])
print(next(it), next(it), next(it, "done")) # 1 2 done

# --- Inspecting objects ---
print(type(5), isinstance(5, (int, float))) # <class 'int'> True
print(callable(len), callable(5))           # True False
print(hasattr("abc", "upper"), getattr("abc", "upper")())   # True ABC
print(hash(5))                              # 5

# --- Evaluating text (DANGEROUS with untrusted input) ---
print(eval("2 + 3 * 4"))                    # 14

# --- Other built-ins to know ---
# print, input, open (Module 11), help, dir, id, vars, globals, locals,
# isinstance, issubclass, slice, bytes, bytearray, frozenset, complex, object

import builtins
print("len" in dir(builtins))               # True