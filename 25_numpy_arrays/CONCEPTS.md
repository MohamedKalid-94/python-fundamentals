# Module 25: NumPy Arrays, Concepts Summary

| # | Topic | Concept | Remember |
|---|---|---|---|
| 01 | Introduction | What | A fixed-size, one-type, N-dimensional array in one block of memory; whole-array operations run in C |
| 01 | Introduction | Lists vs arrays | `list * 2` repeats, `array * 2` calculates; an array stores raw numbers side by side |
| 01 | Environment | Setup | `pip install numpy`, `import numpy as np`, check `np.__version__` (this course: NumPy 2.x) |
| 02 | ndarray | Attributes | `ndim`, `shape`, `size`, `dtype`, `itemsize`, `nbytes` |
| 02 | ndarray | Rules | One dtype per array (the widest that fits); ragged lists raise `ValueError`; `axis=0` runs down the rows |
| 03 | Data types | Families | `bool`, `int8..int64`, `uint8..uint64`, `float16/32/64`, `complex`, text `U`, bytes `S`; defaults `int64`, `float64` |
| 03 | Data types | Conversion | `astype` returns a copy; `int` truncates toward zero; `np.iinfo`, `np.finfo` give limits |
| 03 | Data types | Overflow | Integer arrays wrap around silently (`uint8`: 250 + 10 = 4); a Python int that does not fit raises `OverflowError`; widen first |
| 03 | Data types | Promotion | `np.result_type` gives the type that holds both; a Python float does not widen `float32`; floats are approximate: use `np.isclose` |
| 04 | Creation | Routines | `zeros`, `ones`, `full`, `empty` (uninitialised), `eye`, `identity`, `diag`, `*_like`, `fromfunction`, `triu`, `tril` |
| 04 | Manipulation | Overview | Shape, axes, joining, splitting, adding/removing, rearranging: where each group is taught |
| 05 | Existing data | Copy or not | `np.array` copies; `np.asarray` copies only if needed; `np.frombuffer` is a view on bytes (read-only for `bytes`) |
| 05 | Existing data | Other | `np.fromiter(generator, dtype, count)`, `.tolist()`; byte order matters: `"<u2"` vs `">u2"` |
| 06 | Ranges | Functions | `arange` (stop excluded, float steps can surprise), `linspace` (stop included), `logspace`, `geomspace`, `meshgrid` |
| 07 | Iterating | Tools | `for row in a`, `a.flat`, `ndenumerate`, `ndindex`, `nditer` (order, `readwrite`, `external_loop`) |
| 07 | Iterating | Advice | A Python loop over elements is slow; use whole-array operations |
| 08 | Reshaping | `reshape` | Same number of elements; `-1` is worked out; `order="F"`; usually a view |
| 08 | Reshaping | Axes | `np.newaxis`, `expand_dims`, `squeeze`; `resize` (in place) vs `np.resize` (repeats data) |
| 09 | Joining | Existing axis | `concatenate`, `vstack`, `hstack`, `dstack`, `column_stack`, `block` (`row_stack` is gone: use `vstack`) |
| 09 | Joining | New axis | `stack(axis=...)`; build a list and join once instead of appending in a loop |
| 10 | Splitting | Functions | `split` (equal parts or indices), `array_split` (unequal), `hsplit`, `vsplit`, `dsplit`; the pieces are views |
| 11 | Flattening | Variants | `flatten` copies, `ravel` is a view when possible, `reshape(-1)`, `a.flat` |
| 11 | Transposing | Functions | `a.T` (a view, reverses axes), `np.transpose(a, axes)`, `np.moveaxis` |
| 12 | Copies and views | Views | Basic slices, `reshape`, `ravel`, `T`, `view()`: shared memory; `a.base` points to the owner |
| 12 | Copies and views | Copies | Fancy indexing, boolean masks, `flatten`, `copy`, `astype`; `b = a` is only a second name |
| 12 | Copies and views | Checks | `np.shares_memory` (exact), `np.may_share_memory` (quick), `flags["OWNDATA"]` |
| 13 | Worked examples | Patterns | Sensor frame with `frombuffer` and `reshape`, windows with `array_split`, cosine similarity, stacking runs |