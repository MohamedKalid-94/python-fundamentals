# Strings are immutable: every "change" returns a NEW string.
# Assign the result if you want to keep it.

text = "Hello World"
print(text.upper())             # HELLO WORLD
print(text.lower())             # hello world
print("hello world".title())    # Hello World
print("hello world".capitalize())   # Hello world
print(text.swapcase())          # hELLO wORLD
print(text)                     # Hello World   (unchanged!)

# Removing whitespace
raw = "  hi  "
print(f"[{raw.strip()}]")       # [hi]
print(f"[{raw.lstrip()}]")      # [hi  ]
print(f"[{raw.rstrip()}]")      # [  hi]
print("xxhixx".strip("x"))      # hi

# Replacing
print("banana".replace("a", "o"))       # bonono
print("banana".replace("a", "o", 2))    # bonona   (only the first 2)
print("hello".replace("l", ""))         # heo      (delete characters)

# Rebuilding with slices
word = "Hello"
word = "J" + word[1:]
print(word)                     # Jello

base = "Hello"
print(base[:2] + "XX" + base[2:])       # HeXXllo   (insert)

# Split and join
print("a,b,c".split(","))               # ['a', 'b', 'c']
print("a b  c".split())                 # ['a', 'b', 'c']   (any whitespace)
print("a,b,c".split(",", 1))            # ['a', 'b,c']
print(" ".join(["a", "b"]))             # a b
print("-".join("abc"))                  # a-b-c

# Changing single characters: go through a list
chars = list("hello")
chars[0] = "j"
print("".join(chars))                   # jello

# Padding and alignment
print("hi".center(6, "*"))              # **hi**
print("hi".ljust(5, "."))               # hi...
print("hi".rjust(5, "."))               # ...hi
print("42".zfill(5))                    # 00042

# Prefix and suffix (Python 3.9+)
print("report.pdf".removesuffix(".pdf"))    # report
print("test_main".removeprefix("test_"))    # main

# Translating characters
table = str.maketrans("abc", "xyz")
print("aabbcc".translate(table))        # xxyyzz