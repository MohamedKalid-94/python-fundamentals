from array import array
from bisect import bisect_left, insort

# An array has NO sort() method.

a = array("i", [3, 1, 4, 1, 5])

# 1. sorted() returns a LIST
print(sorted(a))                            # [1, 1, 3, 4, 5]
print(sorted(a, reverse=True))              # [5, 4, 3, 1, 1]

# 2. Wrap it to get an array
print(array("i", sorted(a)))                # array('i', [1, 1, 3, 4, 5])

# 3. Sort IN PLACE: replace the contents
a[:] = array("i", sorted(a))
print(a)                                    # array('i', [1, 1, 3, 4, 5])

# 4. key= works as usual
print(sorted(array("i", [-3, 1, -2]), key=abs))     # [1, -2, -3]

# 5. A hand-written in-place sort (insertion sort, as you would write it in C)
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

data = array("i", [5, 2, 9, 1, 5, 6])
insertion_sort(data)
print(data)                                 # array('i', [1, 2, 5, 5, 6, 9])

# 6. Check that an array is sorted
def is_sorted(arr):
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))

print(is_sorted(data), is_sorted(array("i", [2, 1])))       # True False

# 7. Binary search and sorted insertion work on sorted arrays (module bisect)
print(bisect_left(data, 5))                 # 2        position of the first 5
s = array("i", [1, 3, 5])
insort(s, 4)
print(s)                                    # array('i', [1, 3, 4, 5])

# 8. Largest and smallest
print(max(data), min(data))                 # 9 1

# For big numeric data, NumPy's sort is much faster than sorted().