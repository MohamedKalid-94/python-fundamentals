# Module 28: NumPy Data, Time and Signals, Concepts Summary

| # | Topic | Concept | Remember |
|---|---|---|---|
| 01 | Structured arrays | dtype | List of `(name, type)` tuples, a string `"u2, f4"`, or a dict with `offsets` and `itemsize`; `a["field"]` is a view, `a[i]` one record |
| 01 | Structured arrays | Layout | Packed (`offsets`) vs C-aligned (`align=True`); `dtype.fields[name][1]` is the byte offset; sub-array and nested fields |
| 01 | Structured arrays | Operations | `np.sort(order=...)` (later fields break ties), `argsort(order=)`, `numpy.lib.recfunctions` (`append_fields`, `drop_fields`, `rename_fields`, `merge_arrays`, `structured_to_unstructured`) |
| 01 | Structured arrays | Bytes | `tobytes` and `frombuffer` with the same dtype read and write binary packets |
| 02 | Record arrays | `np.recarray` | Attribute access `r.temp` and `r["temp"]`; build with `np.rec.array`, `fromrecords`, `fromarrays`, or `.view(np.recarray)`; slower, prefer plain structured arrays |
| 03 | Binary files | `.npy` and `.npz` | `np.save`, `np.load`, `np.savez`, `np.savez_compressed`; dtype, shape and byte order are stored |
| 03 | Binary files | Raw bytes | `tofile` and `np.fromfile` keep no header: remember dtype, shape and byte order |
| 03 | Binary files | Big files | `np.load(mmap_mode="r")`, `np.memmap`, `open_memmap`; `allow_pickle=False` for files you do not trust |
| 04 | Text files | Reading | `loadtxt` (strict: `skiprows`, `usecols`, `unpack`, `dtype`, `max_rows`), `genfromtxt` (`names=True`, `filling_values`, `missing_values`) |
| 04 | Text files | Writing | `savetxt(fmt=, delimiter=, header=, comments="")`; the default format keeps every digit, `%.2f` does not |
| 04 | File formats | Choice | `.npy`/`.npz` for NumPy, text/CSV for other programs, raw `.bin` for devices, pandas for tables, HDF5 for big labelled data |
| 05 | Missing data | Identify | `isnan`, `isinf`, `isfinite`; never `== np.nan`; integer arrays cannot hold `nan` |
| 05 | Missing data | Remove | Boolean masks, `any`/`all` over rows, `nan_to_num` |
| 05 | Missing data | Impute | Mean, median, forward fill (`maximum.accumulate`), `np.interp`, column means with `where` |
| 05 | Missing data | Masked arrays | `np.ma.masked_invalid`, `masked_equal`, `.filled()`, `.count()`; the data stay, the mask hides |
| 06 | Datetime | Types | `datetime64[unit]` (Y M W D h m s ms us ns), `timedelta64`; stored as integers since 1970-01-01; `NaT` is missing |
| 06 | Datetime | Functions | `astype` to change unit, `arange` for ranges, `datetime_as_string`, `busday_count`, `busday_offset`, `is_busday` |
| 06 | Time zones | Rule | NumPy has none: an offset in a string is converted to UTC with a warning; keep UTC, convert for display (zoneinfo, pandas) |
| 06 | Leap seconds | Rule | Not represented: every day has 86400 seconds; `23:59:60` is an error |
| 07 | Time deltas | Arithmetic | `t2 - t1`, `t + delta`, `delta / np.timedelta64(1, "h")` for a float; months and years cannot be mixed with days |
| 07 | Time series | Patterns | Select with masks and `searchsorted`; group with `unique(return_inverse)` and `bincount(weights=)`; bin with `datetime64[6h]`; weekday = `(days + 3) % 7`; find gaps with `diff` |
| 08 | Performance | Rules | Vectorize; smallest adequate dtype; avoid copies (`out=`, in place, views); preallocate; measure before optimising |
| 08 | Memory layout | C and F order | `flags`, `strides`; `.T` only changes strides; `ascontiguousarray` copies; a field of a structured array is strided |
| 09 | FFT | Functions | `rfft`, `irfft`, `rfftfreq`, `fftfreq`, `fftshift`; amplitude `2 * abs(X) / N`; resolution is `fs / N` |
| 09 | FFT | Effects | Aliasing above fs/2 (60 Hz at 100 Hz looks like 40 Hz); leakage reduced by a window (`np.hanning`); Parseval |
| 09 | Signal processing | Filters | Zero bins to low-pass or notch; `np.convolve` (`full`, `same`, `valid`) for FIR filters; convolution theorem; `np.correlate` finds delays |
| 09 | Fourier series | Idea | A square wave is a sum of odd sine harmonics; more terms, smaller error |
| 10 | Strings | Namespaces | `np.strings.*` (fast ufuncs: `upper`, `strip`, `replace`, `find`, `count`, `startswith`, `zfill`, `slice` ...), `np.char.*` (older; `split`, `join`, `mod`) |
| 10 | Strings | dtypes | `<U5` is fixed width and cuts long values on assignment; `StringDType()` has variable length; `S` is bytes |
| 11 | Matplotlib | Pattern | `fig, ax = plt.subplots()`, `ax.plot/scatter/bar/hist/imshow`, `ax.set(...)`, `fig.savefig`, `plt.close`; `matplotlib.use("Agg")` for files |
| 11 | Histograms | Facts | `ax.hist` returns the same counts and edges as `np.histogram`; `density=True` makes the area 1 |
| 12 | Seaborn | Distributions | `histplot(kde=True)`, `kdeplot`, `ecdfplot`, `rugplot`, `boxplot`, `violinplot`, `displot` (a `FacetGrid`); needs pandas |
| 13 | Worked examples | Patterns | Binary log with a structured dtype, repair and resample a time series, dominant frequencies, parse a text log, clean labels |