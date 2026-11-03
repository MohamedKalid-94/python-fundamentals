s = "Aé你😀"
print(len(s))                         # 4  (4 characters = 4 code points)

for ch in s:
    print(ch, ord(ch), hex(ord(ch)), len(ch.encode("utf-8")))
# A 65 0x41 1
# é 233 0xe9 2
# 你 20320 0x4f60 3
# 😀 128512 0x1f600 4

# Escape forms
print("\u00e9", "\U0001F600", "\N{GREEK SMALL LETTER ALPHA}")   # é 😀 α

# str (text) vs bytes (raw data)
data = s.encode("utf-8")
print(data)           # b'A\xc3\xa9\xe4\xbd\xa0\xf0\x9f\x98\x80'
print(len(data))      # 10  (bytes, not characters)
print(data.decode("utf-8") == s)      # True

import sys
print(sys.getdefaultencoding())       # utf-8