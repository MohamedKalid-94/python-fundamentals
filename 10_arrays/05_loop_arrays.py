from array import array

a = array("i", [10, 20, 30])

# 1. Items
for v in a:
    print(v)
# 10
# 20
# 30

# 2. Index
for i in range(len(a)):
    print(i, a[i])
# 0 10
# 1 20
# 2 30

# 3. enumerate
for i, v in enumerate(a, start=1):
    print(i, v)
# 1 10
# 2 20
# 3 30

# 4. while
i = 0
while i < len(a):
    print(a[i], end=" ")
    i += 1
print()                                     # 10 20 30

# 5. Two arrays together
b = array("i", [1, 2, 3])
for x, y in zip(a, b):
    print(x + y, end=" ")
print()                                     # 11 22 33

# 6. Reversed and sorted views
for v in reversed(a):
    print(v, end=" ")
print()                                     # 30 20 10

# 7. Change items in place (through the index)
data = array("i", [1, 2, 3])
for i in range(len(data)):
    data[i] *= 2
print(data)                                 # array('i', [2, 4, 6])

# 8. Accumulate
total = 0
for v in a:
    total += v
print(total)                                # 60

# 9. Bytes: each item is an int
for byte in array("B", b"Hi"):
    print(byte, chr(byte))
# 72 H
# 105 i

# 10. Convert the items to another type while looping (embedded style: ADC to volts)
adc = array("H", [0, 1023, 512])
volts = [round(v * 3.3 / 1023, 2) for v in adc]
print(volts)                                # [0.0, 3.3, 1.65]

# 11. Build a new typed array from a comprehension
print(array("i", [v * v for v in a]))       # array('i', [100, 400, 900])

# Do not add or remove items of the array you are looping over.