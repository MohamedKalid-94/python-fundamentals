Write the questions as # comments and your solutions as code below each one.

Create arrays with the typecodes 'b', 'B', 'h', 'H', 'i', 'q', 'f' and 'd'. Print each itemsize and the largest and smallest value each type can hold (calculate the range from the itemsize).
Show what happens when you put 300 into a 'B' array, -1 into a 'B' array, and 1.5 into an 'i' array. Then write wrap8(value) that returns the value as an 8-bit unsigned number the way C would (value & 0xFF).
Create an array of 6 temperature readings ('f'). Print the first, the last, the middle two, and every second reading, then the sum, the average, the minimum and the maximum.
Add readings with append, extend and insert, remove one with remove and one with pop, and delete a slice with del. Print the array after each step.
Write clear(arr) that empties an array in place (hint: there is no clear() method).
Write remove_all(arr, value) that removes every occurrence in place without the skipping bug.
Copy an array in four ways, change the copy, and show which ones leave the original unchanged. Explain in a comment why there is no shallow-copy problem for arrays.
Write reverse_in_place(arr) with two pointers, and rotate_left(arr, k) and rotate_right(arr, k) that also work when k is larger than the length.
Sort an array in three ways: array(typecode, sorted(...)), in place with a slice assignment, and with a hand-written bubble sort that swaps items.
Write a binary search for a sorted array, then use bisect_left to do the same and compare the results on 10 test values.
Join two 'i' arrays in four ways, then show the error when the typecodes differ and fix it with a conversion.
Convert the array array("H", [0x1234, 0xABCD]) to bytes, print the bytes as hex, then call byteswap() and print again. Explain what changed in a comment.
Convert 4 bytes read from a sensor, array("B", [0x00, 0x00, 0x01, 0x2C]), to a 32-bit integer in big-endian and in little-endian order, using int.from_bytes (the answers are 300 and 738263040).
Write a packet builder: a header byte 0xAA, a length byte, a payload array, and an 8-bit sum checksum at the end. Then write verify(packet) that checks the checksum.
Simulate an ADC: build 20 samples of a 10-bit signal (values 0 to 1023) with a fixed list, convert them to volts for a 3.3 V reference, and print the maximum, minimum and average voltage.
Smooth the same samples with a moving average of window 5, and find the indexes where the signal crosses 512 from below to above.
Implement a ring buffer class-free: an array, a head index and a push(buf, head, value) function that returns the new head. Push 10 values into a buffer of size 4 and print the buffer after each push.
Store a 4x4 matrix in a flat array. Write get(m, r, c) and set(m, r, c, value), fill the diagonal with 1, print the matrix row by row, and compute its transpose.
Write the array to a binary file with tofile, read it back with fromfile, and check that both arrays are equal. Delete the file at the end.
Compare the memory of a list and an array of 100,000 integers using sys.getsizeof, and the time of sum() on both with time.perf_counter(). Print both results and explain them in a comment.
Predict first, then run, and explain each result in a comment:
python
from array import array
a = array("B", [250, 5])
b = a
b.append(1)
c = a[:]
c[0] = 7
print(a, c, a is b)

print(array("i", [1, 2]) == [1, 2], array("i", [1, 2]) * 2)
print(array("b", [127]).tolist(), array("B", [255]).tobytes())

try:
    a[0] = a[0] + 10
except OverflowError:
    print("overflow")

print(sum(a) & 0xFF, a.buffer_info()[1] * a.itemsize)
print(array("H", [1]).tobytes() in (b"\x01\x00", b"\x00\x01"))