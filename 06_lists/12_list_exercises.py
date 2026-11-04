# 1. Sum, average, min and max
data = [4, 8, 15, 16, 23, 42]
print(sum(data), sum(data) / len(data), min(data), max(data))   # 108 18.0 4 42

# 2. Second largest value
def second_largest(nums):
    unique = sorted(set(nums))
    return unique[-2] if len(unique) >= 2 else None

print(second_largest([10, 20, 20, 5]), second_largest([5]))     # 10 None

# 3. Remove duplicates and keep the order
print(list(dict.fromkeys([3, 1, 3, 2, 1])))                     # [3, 1, 2]

# 4. Reverse a list in place without .reverse() (two pointers)
def reverse_in_place(items):
    left, right = 0, len(items) - 1
    while left < right:
        items[left], items[right] = items[right], items[left]
        left += 1
        right -= 1

values = [1, 2, 3, 4, 5]
reverse_in_place(values)
print(values)                                                   # [5, 4, 3, 2, 1]

# 5. Rotate left by k positions
def rotate_left(items, k):
    if not items:
        return items
    k %= len(items)
    return items[k:] + items[:k]

print(rotate_left([1, 2, 3, 4, 5], 2))                          # [3, 4, 5, 1, 2]

# 6. Flatten a list of lists
print([v for row in [[1, 2], [3], [4, 5, 6]] for v in row])     # [1, 2, 3, 4, 5, 6]

# 7. Count how often each item appears
counts = {}
for item in ["a", "b", "a", "c", "b", "a"]:
    counts[item] = counts.get(item, 0) + 1
print(counts)                                                   # {'a': 3, 'b': 2, 'c': 1}

# 8. Two sum: indexes of two numbers that add up to the target
def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return i, j
    return None

print(two_sum([2, 7, 11, 15], 9), two_sum([1, 2], 10))          # (0, 1) None

# 9. Split a list into chunks
def chunk(items, size):
    return [items[i:i + size] for i in range(0, len(items), size)]

print(chunk([1, 2, 3, 4, 5, 6, 7], 3))                          # [[1, 2, 3], [4, 5, 6], [7]]

# 10. Merge two sorted lists
def merge_sorted(a, b):
    result = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1
    result.extend(a[i:])
    result.extend(b[j:])
    return result

print(merge_sorted([1, 4, 7], [2, 3, 9, 10]))                   # [1, 2, 3, 4, 7, 9, 10]

# 11. Moving average of sensor readings (window of 3)
readings = [20, 22, 21, 25, 30, 28]
print([round(sum(readings[i:i + 3]) / 3, 2) for i in range(len(readings) - 2)])
# [21.0, 22.67, 25.33, 27.67]

# 12. Balanced brackets with a list used as a stack
def is_balanced(text):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in text:
        if ch in "([{":
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack

print(is_balanced("{[()]}"), is_balanced("([)]"), is_balanced("(("))   # True False False

# 13. Remove every occurrence IN PLACE (all names see the change)
nums = [1, 2, 3, 2]
alias = nums
nums[:] = [n for n in nums if n != 2]
print(alias)                                                    # [1, 3]

# 14. Sort by length, then alphabetically
words = ["pear", "fig", "apple", "kiwi", "date"]
print(sorted(words, key=lambda w: (len(w), w)))
# ['fig', 'date', 'kiwi', 'pear', 'apple']