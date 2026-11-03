# continue: skip the rest of THIS iteration and go to the next one

# Print only odd numbers
for n in range(1, 8):
    if n % 2 == 0:
        continue
    print(n, end=" ")
print()                         # 1 3 5 7

# Ignore invalid values
data = [4, -1, 7, -3, 2]
total = 0
for x in data:
    if x < 0:
        continue
    total += x
print(total)                    # 13

# Skip blank strings
words = ["a", "", "b", " "]
for word in words:
    if not word.strip():
        continue
    print(word)
# a
# b

# In a while loop, update the counter BEFORE continue,
# otherwise you create an endless loop
i = 0
while i < 6:
    i += 1
    if i % 2 == 0:
        continue
    print(i)
# 1
# 3
# 5

# continue makes code flatter than a big nested if
# Instead of:                     Write:
#   for x in data:                  for x in data:
#       if x >= 0:                      if x < 0:
#           ...lots of code...              continue
#                                       ...lots of code...