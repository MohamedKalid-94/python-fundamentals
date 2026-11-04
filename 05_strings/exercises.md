Write the questions as # comments and your solutions as code below each one.

Store your name and age, and print a sentence with them using an f-string, with a + concatenation, and with .format().
For "Python", print the first character, the last character, the middle two characters, every second character, and the reversed string.
Given email = "sam.lee@example.com", extract the username and the domain, first with slicing and find, then with partition.
Count the vowels and consonants in a sentence (ignore spaces and punctuation).
Check whether a string is a palindrome, ignoring case, spaces and punctuation. Test with "Was it a car or a cat I saw?".
Write your own title_case(text) without using .title().
Replace every run of whitespace in " too many spaces " with a single space, using split() and join().
Check whether a string is a valid variable name: it must not start with a digit, and may contain only letters, digits and underscores. Test it with "my_var", "2fast", "bad-name" and "".
Print a receipt with three items using f-string alignment, so the columns line up and the total is shown with two decimals and thousands separators.
Convert "hello_world_example" (snake_case) to "helloWorldExample" (camelCase), then convert it back.
Count how often each word appears in "the cat and the hat and the bat" and print the result sorted by count (highest first).
Find the longest and the shortest word in a sentence.
Reverse each word in a sentence in place ("hello world" becomes "olleh dlrow"), then reverse the word order instead ("world hello").
Validate a password: at least 8 characters, with an uppercase letter, a lowercase letter and a digit. Print every rule that fails.
Show only the last 4 characters of an ID and mask the rest with *.
Check whether two strings are anagrams, ignoring case and spaces.
Find the first non-repeating character in a string, or print None if there isn’t one.
Decode a run-length string: "a3b2c1" becomes "aaabbc".
Parse "TEMP=36.5;HUM=40;STATE=OK" into a dictionary, convert the temperature to Fahrenheit, and print a one-line report with the values formatted to one decimal.
For b"Hello", print each byte as a two-digit hex value and as an 8-bit binary value, one line per byte.
Write a Caesar cipher with shift 5 that encodes and decodes, and leaves non-letters unchanged.
Predict first, then run, and explain each result in a comment:
python
print("abc" * 2 + "d"[::-1])
print("a,b,,c".split(","))
print("a b c".split(" ", 1))
print("hello"[1:-1][::-1])
print("  x ".strip() == "x")
print("Python"[10:] == "")