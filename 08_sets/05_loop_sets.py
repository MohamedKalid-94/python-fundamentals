colors = {"red", "green", "blue"}

# 1. Plain loop: the order is NOT defined, so never depend on it
count = 0
for c in colors:
    count += 1
print(count)                                # 3

# 2. Sorted loop: a predictable order
for c in sorted(colors):
    print(c)
# blue
# green
# red

# 3. With enumerate
for i, c in enumerate(sorted(colors), start=1):
    print(i, c)
# 1 blue
# 2 green
# 3 red

# 4. A set of tuples
pairs = {("a", 1), ("b", 2)}
for key, value in sorted(pairs):
    print(key, value)
# a 1
# b 2

# 5. Loop and filter with a set lookup (fast membership)
allowed = {"admin", "editor"}
for user in ["admin", "guest", "editor"]:
    if user in allowed:
        print(user, "ok")
    else:
        print(user, "denied")
# admin ok
# guest denied
# editor ok

# 6. Consume a set with pop() in a while loop
work = {1, 2, 3}
done = 0
while work:
    work.pop()
    done += 1
print(done)                                 # 3

# 7. Aggregate
nums = {4, 8, 15}
total = 0
for n in nums:
    total += n
print(total)                                # 27

# 8. Build a new set with a comprehension
print({n * n for n in range(5)})            # {0, 1, 4, 9, 16}

# 9. Unique values from a list, then loop
for ch in sorted(set("banana")):
    print(ch, end=" ")
print()                                     # a b n

# Do not add or remove items of the set you are looping over (RuntimeError).