# 1. Remove duplicates from a list
items = [3, 1, 3, 2, 1]
print(sorted(set(items)))                       # [1, 2, 3]          sets lose the order
print(list(dict.fromkeys(items)))               # [3, 1, 2]          keeps the order

# 2. Does a list contain duplicates?
def has_duplicates(items):
    return len(set(items)) != len(items)

print(has_duplicates([1, 2, 3, 2]), has_duplicates([1, 2, 3]))      # True False

# 3. Common items, and items only in the first list
a, b = [1, 2, 3, 4], [3, 4, 5]
print(sorted(set(a) & set(b)))                  # [3, 4]
print(sorted(set(a) - set(b)))                  # [1, 2]
print(sorted(set(a) ^ set(b)))                  # [1, 2, 5]

# 4. Unique characters
print(len(set("mississippi")), sorted(set("mississippi")))          # 4 ['i', 'm', 'p', 's']

# 5. Pangram: does the text use every letter?
def is_pangram(text):
    return set("abcdefghijklmnopqrstuvwxyz") <= set(text.lower())

print(is_pangram("The quick brown fox jumps over the lazy dog"), is_pangram("hello"))
# True False

# 6. Why a set is NOT enough for anagrams (a set forgets the counts)
print(set("aab") == set("abb"), sorted("aab") == sorted("abb"))     # True False

# 7. First duplicate in a list
def first_duplicate(items):
    seen = set()
    for x in items:
        if x in seen:
            return x
        seen.add(x)
    return None

print(first_duplicate([2, 5, 3, 5, 2]), first_duplicate([1, 2, 3]))    # 5 None

# 8. Is there a pair that adds up to the target? (one pass with a set)
def has_pair(nums, target):
    seen = set()
    for n in nums:
        if target - n in seen:
            return True
        seen.add(n)
    return False

print(has_pair([2, 7, 11, 15], 9), has_pair([1, 2], 10))            # True False

# 9. Longest run of consecutive numbers
def longest_consecutive(nums):
    s = set(nums)
    best = 0
    for n in s:
        if n - 1 not in s:                      # n starts a run
            length = 1
            while n + length in s:
                length += 1
            best = max(best, length)
    return best

print(longest_consecutive([100, 4, 200, 1, 3, 2]))                  # 4

# 10. Words shared by two texts
text1, text2 = "the cat sat", "the dog sat"
print(sorted(set(text1.split()) & set(text2.split())))             # ['sat', 'the']
print(len(set(text1.split()) | set(text2.split())))                # 4

# 11. Permission check with subsets
granted = {"read", "write", "admin"}
print({"read", "write"} <= granted, {"read", "delete"} <= granted)  # True False

# 12. Missing numbers in a range
print(set(range(1, 6)) - {1, 3, 5})             # {2, 4}

# 13. Filter a list with a blacklist (a set makes each check fast)
blocked = {"bad", "evil"}
print([w for w in ["a", "bad", "b", "evil"] if w not in blocked])   # ['a', 'b']

# 14. Similarity of two groups (Jaccard)
x, y = {1, 2, 3, 4}, {3, 4, 5, 6}
print(round(len(x & y) / len(x | y), 2))        # 0.33

# 15. Embedded-style: which devices are missing or unexpected?
connected = {"sensorA", "sensorB", "sensorC"}
expected = {"sensorA", "sensorB", "sensorD"}
print(expected - connected)                     # {'sensorD'}     missing
print(connected - expected)                     # {'sensorC'}     unexpected