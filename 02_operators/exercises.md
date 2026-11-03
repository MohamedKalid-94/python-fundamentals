exercises.py

Write your solutions under each question as code, and put the question itself in # comments (as you did in Module 01).

For a = 47 and b = 6, print + - * / // % ** and divmod. Predict -47 // 6 and -47 % 6 first.
Check the identity a == (a // b) * b + a % b for 3 pairs, including negative numbers.
Convert 3725 seconds into hours, minutes and seconds using only // and % (or divmod).
Check whether a number is in the range 18 to 65 using one chained comparison, and test it with 17, 18, 65 and 66.
Predict first, then run: 5 == 5.0, "a" < "B", [1, 2] < [1, 3], (1, 2) == [1, 2], 0.1 + 0.2 == 0.3.
Show that += on a list keeps the same id, but += on a string does not. Explain why in a comment.
Show the alias trap: b = a; b += [3] changes a, but b = b + [3] does not.
Predict first, then run: 0 or "x", "" and 5, None or [] or 7, 1 and 2 and 3, not [].
Write a default-name pattern with or, then show where it goes wrong when the input is a valid 0.
For x = 0b10110100, print it in 8-bit binary and do: set bit 0, clear bit 2, toggle bit 7, test bit 4. Print the result after each step with f"{x:08b}".
Print ~x & 0xFF for x = 0b10110100, and explain in a comment why you need the mask.
Write one expression that tells whether a number is odd or even using &. Test it with 0, 7, 10 and -3.
Check "admin" in ... for a list, a set and a dict. For the dict, show the three different checks (keys, values, items).
Show == vs is with two equal lists, and explain why x is None is preferred over x == None.
Use := in an if and in a list comprehension to avoid computing len(...) or n ** 0.5 twice.
Predict first, then run: 2 ** 3 ** 2, -3 ** 2, 10 - 2 - 3, 1 + 2 << 3, 5 & 1 == 0, not 1 == 2, 1 or 0 and 0. Rewrite each one with parentheses to show your reading.