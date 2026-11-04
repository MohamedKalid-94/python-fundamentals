Write the questions as # comments and your solutions as code below each one.

Create a set from [5, 3, 5, 1, 3, 9]. Print its length, and print the sorted items.
Show that {} creates a dictionary, and create an empty set the correct way.
Show that a list cannot go into a set but a tuple can, and explain why in a comment.
Add one item with add, several with update, then show the difference between add("hello") and update("hello").
Remove an item with remove, with discard and with pop. Show the error that remove raises for a missing item and explain why discard is safer.
Given a = {1, 2, 3, 4, 5} and b = {4, 5, 6, 7}, print the union, intersection, both differences and the symmetric difference, using operators first and methods second.
Check whether {1, 2} is a subset of a, whether a is a superset of {1, 2}, and whether a and {8, 9} are disjoint.
Remove duplicates from ["b", "a", "b", "c", "a"] in two ways: one that loses the order and one that keeps it.
Write common_items(list1, list2) that returns the sorted common items of two lists.
Find the students who are in both the Python class and the SQL class, only in Python, only in SQL, and in exactly one class (use sets of names).
Write is_pangram(text) and is_isogram(word) (no repeated letters).
Count how many unique words a sentence has, ignoring case and punctuation ("The cat. The hat! the BAT" has 3).
Find the numbers from 1 to 20 that are missing from [2, 4, 6, ..., 20, 7, 13], using a set difference.
Write first_duplicate(items) and all_duplicates(items) using a set of seen items.
Write longest_consecutive(nums) and test it with [10, 5, 12, 3, 55, 30, 4, 11, 2] (the answer is 4: 2, 3, 4, 5).
Remove the items of a blocklist from a list of words, with a set for the blocklist, and compare it with using a list for the blocklist on a large input (use time.perf_counter() to measure both).
Use a set as a dictionary key by using frozenset. Show that {frozenset({1, 2}): "x"} works and explain why {{1, 2}: "x"} fails.
Model device permissions with sets: define READ, WRITE and ADMIN roles, then write can(user_perms, required) that returns True only when all the required permissions are present.
Re-implement the same permission check using a bitmask with |, & and ~ (your embedded way), and compare it with the set version in a comment.
Predict first, then run, and explain each result in a comment:
python
a = {1, 2, 3}
b = a
b.add(4)
c = a.copy()
c.discard(1)
print(a, c, a is b, a is c)

print({1, 2} | {2, 3} & {3, 4})
print(({1, 2} | {2, 3}) & {3, 4})
print({1, 2, 3} - {2} == {1, 3}, {1, 2} < {1, 2})
print(len({1, 1.0, True, "1"}), type({}), type(set()))
print(sorted({"b": 1, "a": 2}), set("aab") == set("abb"))