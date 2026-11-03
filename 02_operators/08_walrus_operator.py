# := assigns a value AND returns it, inside an expression (Python 3.8+)

# Without walrus: two steps
words = ["python", "is", "fun"]
count = len(words)
if count > 2:
    print(f"{count} words")           # 3 words

# With walrus: one step
if (count := len(words)) > 2:
    print(f"{count} words")           # 3 words

# It works anywhere an expression works
print((y := 10) + 5)                  # 15
print(y)                              # 10

# In a comprehension: compute once, use twice
numbers = [1, 4, 9, 16, 25]
result = [root for n in numbers if (root := n ** 0.5) > 2]
print(result)                         # [3.0, 4.0, 5.0]

# In a while loop (loops are covered in Module 03; just read it for now)
count = 0
while (count := count + 1) < 4:
    print("round", count)
# round 1
# round 2
# round 3

# RULES
# 1. A bare "x := 5" as a statement is a SyntaxError.  Use parentheses: (x := 5)
# 2. Use "=" for normal assignment, ":=" only when you need the value right there.
# 3. Do not overuse it; readability comes first.
# 4. "if x = 5:" is a SyntaxError. "if x := 5:" is legal but means "assign, then test".