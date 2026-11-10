import os

# Two functions with deliberate bugs

def average(numbers):
    total = 0
    for n in numbers:
        total += n
    return total / len(numbers) + 1             # BUG: the "+ 1" does not belong here


def sum_to(n):
    """Return 1 + 2 + ... + n."""
    total = 0
    for i in range(n):                          # BUG: range(n) stops at n - 1
        total += i
    return total


print("average:", average([2, 4, 6]))           # average: 5.0     (expected 4.0)
print("sum_to:", sum_to(5))                     # sum_to: 10       (expected 15)

# 1. Print debugging: the f"{x=}" form shows the name and the value
n = 5
print(f"{n=}")                                  # n=5

# 2. Start the debugger from inside the code with breakpoint().
#    Remove the next two lines to try it: the program stops there and shows (Pdb).
#        breakpoint()
#        print("after the breakpoint")
# Setting PYTHONBREAKPOINT=0 turns every breakpoint() into a no-op:
os.environ["PYTHONBREAKPOINT"] = "0"
breakpoint()                                    # does nothing because of the line above
print("after breakpoint")                       # after breakpoint


# 3. The fixed versions
def average_fixed(numbers):
    return sum(numbers) / len(numbers)

def sum_to_fixed(n):
    return sum(range(1, n + 1))

print(average_fixed([2, 4, 6]), sum_to_fixed(5))        # 4.0 15