import numpy as np

# STRING FUNCTIONS: operate on whole arrays of text.
#   np.strings.*   the modern namespace (NumPy 2): fast ufuncs for upper lower strip replace find count startswith ...
#   np.char.*      the older namespace; still the one with split and join (they return object arrays)
# Arrays of text have a fixed-width dtype: "<U5" = up to 5 characters. Longer values are cut off when assigned
# to an existing array, so build the array with all the text at once. np.dtypes.StringDType() holds text of any length.

words = np.array(["  Alpha ", "beta", "Gamma-Delta", "42"])
print(words.dtype, words.shape, np.strings.str_len(words))
print(np.strings.strip(words), np.strings.upper(words), np.strings.lower(words))
print(np.strings.capitalize(np.array(["hello world", "ÉCOLE"])), np.strings.title(np.array(["hello world"])), np.strings.swapcase(np.array(["aBc"])))

names = np.strings.strip(words)
print(np.strings.replace(names, "a", "@"), np.strings.replace(names, "a", "A", 1))
print(np.strings.find(names, "a"), np.strings.rfind(names, "a"), np.strings.count(names, "a"))
print(np.strings.startswith(names, "G"), np.strings.endswith(names, "a"))
print(np.strings.isalpha(names), np.strings.isdigit(names), np.strings.isnumeric(names), np.strings.isupper(names))
print(np.strings.add(names, "!"), np.strings.multiply(np.array(["ab", "c"]), 3))
print(np.strings.center(np.array(["ab", "abcd"]), 6, "*"), np.strings.ljust(np.array(["ab"]), 5, "."), np.strings.rjust(np.array(["ab"]), 5, "."))
print(np.strings.zfill(np.array(["7", "42", "-3"]), 4))
print(np.strings.partition(np.array(["key=value"]), "="))
print(np.strings.slice(np.array(["abcdef", "uvwxyz"]), 1, 4))
print(np.strings.translate(np.array(["a-b-c"]), str.maketrans("-", "_")))
print(np.strings.mod(np.array(["%d items", "%d boxes"]), 5))                  # format strings are the ARRAY, the values follow
print(np.char.mod("%05.1f", np.array([3.14159, 42.0])))                      # np.char.mod formats every number

# Comparison works with operators and with functions
print(names == "beta", np.strings.equal(names, "42"), np.strings.less(np.array(["a", "c"]), "b"))
print(np.sort(names), np.unique(np.array(["b", "a", "b"])), np.isin(names, ["beta", "42"]))

# Bytes and text
encoded = np.strings.encode(np.array(["héllo", "ok"]), "utf-8")
print(encoded, encoded.dtype, np.strings.decode(encoded, "utf-8"))

# Splitting and joining: np.char (the results are object arrays of Python lists)
lines = np.array(["a b c", "d e"])
pieces = np.char.split(lines)
print([list(p) for p in pieces], [len(p) for p in pieces], np.char.join("-", np.array(["abc", "de"])))

# Variable-width strings
variable = np.array(["a", "a much longer text"], dtype=np.dtypes.StringDType())
print(variable.dtype, np.strings.str_len(variable), np.strings.upper(variable))
fixed = np.array(["a", "bb"])                                       # <U2
fixed[0] = "toolong"
print(fixed)                                                         # cut off to 2 characters

# Use: clean up the labels of a dataset, then count them
labels = np.array([" Cat", "dog ", "CAT", "Dog", "bird", "cat "])
cleaned = np.strings.lower(np.strings.strip(labels))
values, counts = np.unique(cleaned, return_counts=True)
print(cleaned, dict(zip(values.tolist(), counts.tolist())))

# Use: hexadecimal text from a device to numbers
hex_text = np.array(["0A", "FF", "7F"])
print(np.array([int(h, 16) for h in hex_text]), np.char.mod("%02X", np.array([10, 255, 127])))

# EXPECTED OUTPUT
# <U11 (4,) [ 8  4 11  2]
# ['Alpha' 'beta' 'Gamma-Delta' '42'] ['  ALPHA ' 'BETA' 'GAMMA-DELTA' '42'] ['  alpha ' 'beta' 'gamma-delta' '42']
# ['Hello world' 'École'] ['Hello World'] ['AbC']
# ['Alph@' 'bet@' 'G@mm@-Delt@' '42'] ['AlphA' 'betA' 'GAmma-Delta' '42']
# [ 4  3  1 -1] [ 4  3 10 -1] [1 1 3 0]
# [False False  True False] [ True  True  True False]
# [ True  True False False] [False False False  True] [False False False  True] [False False False False]
# ['Alpha!' 'beta!' 'Gamma-Delta!' '42!'] ['ababab' 'ccc']
# ['**ab**' '*abcd*'] ['ab...'] ['...ab']
# ['0007' '0042' '-003']
# (array(['key'], dtype='<U3'), array(['='], dtype='<U1'), array(['value'], dtype='<U5'))
# ['bcd' 'vwx']
# ['a_b_c']
# ['5 items' '5 boxes']
# ['003.1' '042.0']
# [False  True False False] [False False False  True] [ True False]
# ['42' 'Alpha' 'Gamma-Delta' 'beta'] ['a' 'b'] [False  True False  True]
# [b'h\xc3\xa9llo' b'ok'] |S6 ['héllo' 'ok']
# [['a', 'b', 'c'], ['d', 'e']] [3, 2] ['a-b-c' 'd-e']
# StringDType() [ 1 18] ['A' 'A MUCH LONGER TEXT']
# ['to' 'bb']
# ['cat' 'dog' 'cat' 'dog' 'bird' 'cat'] {'bird': 1, 'cat': 3, 'dog': 2}
# [ 10 255 127] ['0A' 'FF' '7F']