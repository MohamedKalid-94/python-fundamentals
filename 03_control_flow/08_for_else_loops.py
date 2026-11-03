# The else block of a loop runs ONLY if the loop finished WITHOUT hitting break.
# Think of it as "no break".

# No even number, so the loop is never broken, so else runs
for n in [1, 3, 5]:
    if n % 2 == 0:
        print("found even", n)
        break
else:
    print("no even number found")      # no even number found

# An even number exists, so break happens, so else is skipped
for n in [1, 2, 5]:
    if n % 2 == 0:
        print("found even", n)         # found even 2
        break
else:
    print("no even number found")

# Search pattern
names = ["amy", "bob", "carol"]
target = "dave"
for name in names:
    if name == target:
        print("found", name)
        break
else:
    print(target, "not found")         # dave not found

# Prime numbers (classic use)
for num in range(2, 12):
    for d in range(2, num):
        if num % d == 0:
            break                      # divisor found, not prime
    else:
        print(num, "is prime")
# 2 is prime
# 3 is prime
# 5 is prime
# 7 is prime
# 11 is prime

# else also runs when the loop body never executed
for x in []:
    print("never")
else:
    print("empty loop still reaches else")   # empty loop still reaches else

# "continue" does NOT stop else from running; only "break" does.
# "while ... else" works the same way.