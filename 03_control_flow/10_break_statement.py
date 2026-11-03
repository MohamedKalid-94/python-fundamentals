# break: exit the loop immediately

for n in [3, 8, 12, 5]:
    if n > 10:
        print("found", n)
        break
    print("checked", n)
# checked 3
# checked 8
# found 12          (5 is never reached)

# break only leaves the INNERMOST loop
for i in range(3):
    for j in range(3):
        if j == 2:
            break
        print(i, j)
# 0 0
# 0 1
# 1 0
# 1 1
# 2 0
# 2 1

# To leave BOTH loops, use a flag
found = False
for i in range(3):
    for j in range(3):
        if i * j == 2:
            found = True
            break
    if found:
        break
print(i, j)                     # 1 2

# break in "while True" is the standard way to stop an endless loop
count = 0
while True:
    count += 1
    if count == 3:
        break
print(count)                    # 3

# break skips the loop's else block (see 08_for_else_loops.py)