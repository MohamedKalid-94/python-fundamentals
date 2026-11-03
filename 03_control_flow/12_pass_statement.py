# pass does nothing. It is a placeholder where Python needs a statement.

if True:
    pass                        # without pass, an empty block is an IndentationError

for _ in range(3):
    pass                        # loop that does nothing (rare)

# Typical use: stubs you will fill in later
def todo():                     # functions come in Module 04
    pass

class Empty:                    # classes come in Module 12
    pass

# "..." (Ellipsis) works the same way as a stub
def later():
    ...

# pass vs continue vs break
for n in [1, 2, 3]:
    if n == 2:
        pass                    # does nothing, the loop body continues
    print("after pass", n)
# after pass 1
# after pass 2
# after pass 3

for n in [1, 2, 3]:
    if n == 2:
        continue                # skips the rest of this iteration
    print("after continue", n)
# after continue 1
# after continue 3

for n in [1, 2, 3]:
    if n == 2:
        break                   # leaves the loop
    print("after break", n)
# after break 1

# Warning: "except: pass" silently hides errors. Avoid it (Module 14).