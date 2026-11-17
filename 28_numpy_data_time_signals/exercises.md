Write the questions as # comments and your solutions as code. Use assert and np.isclose to check your own answers.

Define a structured dtype for a device record: id (u4), name (U12), position (3 floats), status (a nested record with online and errors). Create 5 devices, fill them, select the online ones with more than 2 errors, and sort them by name and then id. Print the byte offset of every field with and without align=True.
Add a battery field with rfn.append_fields, rename name to label, drop position, and convert two numeric fields to a plain 2-D float array and back.
Build a recarray of 5 sensors, read the fields by attribute, change a field by attribute, and convert it back to a plain structured array. Write in a comment why a field called size cannot be read with a dot.
Save an array, a structured array and three arrays in an archive, load them back, and compare. Compare the file sizes of savez and savez_compressed for random data and for an array of zeros. Open a 1,000,000-element .npy file with mmap_mode="r" and read the last element without loading everything.
Write 1000 int16 samples as big-endian raw bytes. Read them back correctly with fromfile, then with the wrong byte order, and fix the wrong result with byteswap.
Create a CSV file (with a header, a comment line, a missing value and a text column), read it with loadtxt and with genfromtxt, and write a cleaned version with savetxt using different formats for each column.
A temperature array with nan, -999 and inf. Count each kind, replace the sentinel with nan, drop the infinities, then fill the gaps four ways: mean, median, forward fill and linear interpolation. Compare the four with the true values you started from.
Build the same cleaning with a masked array (np.ma): compute the mean, the count and the maximum, and fill the masked values with the mean.
Create all dates of December 2026. Find the weekdays, the business days (with 25 and 26 December as holidays), and the date of the last Friday. Convert a Unix timestamp array to dates and back to integers.
Show that NumPy has no time zones: parse 2026-11-15T10:00+0530, explain the warning, and print the same instant in UTC and in India time by adding a timedelta64. Compute the number of seconds between 2016-12-31T23:59:59 and 2017-01-01T00:00:00 and write down why it is not the real UTC value.
A week of readings every 15 minutes (use np.arange, no random numbers): find the readings of Wednesday, the daily mean and maximum with unique and bincount, the 6-hour averages, the gaps after deleting 10 readings, and fill them by interpolation.
Compare a Python loop, a list comprehension and a vectorized expression for the sum of x ** 2 + 3 * x over a million numbers, using timeit (print the ratios, not asserts). Compute the memory of the same data as float64, float32 and float16, and the error of the float32 sum.
Make a C-order and a Fortran-order array of shape (2000, 2000), print their strides, time sum(axis=0) and sum(axis=1) on each, and explain the four results.
Build a signal from three sine waves (for example 35, 90 and 210 Hz at fs = 2000 Hz). Find the three dominant frequencies and their amplitudes with the FFT, remove the middle one, and check the result against the signal without that wave. Sample a 120 Hz wave at 150 Hz and show where it appears.
Convolve a noisy square wave (use a seeded default_rng) with a 5-point box filter and with a Gaussian kernel, compare both with the clean wave using the mean squared error, and find the delay between a signal and a shifted copy with np.correlate.
Clean a list of 20 messy labels with np.strings (strip, lower, replace spaces and dashes, fix a typo with replace), count them with unique, and write the result as a table of label, count with savetxt. Then split sentences with np.char.split and count the words in each.
Plot (and save as PNG) a signal, its spectrum, a histogram of the noise with a fitted normal curve, and a 2-D heat map of a spectrogram you compute by hand with rfft over windows. Make a box plot and a violin plot of three sensors with Seaborn.
Embedded exercise: write a function that parses a binary log of 10,000 packets [time u32][sensor u8][value i16][crc u16] (little endian) produced with struct.pack. Check the CRC with a simple sum, drop the bad packets, convert the values to units, repair the missing samples by interpolation, compute the dominant vibration frequency per sensor, and save the result as .npz. Then write a second function that reads it back and plots the spectra.
Predict first, then run, and explain each result in a comment:
python
import numpy as np

a = np.array([(2, 1.5), (1, 2.5), (1, 0.5)], dtype=[("n", "i4"), ("x", "f8")])
print(np.sort(a, order="n")["x"], a["x"].strides, a[["n"]].itemsize)
b = np.array(["2026-11-15", "2026-12-31"], dtype="datetime64[D]")
print(b[1] - b[0], (b[1] - b[0]) / np.timedelta64(1, "W"), b.astype("datetime64[M]"))
c = np.array([1.0, np.nan, 3.0])
print(c.mean(), np.nanmean(c), np.ma.masked_invalid(c).mean(), np.interp(1, [0, 2], [10, 20]))
print(np.round(np.abs(np.fft.rfft(np.ones(8))), 3), np.convolve([1, 1], [1, 1, 1]))