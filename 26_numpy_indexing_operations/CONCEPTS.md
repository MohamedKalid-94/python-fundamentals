# Module 26: NumPy Indexing and Operations, Concepts Summary

| # | Topic | Concept | Remember |
|---|---|---|---|
| 01 | Indexing | Single elements | `a[i]`, `a[i, j]`; negative numbers count from the end; out of range raises `IndexError` |
| 01 | Slicing | Ranges | `a[start:stop:step]`, stop excluded; `...` and `np.newaxis`; out-of-range slices give empty arrays |
| 01 | Slicing | Views | A basic slice is a view: writing to it changes the original |
| 02 | Fancy indexing | Lists and arrays | `a[[0, 2]]`; the result has the shape of the index array; two lists are taken as pairs; `np.ix_` gives rows x columns |
| 02 | Fancy indexing | Copies | Always a copy; assignment works; a repeated index in `+=` counts once, `np.add.at` and `np.bincount` count every repeat |
| 02 | Fancy indexing | Helpers | `np.take`, `np.put`, `np.take_along_axis` |
| 03 | Field access | Structured arrays | `a["name"]` is a view of one field, `a[["f1", "f2"]]` several; masks work on a field |
| 04 | Boolean indexing | Masks | `a[a > 4]`; combine with `&`, `\|`, `~` and parentheses (never `and`/`or`); a mask makes a copy |
| 04 | Filtering | Tools | `np.where(cond, x, y)`, `np.clip`, `np.select`, `np.extract`, `np.nonzero`, `np.flatnonzero` |
| 04 | Comparisons | Functions | `==`, `<` ..., `np.array_equal`, `np.isclose`, `np.allclose`, `np.any`, `np.all`; compare NaN with `np.isnan` |
| 05 | Attributes | List | `shape`, `ndim`, `size`, `dtype`, `itemsize`, `nbytes`, `strides`, `flags`, `base` |
| 05 | Strides | Meaning | Bytes to step along each axis; `T`, steps and reversals only change strides; `sliding_window_view` copies nothing |
| 06 | Broadcasting | Rules | Compare shapes from the last axis: equal or 1 is compatible; add 1s on the left; else `ValueError` |
| 06 | Broadcasting | Uses | Centre and scale columns, `keepdims=True`, distance tables with `[:, None]`, grids without `meshgrid` |
| 07 | Arithmetic | Operators | `+ - * / // % **` and `np.add` ...; `/` is always float; floor division and `%` round toward minus infinity |
| 07 | Arithmetic | Details | In-place operators must fit the dtype; `out=` and `where=`; division by zero gives `inf`, `nan` and a warning |
| 08 | Axes | Swapping | `swapaxes`, `moveaxis`, `transpose(axes)`, all views |
| 08 | Byte order | Swapping | `<` little, `>` big; `byteswap` changes the bytes, `view(">u2")` rereads them, `astype(">u2")` converts the values |
| 09 | Binary operators | Bits | `& \| ^ ~ << >>`; masks for test, set, clear and toggle; Python's `~1` is -2 and does not fit `uint8` |
| 09 | Binary operators | Helpers | `binary_repr`, `unpackbits`, `packbits`, `bitwise_count` |
| 10 | Sorting | Functions | `np.sort` (copy), `a.sort()` (in place), `argsort`, `lexsort` (last key is main), `partition`; `kind="stable"` keeps ties in order |
| 10 | Sorting | Patterns | Reorder another array with `names[np.argsort(a)]`; `axis=0/1/None`; descending with `[::-1]` |
| 10 | Searching | Functions | `argmax`, `argmin`, `where`, `searchsorted` (needs sorted data, `side=`), `isin` |
| 10 | Counting | Functions | `count_nonzero`, `mask.sum()`, `bincount`, `unique(return_counts=True)` |
| 11 | Sets | Functions | `unique`, `union1d`, `intersect1d`, `setdiff1d`, `setxor1d`, `isin` (the old `in1d` is gone) |
| 11 | Unique rows | `axis=0` | `np.unique(a, axis=0)`; `return_index` to keep the original order; union of tables = `vstack` then unique |
| 12 | Size changes | Functions | `append`, `insert`, `delete` return new arrays; collect in a list and join once instead of appending in a loop |
| 12 | Rearranging | Functions | Swap columns with `c[:, [1, 0, 2]]`, reverse with `[::-1]` or `flip`, `roll`, `rot90` |
| 12 | Axes | Inserting | `np.newaxis` / `None`, `np.expand_dims` |
| 13 | Worked examples | Patterns | z-score by column, mask-and-replace outliers, top-k with `argpartition`, nearest neighbour by broadcasting, status bits, `searchsorted` lookup, unique rows in order, `bincount` |