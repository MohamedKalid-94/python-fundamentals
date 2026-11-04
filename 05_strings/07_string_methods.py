# Every method returns a NEW value; the original string never changes.

# ---------- Case ----------
print("Hello World".upper(), "Hello World".lower())   # HELLO WORLD hello world
print("Straße".lower(), "Straße".casefold())          # straße strasse
# casefold() is the right choice for case-insensitive comparison

# ---------- Searching ----------
s = "banana"
print(s.find("an"), s.find("an", 2), s.rfind("an"), s.find("x"))   # 1 3 3 -1
try:
    s.index("x")                    # like find(), but raises an error
except ValueError as e:
    print(e)                        # substring not found
print(s.count("a"), s.count("an"))  # 3 2
print(s.startswith("ban"), s.endswith("na"), s.startswith(("x", "b")))   # True True True

# ---------- Testing ----------
print("123".isdigit(), "12a".isdigit(), "".isdigit(), "-5".isdigit())   # True False False False
print("abc".isalpha(), "abc123".isalnum(), "  ".isspace())              # True True True
print("ABC".isupper(), "abc".islower(), "Hello World".istitle())        # True True True
print("²".isdigit(), "²".isdecimal(), "½".isnumeric(), "½".isdigit())   # True False True False
print("my_var".isidentifier(), "abc".isascii())                         # True True

# ---------- Cleaning ----------
print(repr("  hi \n".strip()))     # 'hi'

# ---------- Splitting ----------
print("a b  c".split())                         # ['a', 'b', 'c']
print("a,b,c".split(",", 1))                    # ['a', 'b,c']
print("a,b,c".rsplit(",", 1))                   # ['a,b', 'c']
print("line1\nline2\r\nline3".splitlines())      # ['line1', 'line2', 'line3']
print("key=value=more".partition("="))           # ('key', '=', 'value=more')
print("key=value=more".rpartition("="))          # ('key=value', '=', 'more')
print("nokey".partition("="))                    # ('nokey', '', '')

# ---------- Joining ----------
print("-".join(["a", "b", "c"]))                # a-b-c

# ---------- Replacing and translating ----------
print("banana".replace("a", "o", 2))            # bonona
table = str.maketrans("abc", "xyz")
print("aabbcc".translate(table))                # xxyyzz
print("a\tb".expandtabs(4))                      # a   b

# ---------- Alignment ----------
print("hi".center(6, "*"), "hi".ljust(5, "."), "hi".rjust(5, "."), "-42".zfill(5))
# **hi** hi... ...hi -0042

# ---------- Prefix and suffix (3.9+) ----------
print("report.pdf".removesuffix(".pdf"), "test_main".removeprefix("test_"))   # report main

# ---------- Encoding ----------
print("é".encode("utf-8"))                      # b'\xc3\xa9'
print(b"\xc3\xa9".decode("utf-8"))              # é

# ---------- Format ----------
print("{} + {} = {}".format(1, 2, 3))           # 1 + 2 = 3

# ---------- Chaining methods ----------
print("  Hello World  ".strip().lower().replace(" ", "_"))   # hello_world