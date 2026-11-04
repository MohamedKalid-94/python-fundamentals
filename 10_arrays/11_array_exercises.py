from array import array

# 1. Sum, min, max and average of sensor readings
data = array("d", [20.5, 22.0, 21.5, 25.0])
print(sum(data), min(data), max(data), sum(data) / len(data))      # 89.0 20.5 25.0 22.25

# 2. Index of the largest value
print(data.index(max(data)))                    # 3

# 3. Remove duplicates, keep the order
print(array("i", dict.fromkeys(array("i", [3, 1, 3, 2, 1]))))      # array('i', [3, 1, 2])

# 4. Second largest value
print(sorted(set(array("i", [10, 20, 20, 5])))[-2])                # 10

# 5. Checksums of a packet (8-bit, as on a microcontroller)
packet = array("B", [10, 20, 30, 250])
print(sum(packet) & 0xFF)                       # 54       sum modulo 256
xor = 0
for b in packet:
    xor ^= b
print(xor)                                      # 250      XOR checksum
print((-sum(packet)) & 0xFF)                    # 202      two's complement checksum

# 6. Moving average of ADC samples (window of 3)
adc = array("H", [100, 102, 98, 110, 120, 115])
print([round(sum(adc[i:i + 3]) / 3, 1) for i in range(len(adc) - 2)])
# [100.0, 103.3, 109.3, 115.0]

# 7. How many samples are above a threshold?
print(sum(1 for v in adc if v > 105))           # 3

# 8. Peak detection: higher than both neighbours
print([i for i in range(1, len(adc) - 1) if adc[i] > adc[i - 1] and adc[i] > adc[i + 1]])
# [1, 4]

# 9. A 2D grid stored in a flat array (row * columns + column, as in C)
rows, cols = 3, 4
grid = array("i", [0] * (rows * cols))
grid[1 * cols + 2] = 7
print(grid)                                     # array('i', [0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0])
for r in range(rows):
    print(list(grid[r * cols:(r + 1) * cols]))
# [0, 0, 0, 0]
# [0, 0, 7, 0]
# [0, 0, 0, 0]

# 10. Split and rebuild a 16-bit value
value = 0x1234
high, low = value >> 8, value & 0xFF
print(high, low)                                # 18 52
print((high << 8) | low)                        # 4660
print(array("B", [high, low]).tobytes().hex())  # 1234

# 11. Binary search in a sorted array
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

sorted_arr = array("i", [1, 3, 5, 7, 9, 11])
print(binary_search(sorted_arr, 7), binary_search(sorted_arr, 4))  # 3 -1

# 12. Prefix sums: the sum of any range in O(1)
values = array("i", [1, 2, 3, 4])
prefix = array("i", [0])
for v in values:
    prefix.append(prefix[-1] + v)
print(prefix)                                   # array('i', [0, 1, 3, 6, 10])
print(prefix[3] - prefix[1])                    # 5        sum of values[1:3]

# 13. A counting table (like a histogram array in C)
counts = array("i", [0] * 10)
for digit in [3, 1, 3, 3, 7, 1]:
    counts[digit] += 1
print(counts)                                   # array('i', [0, 2, 0, 3, 0, 0, 0, 1, 0, 0])

# 14. A circular (ring) buffer
size = 4
buf = array("i", [0] * size)
head = 0
for v in [1, 2, 3, 4, 5, 6]:
    buf[head] = v
    head = (head + 1) % size
print(buf, head)                                # array('i', [5, 6, 3, 4]) 2

# 15. Hex dump of a buffer
print(" ".join(f"{b:02x}" for b in array("B", [1, 2, 255])))   # 01 02 ff