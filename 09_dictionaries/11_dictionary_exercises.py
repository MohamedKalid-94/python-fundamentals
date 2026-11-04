import json
from collections import Counter

# 1. Count the characters of a string
freq = {}
for ch in "banana":
    freq[ch] = freq.get(ch, 0) + 1
print(freq)                                     # {'b': 1, 'a': 3, 'n': 2}

# 2. Word frequency, highest count first (ties alphabetical)
text = "the cat and the hat and the bat"
counts = {}
for word in text.split():
    counts[word] = counts.get(word, 0) + 1
print(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])))
# [('the', 3), ('and', 2), ('bat', 1), ('cat', 1), ('hat', 1)]

# 3. Invert a dictionary (values must be unique and hashable)
print({v: k for k, v in {"a": 1, "b": 2}.items()})      # {1: 'a', 2: 'b'}

# 4. Group words by first letter
groups = {}
for w in ["apple", "banana", "avocado"]:
    groups.setdefault(w[0], []).append(w)
print(groups)                                   # {'a': ['apple', 'avocado'], 'b': ['banana']}

# 5. Merge two dictionaries and add the values of shared keys
a, b = {"x": 1, "y": 2}, {"y": 3, "z": 4}
merged = dict(a)
for k, v in b.items():
    merged[k] = merged.get(k, 0) + v
print(merged)                                   # {'x': 1, 'y': 5, 'z': 4}

# 6. Two sum with a dictionary: indexes of two numbers that add up to the target
def two_sum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return seen[target - n], i
        seen[n] = i
    return None

print(two_sum([2, 7, 11, 15], 9), two_sum([1, 2], 10))  # (0, 1) None

# 7. Group anagrams
groups = {}
for w in ["eat", "tea", "tan", "ate", "nat", "bat"]:
    groups.setdefault("".join(sorted(w)), []).append(w)
print(list(groups.values()))                    # [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]

# 8. Most frequent word
print(max(counts, key=counts.get))              # the

# 9. Ranking, best score, average
scores = {"Ann": 90, "Bob": 75, "Cy": 82}
print(sorted(scores, key=scores.get, reverse=True))     # ['Ann', 'Cy', 'Bob']
print(max(scores, key=scores.get))                      # Ann
print(round(sum(scores.values()) / len(scores), 2))     # 82.33

# 10. Drop the keys whose value is None
raw = {"a": 1, "b": None, "c": 3}
print({k: v for k, v in raw.items() if v is not None})  # {'a': 1, 'c': 3}

# 11. Defaults plus user settings
defaults = {"baud": 9600, "parity": "N"}
user = {"baud": 115200}
print(defaults | user)                          # {'baud': 115200, 'parity': 'N'}

# 12. Lookup table and dispatch table (embedded style)
ERROR_CODES = {0: "OK", 1: "TIMEOUT", 2: "CRC_FAIL"}
print(ERROR_CODES.get(2, "UNKNOWN"), ERROR_CODES.get(9, "UNKNOWN"))     # CRC_FAIL UNKNOWN

def add(x, y):
    return x + y

def sub(x, y):
    return x - y

ops = {"add": add, "sub": sub}
print(ops["add"](2, 3), ops["sub"](2, 3))       # 5 -1

# 13. Parse key=value text into a dictionary
line = "TEMP=36.5;HUM=40;STATE=OK"
print(dict(pair.split("=") for pair in line.split(";")))
# {'TEMP': '36.5', 'HUM': '40', 'STATE': 'OK'}

# 14. Counter: a dictionary made for counting
print(Counter("banana").most_common(2))         # [('a', 3), ('n', 2)]

# 15. JSON round trip
as_text = json.dumps({"a": 1, "b": [1, 2]})
print(as_text)                                  # {"a": 1, "b": [1, 2]}
print(json.loads(as_text))                      # {'a': 1, 'b': [1, 2]}

# 16. Memoization: a dictionary as a cache
memo = {}
def fib(n):
    if n in memo:
        return memo[n]
    memo[n] = n if n < 2 else fib(n - 1) + fib(n - 2)
    return memo[n]

print(fib(30))                                  # 832040