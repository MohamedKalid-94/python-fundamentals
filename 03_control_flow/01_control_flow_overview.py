# Normal flow: top to bottom, one statement at a time
print("step 1")
print("step 2")
print("step 3")

# Control flow lets you change that order. There are three kinds:
#   1. Sequential : the default, line by line
#   2. Decision   : if / elif / else / match   (choose a path)
#   3. Repetition : for / while                 (repeat a block)

# Blocks are defined by a COLON and INDENTATION (4 spaces), not braces.
#
#   if condition:        <- colon ends the header line
#       statement        <- indented = inside the block
#   statement            <- not indented = outside the block
#
# Wrong indentation raises IndentationError.

# Every condition is judged by truthiness (see Module 01)
# (a for loop is used here as a preview; loops are covered below)
for value in [0, 1, "", "hi", [], [0], None]:
    if value:
        print(repr(value), "-> truthy")
    else:
        print(repr(value), "-> falsy")