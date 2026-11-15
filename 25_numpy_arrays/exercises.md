Write the questions as # comments and your solutions as code. Use assert statements to check your own answers.

Create these without typing the values: a 3x4 int8 array of zeros, a 4x4 array with 7 on the diagonal and 0 elsewhere, a 2x3 array of 0.5, and an empty array. Print the dtype, shape and nbytes of each.
A uint8 image row has the values [200, 220, 250]. Add 50 to brighten it. Show the wrong result, then fix it in two ways (widening with astype, and clipping with np.clip). Explain in a comment which one is right for an image.
Build the numbers 0.0, 0.1, ..., 1.0 (11 values) with arange and with linspace. Compare the lengths. Then find a start, stop and step where arange gives one element too many.
Using struct.pack, build a frame of one header byte plus eight uint16 values in big-endian order. Parse the values with np.frombuffer and with struct.unpack. Show that the results agree, and what changes if you read them with "<u2" by mistake.
Reshape the numbers 0 to 23 into (2, 3, 4), (4, 6), (6, -1) and (2, 12). Which of these are views of the original? Check with np.shares_memory.
Turn a row vector (1, 5) into a column vector (5, 1) in three ways. Then remove the extra axis from an array of shape (1, 3, 1, 4) with squeeze, once for all axes and once for a single axis.
You have three 1-D arrays of 4 sensor readings each. Build a table with the sensors as rows and as columns. Add a fourth sensor as a new row. Then try to add an array of the wrong length and read the error message.
Split an array of 100 samples into windows of 16 samples with reshape (dropping the rest), and into 7 nearly equal chunks with array_split. Split a 6x6 matrix into four 3x3 quadrants.
Convert an image array from (height, width, channels) to (channels, height, width) and back. Check that the result equals the original. After the transpose, is the array C-contiguous? Fix that with np.ascontiguousarray and check the flags again.
Predict first, then run, and explain each result in a comment:
python
import numpy as np

a = np.arange(8)
b = a[2:6]
c = a[[2, 3, 4, 5]]
b[0] = 100
c[1] = 200
d = a.reshape(2, 4)
d[1, 3] = -1
print(a)
print(b, c)
print(np.shares_memory(a, b), np.shares_memory(a, c), np.shares_memory(a, d))
Create a million-element array, keep only its first 3 elements, and prove with base and nbytes that the large array is still referenced. Then fix it.
Write a loop that computes the sum of squares of 100,000 numbers, and the same with one NumPy expression. Check that both give the same result, and time both with timeit (do not assert on the times).
Make 5 random-looking embeddings of 4 numbers by hand (or with np.arange and arithmetic). Normalise them, compute the cosine similarity of a query against all of them, and print the documents ranked from best to worst.
Embedded exercise: a byte stream holds big-endian signed 16-bit samples from 3 channels, interleaved (c0 c1 c2 c0 c1 c2 ...), 8 samples per channel, with a 2-byte header you must skip. Build it with struct, decode it with np.frombuffer, reshape it to (8, 3), convert each channel to volts, and print the maximum of each channel and where it occurs.
Write a function windows(signal, size, step) that returns a 2-D array of overlapping windows as copies, and another that returns them as views (look up np.lib.stride_tricks.sliding_window_view). Show that changing a view window changes the signal and changing a copy does not.