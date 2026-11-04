Write the questions as # comments and your solutions as code below each one.

Create a tuple of 6 numbers. Print the first, the last, the middle two, every second item, and the reversed tuple.
Create a single-item tuple and show with type() that (7) and (7,) are different.
Show that a tuple cannot be changed, then “update” it three ways: replace one item, add an item, and remove an item (use a list and slicing).
Write stats(numbers) that returns the minimum, maximum and average as one tuple, and unpack the result into three variables.
Use star unpacking to get the first, the last and the middle items of (10, 20, 30, 40, 50).
Swap three variables in a rotation (a, b, c = b, c, a) in one line and explain the result.
Given records = (("Ann", 30), ("Bob", 25), ("Cy", 35)), print each record with a loop that unpacks it, then print the oldest person with max(..., key=...).
Sort [("Cy", 90), ("Ann", 90), ("Bob", 85)] by score (highest first), with ties broken by name.
Build a dictionary that uses (row, col) tuples as keys for a 3x3 board. Put "X" at (1, 1) and "O" at (0, 2), then print the board with nested loops.
Given names = ("Ann", "Bob", "Cy") and scores = (90, 85, 70), build a tuple of (name, score) pairs with zip, then unzip it back into two tuples.
Join two tuples, remove the duplicates while keeping the order, and print the result as a tuple.
Flatten ((1, 2), (3,), (4, 5, 6)) into one tuple.
Show that a tuple holding a list can change, and reproduce the t[0] += [5] quirk. Explain in a comment why the list changes even though an error is raised.
Show that {(1, 2): "a"} works but {(1, [2]): "a"} raises an error, and explain why.
Create a namedtuple called Reading with sensor, value and unit. Make 4 readings, print them, sort them by value, and use _replace to change one unit.
Create a namedtuple for a 3D point with a default z of 0. Write a function that returns the distance between two points.
Convert (255, 128, 0) to a hex colour string, then convert "#1e90ff" back to an (r, g, b) tuple.
Write is_sorted(t) and is_palindrome(t) for tuples, and test both on tuples of numbers and of strings.
Use tuples to implement a tiny state machine: keep the transitions in a dictionary with (state, event) keys, for example ("IDLE", "start") giving "RUNNING", and run a list of events through it.
Predict first, then run, and explain each result in a comment:
python
t = (1, 2, 3)
print(t + (4,), t * 2, t[::-1], t[1:], t[5:])
print((1, 2) < (1, 2, 0), (2,) > (1, 99), () == tuple())
a = (1, [2, 3])
a[1].append(4)
print(a, len(a))
x, *y, z = "hello"
print(x, y, z)
print(type((1)), type((1,)), type(()))