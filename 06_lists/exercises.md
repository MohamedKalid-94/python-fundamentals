Write the questions as # comments and your solutions as code below each one.

Create a list of 5 numbers. Print the first, the last, the middle one, the first three, the last three, and the list reversed.
Add 99 at the end, 0 at the start, and 50 at position 3. Then extend the list with [7, 8]. Print the list after each step.
Remove the first 99, pop the last item, and delete the first two items with del. Print the list and the popped value.
Given [5, 3, 8, 3, 1, 3], print how many times 3 appears, the index of the first 3, and the list with every 3 removed.
Read numbers from one line of input ("4 8 15 16") into a list of integers, and print the sum, average, minimum and maximum.
Write second_smallest(nums) that works when there are duplicates ([4, 1, 1, 3] gives 3), and returns None when there is no second value.
Create a list of squares of the odd numbers from 1 to 15 with a list comprehension. Then rewrite it with a normal loop.
From ["apple", "Banana", "cherry", "date"] build a list of the words longer than 4 letters, in uppercase, using a comprehension.
Create a 3x4 grid of zeros the correct way, set the cell in row 1, column 2 to 5, and print the grid. Then show what goes wrong with [[0] * 4] * 3.
Flatten [[1, 2], [3, 4, 5], [6]], then transpose [[1, 2, 3], [4, 5, 6]], both with comprehensions.
Sort ["banana", "Apple", "cherry", "apple"] three ways: default, case-insensitive, and by length then alphabetically.
Given a list of (name, score) tuples, print the ranking: highest score first, ties sorted by name. Use enumerate to print the rank numbers.
Show that b = a shares a list, then show that a.copy() does not. Then build a nested list and show where a shallow copy fails and deepcopy works.
Write remove_all(items, value) that removes every occurrence in place (the caller’s list must change), without the skipping bug.
Write rotate_right(items, k) and test it with k larger than the list length and with an empty list.
Merge two lists into one without duplicates, in three ways: keeping the order, sorted, and only the items that appear in both lists.
Write chunk(items, size) and use it to split 10 sensor readings into groups of 4, with the last group shorter.
Compute a moving average with a window of 4 over 10 sensor readings, rounded to 1 decimal.
Use a list as a stack to reverse a string, then to check that "{[()]}", "([)]" and "((" are balanced or not.
Write bubble_sort(items) that sorts a list in place using nested loops and a swap (no sort()). Test it on [5, 2, 9, 1, 5, 6].
Find all pairs in [1, 2, 3, 4, 5, 6] whose sum is 7, without printing the same pair twice.
Predict first, then run, and explain each result in a comment:
python
a = [1, 2, 3]
b = a
b += [4]
c = a + [5]
print(a, b, c, a is b, a is c)

x = [[1], [2]]
y = x[:]
y[0].append(9)
y.append([3])
print(x, y)

print([1, 2, 3][::-1][0], [1, 2, 3][5:], [0] * 3 + [1])
nums = [3, 1, 2]
print(nums.sort(), nums)