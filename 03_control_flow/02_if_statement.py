temperature = 35

if temperature > 30:
    print("It's hot")           # inside the block
    print("Drink water")        # inside the block
print("Done")                   # outside: always runs

# A false condition skips the whole block
if temperature > 40:
    print("This never prints")
print("After the second if")

# The condition can be ANY expression
age = 20
if age >= 18:
    print("adult")              # adult

items = []
if not items:
    print("list is empty")      # list is empty

name = "Sam"
if name:                        # non-empty string is truthy
    print("hello", name)        # hello Sam

if "a" in "cat":
    print("found a")            # found a

x = 5
if 1 < x < 10:                  # chained comparison
    print("x is between 1 and 10")

# One-line form (fine for very short bodies)
if x > 0: print("positive")

# Style rules
# - Write "if flag:" not "if flag == True:"
# - Write "if items:" not "if len(items) > 0:"
# - Test None with "is None"

# Common errors (do not run these)
# if x = 5:        -> SyntaxError (= is assignment, == is comparison)
# if x == 5        -> SyntaxError (missing colon)
# an empty block   -> IndentationError (use pass, see 12_pass_statement.py)