import re

import numpy as np
import pandas as pd

# TEXT DATA: the .str accessor applies string methods to a whole column (Series or Index), and skips missing values
#   case      lower upper title capitalize swapcase casefold          cleaning   strip lstrip rstrip replace removeprefix removesuffix
#   test      contains startswith endswith match fullmatch isalpha isdigit isnumeric isupper islower
#   find      find count len findall extract extractall                cut/join   slice get split rsplit partition cat repeat pad center zfill
#   other     normalize encode decode translate get_dummies
#   regex     replace / contains / split use regular expressions by default for patterns: regex=False for plain text
# Missing text stays missing: str.upper() of NaN is NaN; str.len() gives NaN; tests such as contains give False.

s = pd.Series(["  Ann Lee ", "bo-xu", None, "CY Ray", "d.i"], name="name")
print(s.str.strip().tolist())
print(s.str.lower().tolist(), s.str.upper().tolist(), s.str.strip().str.title().tolist(), s.str.strip().str.capitalize().tolist(), s.str.swapcase().tolist()[3])
print(s.str.len().tolist(), s.str.strip().str.len().tolist(), s.str.count("o").tolist(), s.str.find("e").tolist())

# Tests and selections
print(s.str.contains("Ray").tolist(), s.str.contains("ray", case=False).tolist(), s.str.contains("o|e").tolist())
print(s.str.startswith("bo").tolist(), s.str.endswith("i").tolist(), s.str.contains("^[A-Z]{2}", regex=True).tolist())
print(s.str.contains("Ann", na=True).tolist(), s[s.str.contains("-|\\.", na=False)].tolist())
print(pd.Series(["a1", "12", "ab", "A"]).str.isalpha().tolist(), pd.Series(["a1", "12", "ab", "A"]).str.isdigit().tolist(), pd.Series(["a1", "12", "ab", "A"]).str.isupper().tolist())
print(s.str.match(r"\s*Ann").tolist(), s.str.fullmatch(r"d\.i").tolist())

# Replacing (regular expressions by default: regex=False for a plain text)
messy = pd.Series(["a-b-c", "x.y.z", "1 2  3", "Hello World"])
print(messy.str.replace("-", "_").tolist(), messy.str.replace(".", "_", regex=False).tolist(), messy.str.replace(".", "_", regex=True).tolist()[1])
print(messy.str.replace(r"\s+", " ", regex=True).tolist()[2], messy.str.replace(r"\d", "#", regex=True).tolist()[2], messy.str.replace("hello", "Bye", case=False, regex=True).tolist()[3])
print(messy.str.replace(r"(\w)-(\w)", r"\2-\1", regex=True).tolist()[0], messy.str.replace("o", lambda m: m.group(0).upper(), regex=True).tolist()[3])
print(pd.Series(["pre_name", "name_suf"]).str.removeprefix("pre_").tolist(), pd.Series(["pre_name", "name_suf"]).str.removesuffix("_suf").tolist())

# Splitting, joining, slicing
names = pd.Series(["Ann Lee", "Bo Xu Jr", "Cy"])
print(names.str.split().tolist(), names.str.split(" ", n=1).tolist(), names.str.split().str.len().tolist())
print(names.str.split(expand=True))
print(names.str.split(expand=True, n=1).rename(columns={0: "first", 1: "rest"}).values.tolist())
print(names.str.split().str[0].tolist(), names.str.split().str.get(-1).tolist(), names.str.rsplit(n=1).str[0].tolist())
print(names.str[:2].tolist(), names.str.slice(1, 4).tolist(), names.str.slice(stop=3).tolist(), names.str[-2:].tolist())
print(names.str.partition(" ").values.tolist())
print(names.str.cat(sep="; "), names.str.cat(["x", "y", "z"], sep="-").tolist(), names.str.cat(pd.Series(["!", "?", "."]), na_rep="").tolist())
print(names.str.repeat(2).tolist()[2], pd.Series(["7", "42"]).str.zfill(4).tolist(), pd.Series(["ab"]).str.pad(6, side="left", fillchar=".").tolist(), pd.Series(["ab"]).str.center(6, "*").tolist())
print(names.str.split().explode().tolist(), len(names.str.split().explode()))

# Extracting with regular expressions
log = pd.Series(["2026-11-15 10:00:00 ERROR disk full code=42", "2026-11-15 10:05:10 INFO started", "2026-11-15 10:07:00 WARN low battery code=7", None])
parsed = log.str.extract(r"^(?P<date>\S+) (?P<time>\S+) (?P<level>[A-Z]+) (?P<message>.*?)(?: code=(?P<code>\d+))?$")
print(parsed)
print(parsed["code"].astype(float).tolist(), parsed["level"].value_counts().sort_index().to_dict())
print(log.str.extract(r"code=(\d+)").iloc[:, 0].tolist(), log.str.extract(r"code=(\d+)", expand=False).tolist())
print(log.str.findall(r"\d+").str.len().tolist(), log.str.contains("ERROR|WARN").tolist())
print(log.str.extractall(r"(?P<n>\d+)").loc[0, "n"].tolist()[:4], log.str.extractall(r"(?P<n>\d+)").shape)
print(pd.to_datetime(parsed["date"] + " " + parsed["time"]).dt.minute.tolist())
print(log.str.count(r"\d").tolist(), log.str.split(" ", n=2).str[2].tolist()[0])

# Unicode, and other helpers
accents = pd.Series(["café", "NAÏVE"])
print(accents.str.normalize("NFKD").str.encode("ascii", errors="ignore").str.decode("ascii").tolist(), accents.str.casefold().tolist(), accents.str.len().tolist())
print(pd.Series(["a|b", "b|c", "a"]).str.get_dummies(sep="|").values.tolist(), pd.Series(["a|b", "b|c", "a"]).str.get_dummies(sep="|").columns.tolist())
print(pd.Series(["abc"]).str.translate(str.maketrans("abc", "xyz")).tolist(), pd.Series(["é"]).str.encode("utf-8").tolist())

# Labels of rows and columns
table = pd.DataFrame({"First Name": ["a"], "Last-Name": ["b"], " Age ": [1]}, index=["Row 1"])
table.columns = table.columns.str.strip().str.lower().str.replace(r"[ -]+", "_", regex=True)
print(table.columns.tolist(), table.index.str.upper().tolist(), pd.Index(["x1", "x2"]).str.replace("x", "col_").tolist())

# Cleaning a column of labels, step by step
raw = pd.Series([" Cat", "dog ", "CAT", "Dog!", "bird", "cat ", None, "d0g"])
cleaned = raw.str.strip().str.lower().str.replace(r"[^a-z]", "", regex=True)
print(cleaned.tolist(), cleaned.value_counts().sort_index().to_dict(), cleaned.isna().sum())
fixed = cleaned.replace({"dg": "dog"})
print(fixed.value_counts().sort_index().to_dict(), fixed.fillna("unknown").unique().tolist())

# Speed and types: .str is a Python loop under the hood; text columns have the "str" dtype
print(s.dtype, s.str.len().dtype, s.str.contains("a").dtype, s.isna().sum(), re.compile(r"\d+").findall("a1b22"))

# EXPECTED OUTPUT
# ['Ann Lee', 'bo-xu', nan, 'CY Ray', 'd.i']
# ['  ann lee ', 'bo-xu', nan, 'cy ray', 'd.i'] ['  ANN LEE ', 'BO-XU', nan, 'CY RAY', 'D.I'] ['Ann Lee', 'Bo-Xu', nan, 'Cy Ray', 'D.I'] ['Ann lee', 'Bo-xu', nan, 'Cy ray', 'D.i'] cy rAY
# [10.0, 5.0, nan, 6.0, 3.0] [7.0, 5.0, nan, 6.0, 3.0] [0.0, 1.0, nan, 0.0, 0.0] [7.0, -1.0, nan, -1.0, -1.0]
# [False, False, False, True, False] [False, False, False, True, False] [True, True, False, False, False]
# [False, True, False, False, False] [False, False, False, False, True] [False, False, False, True, False]
# [True, False, True, False, False] ['bo-xu', 'd.i']
# [False, False, True, True] [False, True, False, False] [False, False, False, True]
# [True, False, False, False, False] [False, False, False, False, True]
# ['a_b_c', 'x.y.z', '1 2  3', 'Hello World'] ['a-b-c', 'x_y_z', '1 2  3', 'Hello World'] _____
# 1 2 3 # #  # Bye World
# b-a-c HellO WOrld
# ['name', 'name_suf'] ['pre_name', 'name']
# [['Ann', 'Lee'], ['Bo', 'Xu', 'Jr'], ['Cy']] [['Ann', 'Lee'], ['Bo', 'Xu Jr'], ['Cy']] [2, 3, 1]
#      0    1    2
# 0  Ann  Lee  NaN
# 1   Bo   Xu   Jr
# 2   Cy  NaN  NaN
# [['Ann', 'Lee'], ['Bo', 'Xu Jr'], ['Cy', nan]]
# ['Ann', 'Bo', 'Cy'] ['Lee', 'Jr', 'Cy'] ['Ann', 'Bo Xu', 'Cy']
# ['An', 'Bo', 'Cy'] ['nn ', 'o X', 'y'] ['Ann', 'Bo ', 'Cy'] ['ee', 'Jr', 'Cy']
# [['Ann', ' ', 'Lee'], ['Bo', ' ', 'Xu Jr'], ['Cy', '', '']]
# Ann Lee; Bo Xu Jr; Cy ['Ann Lee-x', 'Bo Xu Jr-y', 'Cy-z'] ['Ann Lee!', 'Bo Xu Jr?', 'Cy.']
# CyCy ['0007', '0042'] ['....ab'] ['**ab**']
# ['Ann', 'Lee', 'Bo', 'Xu', 'Jr', 'Cy'] 6
#          date      time  level      message code
# 0  2026-11-15  10:00:00  ERROR    disk full   42
# 1  2026-11-15  10:05:10   INFO      started  NaN
# 2  2026-11-15  10:07:00   WARN  low battery    7
# 3         NaN       NaN    NaN          NaN  NaN
# [42.0, nan, 7.0, nan] {'ERROR': 1, 'INFO': 1, 'WARN': 1}
# ['42', nan, '7', nan] ['42', nan, '7', nan]
# [7.0, 6.0, 7.0, nan] [True, False, True, False]
# ['2026', '11', '15', '10'] (20, 1)
# [0.0, 5.0, 7.0, nan]
# [16.0, 14.0, 15.0, nan] ERROR disk full code=42
# ['cafe', 'NAIVE'] ['café', 'naïve'] [4, 5]
# [[1, 1, 0], [0, 1, 1], [1, 0, 0]] ['a', 'b', 'c']
# ['xyz'] [b'\xc3\xa9']
# ['first_name', 'last_name', 'age'] ['ROW 1'] ['col_1', 'col_2']
# ['cat', 'dog', 'cat', 'dog', 'bird', 'cat', nan, 'dg'] {'bird': 1, 'cat': 3, 'dg': 1, 'dog': 2} 1
# {'bird': 1, 'cat': 3, 'dog': 3} ['cat', 'dog', 'bird', 'unknown']
# str float64 bool 1 ['1', '22']