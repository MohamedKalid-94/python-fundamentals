# if / else: exactly one of two paths
number = 7
if number % 2 == 0:
    print("even")
else:
    print("odd")                # odd

# if / elif / else: exactly one of many paths
for marks in [95, 80, 72, 40]:
    if marks >= 90:
        grade = "A"
    elif marks >= 75:
        grade = "B"
    elif marks >= 60:
        grade = "C"
    else:
        grade = "F"
    print(f"{marks} -> {grade}")
# 95 -> A
# 80 -> B
# 72 -> C
# 40 -> F

# Only the FIRST true branch runs; the rest are skipped
x = 10
if x > 5:
    print("big")                # big
elif x > 1:
    print("medium")             # skipped, even though x > 1 is also true
else:
    print("small")

# ORDER MATTERS: put the most specific condition first
marks = 95
if marks >= 60:                 # wrong order
    print("C")                  # C   (95 should be an A)
elif marks >= 90:
    print("A")                  # never reached

# Conditional expression (ternary): one line, produces a value
age = 16
status = "adult" if age >= 18 else "minor"
print(status)                   # minor

# Rules
# - "elif" is the keyword (not "else if")
# - "else" never has a condition
# - "else" must come last