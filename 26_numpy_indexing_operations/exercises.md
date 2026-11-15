Write the questions as # comments and your solutions as code. Use assert statements to check your own answers.

On a 6x6 matrix of the numbers 0 to 35, select with slicing only: the border, every second element in a checkerboard pattern, the centre 2x2 block, and both diagonals (once with slicing, once with fancy indexing).
Pick rows 1 and 4 and columns 0, 2 and 5 of a 6x6 matrix with np.ix_. Then set the same cells to -1 using fancy assignment, and explain why the result of the selection is a copy.
Count how many times each value from 0 to 9 occurs in a 1-D array of 50 integers (build it with np.arange(50) * 7 % 10). Do it with counts[idx] += 1, with np.add.at and with np.bincount. Which of the three gives a different answer, and why?
Make a structured array of 5 devices (id, name, temp, online). Select the names of online devices above 25 degrees, increase temp by 1 for all offline devices, and list the devices ordered by temperature using argsort on the temp field.
A 2-D array of readings contains nan values and values outside 0 to 100. Replace the out-of-range values with nan using a mask, then replace every nan with the mean of its column (use np.isnan, np.nanmean and np.where). Count how many cells you changed.
For a 3-D int16 array and its transpose, print shape, strides and the flags. Compute the byte offset of one element by hand with the strides and check it against a.view(np.uint8).
Broadcasting: (a) scale every row of a 4x3 matrix so it sums to 1, (b) subtract the per-channel mean from an array of shape (8, 8, 3), (c) build the 9x9 multiplication table without a loop. Then write down the result shape for six pairs of shapes of your choice, and check them with np.broadcast_shapes. Make two of the pairs fail.
Arithmetic: brighten a uint8 image row by 50 without wrap-around (saturate at 255), once with astype and np.minimum, once with np.clip. Then compare //, %, np.fmod and np.divmod for the numbers -7 and 7 divided by 3 and -3.
A buffer holds 4 big-endian int32 values. Read them correctly, convert them to native byte order, and prove that byteswap on the wrong reading gives the right values. Show what astype(">i4") does to the bytes but not to the values.
A 16-bit status word has bit 0 = READY, bit 1 = ERROR, bit 2 = OVERRUN, bits 4 to 7 = a 4-bit mode number. Decode an array of 8 such words into four arrays: the three flags and the mode. Count how many bits are set in each word with np.bitwise_count. Then set OVERRUN on all words with ERROR set.
Sort 10 rows of (last name, first name, age) by last name, then first name, then age (descending) with np.lexsort. Find the 3 oldest people with argpartition. Check that kind="stable" keeps the original order of two people with equal ages.
Searching: (a) put 20 values into 4 bins with np.searchsorted, (b) find the first index where the running total (cumsum) exceeds 100, (c) find the value of a sorted array nearest to 7.3 using searchsorted and a comparison of its two neighbours.
Two arrays of user IDs: find those in both, only in A, only in B, in either, and in exactly one. Then find the duplicated IDs in A. Finally take a 2-D log of (user, action) rows, remove the duplicates while keeping the first appearance order, and count each distinct row.
Remove the columns of a 2-D array whose sum is below a threshold using a mask, insert a column of ones at the front, swap the first and last columns in place, reverse every row, and shift every row two places to the right with np.roll.
Embedded exercise: simulate a 1000-sample 12-bit ADC trace without random numbers (for example (2000 + 1500 * np.sin(np.arange(1000) / 20)).astype(np.uint16) with a few samples set to 4095 and a few spikes). Find the runs of clipped samples (value 4095), replace spikes (a jump of more than 800 between neighbouring samples) with the average of their neighbours, reshape into blocks of 100 and find the maximum of each block and its position, and find the first sample above 3000 with argmax.
RAG exercise: make 10 document vectors of 4 numbers by hand, a category label for each, and a query vector. Compute cosine similarities with broadcasting, keep only documents of one category with a mask, and return the top 3 in order with argpartition and argsort.
Predict first, then run, and explain each result in a comment:
python
import numpy as np

a = np.arange(12).reshape(3, 4)
b = a[:, [0, 2]]
c = a[:, 0:3:2]
b[0, 0] = 100
c[1, 0] = 200
print(a)
print(np.shares_memory(a, b), np.shares_memory(a, c))
print(a[a % 2 == 0].shape, a[[0, 2], [1, 3]], (a > 5).sum(axis=0))
print((np.arange(3)[:, None] + np.arange(3)).tolist())