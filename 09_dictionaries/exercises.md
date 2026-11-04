Write the questions as # comments and your solutions as code below each one.

Create a dictionary for yourself with name, age, city and skills (a list). Print each value with [], then use get for a key that does not exist with a default.
Show the difference between d["missing"], d.get("missing") and d.setdefault("missing", 0), and what each one does to the dictionary.
Add three keys in three different ways ([], update, |=), change one value, and remove one key with pop, del and popitem. Print the dictionary after each step.
Count how many times each character appears in "mississippi", then print the characters sorted by count (highest first).
Count the words of a paragraph, ignoring case and punctuation, and print the top 3 with sorted and then with Counter.most_common.
Write invert(d) that swaps keys and values. Then write a second version that works when values repeat, by collecting the keys in a list.
Merge {"a": 1, "b": 2} and {"b": 3, "c": 4} in three ways ({**}, |, update on a copy), then merge them again adding the values of shared keys.
Given scores = {"Ann": 90, "Bob": 75, "Cy": 82, "Di": 75}, print the highest and lowest scorer, the average, the names above the average, and the ranking with ties sorted by name.
Build a dictionary of lists that groups the numbers 1 to 20 by remainder when divided by 3, once with setdefault and once with defaultdict.
Group ["tea", "eat", "tan", "ate", "nat", "bat"] into anagram groups.
Write two_sum(nums, target) that returns the two indexes with one pass and a dictionary. Test it with [3, 2, 4] and target 6 (the answer is (1, 2)).
Show the fromkeys trap: create dict.fromkeys(["a", "b"], []), append to one value, and print both. Then fix it with a comprehension.
Show that a list cannot be a key but a tuple can, and use (row, col) tuples as keys to store a small 3x3 board. Print the board with nested loops.
Loop over a dictionary in four ways (keys, values, items, sorted by value), and show the RuntimeError when you delete keys while looping, then fix it.
Use keys() views as sets: given two dictionaries of stock levels, print the products only in the first, only in the second, in both, and the ones whose quantity differs.
Copy a nested dictionary three ways (assignment, copy, deepcopy), change a nested list, and print which copies were affected.
Create a nested dictionary of 3 students with marks in 3 subjects. Print each student’s total and average, the topper, and the subject with the highest class average.
Write deep_get(data, path, default) and deep_set(data, path, value) that create missing levels as needed. Test them on an empty dictionary.
Convert a nested dictionary to JSON text with indent=2, parse it back with json.loads, and check that the result equals the original.
Build a dispatch table of four functions (add, sub, mul, div) and use it for a calculator that reads "8 / 2" from input(). Handle an unknown operator and division by zero.
Parse "TEMP=36.5;HUM=40;STATE=OK" into a dictionary, convert the numeric values to numbers, and print a formatted report. Then do the reverse: build the text from the dictionary.
Write a memoized fib(n) with a dictionary, and count how many times the function body really runs for fib(30) with and without the cache.
Predict first, then run, and explain each result in a comment:
python
a = {"x": [1], "y": 2}
b = a.copy()
b["x"].append(9)
b["y"] = 99
print(a, b)

d = {1: "a", 1.0: "b", True: "c"}
print(d, len(d))

print({"a": 1} | {"a": 2}, {"a": 1, "b": 2} == {"b": 2, "a": 1})
print(list({"z": 1, "a": 2}), "a" in {"a": 0}, 0 in {"a": 0})

e = {"k": 1}
print(e.setdefault("k", 5), e.setdefault("m", 5), e)
print(e.pop("zzz", "none"), e.get("zzz"), len(e))