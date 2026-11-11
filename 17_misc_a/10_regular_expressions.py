import re

# A REGULAR EXPRESSION (regex) describes a pattern of text.
# ALWAYS write patterns as RAW strings: r"\d+", so Python does not touch the backslashes.
#
#   .        any character except newline        \d digit   \w letter/digit/_   \s whitespace
#   \D \W \S the opposites                       [abc] one of a, b, c   [a-z] a range   [^0-9] not a digit
#   ^ start of the text   $ end   \b word boundary
#   *  0 or more   +  1 or more   ?  0 or 1   {3}  exactly 3   {2,4}  2 to 4
#   (...) a group   (?P<name>...) a named group   a|b  a or b   (?:...) a group that is not captured
#   (?=...) followed by   (?<=...) preceded by   \1 the same text as group 1

text = "Call 555-1234 or 555-9876 today"

# 1. search (anywhere), match (at the start), fullmatch (the whole text)
print(re.search(r"\d{3}-\d{4}", text).group())  # 555-1234
print(re.findall(r"\d{3}-\d{4}", text))         # ['555-1234', '555-9876']
print(re.match(r"Call", text) is not None, re.match(r"today", text))        # True None
print(re.fullmatch(r"\d+", "123") is not None, re.fullmatch(r"\d+", "12a")) # True None

# 2. Groups and the match object
m = re.search(r"(\d{3})-(\d{4})", text)
print(m.group(0), m.group(1), m.group(2), m.groups(), m.span())
# 555-1234 555 1234 ('555', '1234') (5, 13)

m = re.search(r"(?P<area>\d{3})-(?P<num>\d{4})", text)
print(m.group("area"), m.groupdict())           # 555 {'area': '555', 'num': '1234'}

# 3. finditer: every match with its position
print([(m.group(), m.start()) for m in re.finditer(r"\d{3}-\d{4}", text)])
# [('555-1234', 5), ('555-9876', 17)]

# 4. Replace
print(re.sub(r"\d", "#", "a1b22"), re.subn(r"\d", "#", "a1b22"))            # a#b## ('a#b##', 3)
print(re.sub(r"(\w+)@(\w+)\.com", r"\2:\1", "ann@site.com"))                # site:ann
print(re.sub(r"\d+", lambda m: str(int(m.group()) * 2), "a1 b22"))          # a2 b44

# 5. Split
print(re.split(r"[,;]\s*", "a, b;c"), re.split(r"(,)", "a,b"))              # ['a', 'b', 'c'] ['a', ',', 'b']

# 6. Flags
print(re.findall(r"cat", "Cat cat CAT", re.IGNORECASE))                     # ['Cat', 'cat', 'CAT']
print(re.findall(r"^\w+", "one\ntwo", re.MULTILINE))                        # ['one', 'two']
print(re.search(r"a.b", "a\nb"), bool(re.search(r"a.b", "a\nb", re.DOTALL)))    # None True

# 7. Greedy or lazy: add ? to take as LITTLE as possible
print(re.search(r"<.+>", "<a><b>").group(), re.search(r"<.+?>", "<a><b>").group())  # <a><b> <a>

# 8. Whole words
print(re.findall(r"\bcat\b", "cat concat cat."))                            # ['cat', 'cat']

# 9. findall with groups returns the GROUPS
pairs = re.findall(r"(\w+)=(\d+)", "a=1, b=22")
print(pairs, dict(pairs))                       # [('a', '1'), ('b', '22')] {'a': '1', 'b': '22'}

# 10. Look-ahead and look-behind
print(re.findall(r"\d+(?= dollars)", "5 dollars 7 euros"))                  # ['5']
print(re.findall(r"(?<=\$)\d+", "cost $30 and $4"))                         # ['30', '4']

# 11. Back-references
print(re.search(r"(\w)\1", "hello").group(), re.findall(r"\b(\w+) \1\b", "the the cat"))  # ll ['the']

# 12. compile() a pattern you use many times
pattern = re.compile(r"(\d+)-(\d+)")
print(pattern.search("tel 12-34").groups())     # ('12', '34')

# 13. Special characters in the TEXT you search for: re.escape
print(re.escape("a.b*c"))                       # a\.b\*c

# 14. VERBOSE: spaces and comments inside a long pattern
date_pattern = re.compile(r"""
    (\d{4}) - (\d{2}) - (\d{2})     # year - month - day
""", re.VERBOSE)
print(date_pattern.fullmatch("2026-11-10").groups())    # ('2026', '11', '10')

# 15. Useful patterns (rough checks, not perfect validators)
email = r"[\w.+-]+@[\w-]+\.[\w.-]+"
print(bool(re.fullmatch(email, "ann@example.com")), re.fullmatch(email, "bad@"))   # True None

log_line = "2026-11-10 14:30:15 ERROR disk full"
m = re.match(r"(?P<date>\S+) (?P<time>\S+) (?P<level>[A-Z]+) (?P<msg>.*)", log_line)
print(m.groupdict())
# {'date': '2026-11-10', 'time': '14:30:15', 'level': 'ERROR', 'msg': 'disk full'}

print(re.findall(r"[A-Z]+=-?\d+(?:\.\d+)?", "TEMP=36.5;HUM=40;X=-3"))     # ['TEMP=36.5', 'HUM=40', 'X=-3']

# 16. \w also matches letters of other languages (Unicode)
print(re.findall(r"\w+", "café ok"))            # ['café', 'ok']

# PITFALLS
#  - match() only looks at the START of the text; use search() to look anywhere.
#  - "." does not match a newline unless you use re.DOTALL.
#  - Nested quantifiers such as (a+)+ can take forever on some inputs ("catastrophic backtracking").
#  - Do not parse HTML or JSON with regex: use an HTML parser or the json module.
#  - If str methods are enough ("in", startswith, split, replace), use them: they are simpler.