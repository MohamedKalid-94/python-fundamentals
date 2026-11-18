# Module 29: pandas Basics, Concepts Summary

| # | Topic | Concept | Remember |
|---|---|---|---|
| 01 | pandas | Structures | `Series` (labelled 1-D) and `DataFrame` (columns that share one index); built on NumPy; this course uses pandas 3 |
| 01 | pandas | Why | Labels, one dtype per column, missing-value tools, arithmetic that aligns on labels, readers for CSV, Excel, JSON, SQL, Parquet |
| 01 | Panel | Gone | `pd.Panel` no longer exists: use a DataFrame with a `MultiIndex` (Module 31), or the `xarray` package |
| 02 | Series | Creation | From a list, ndarray, dict (keys become the index) or one value; `index=`, `dtype=`, `name=`; missing values turn ints into floats |
| 02 | Series | Attributes | `values index dtype name shape size ndim nbytes empty is_unique hasnans`; `to_numpy()` is read-only, `copy=True` to change it |
| 03 | Selecting | By label | `s.loc[a:b]` includes both ends; `s.at[label]` for one value |
| 03 | Selecting | By position | `s.iloc[a:b]` excludes the end; `s.iat[i]`; `s[a:b]` is a position slice for integer data: prefer `loc` and `iloc` |
| 03 | Selecting | Masks | `s[s > 2]`, `&`, `\|`, `~`, `isin`, `between`, `where`, `mask`, `nlargest`, `idxmax`; `s.get(label, default)` for safe lookups |
| 04 | Series arithmetic | Alignment | `a + b` matches labels, others give `NaN`; `a.add(b, fill_value=0)`; `==` needs identical labels |
| 04 | Series arithmetic | Tools | Scalars, NumPy ufuncs, `map`, `apply`, `clip`, `rank`, `shift`, `diff`, `pct_change`, `cumsum` |
| 04 | Conversions | Targets | `to_list`, `to_dict`, `to_numpy`, `to_frame`, `to_csv`, `to_json`, `astype`, `pd.to_numeric(errors="coerce")`, `pd.to_datetime` |
| 05 | Index | Objects | Immutable labels: `Index`, `RangeIndex`, `DatetimeIndex`, `MultiIndex`; `union`, `intersection`, `difference`, `get_loc`, `get_indexer`, `isin` |
| 05 | Index | Changing | `set_index`, `reset_index`, `rename_axis`, `df.index = ...`, `df.columns = ...`, `rename`; duplicate labels are allowed but return several rows |
| 06 | DataFrame | Creation | Dict of lists or Series, list of dicts, 2-D array with `columns=`, records, `from_dict`, `from_records`; columns of different length raise `ValueError` |
| 06 | DataFrame | Look | `shape size ndim columns index dtypes T`, `head`, `tail`, `info`, `describe` (`include="all"`), `astype`, `convert_dtypes`, `select_dtypes` |
| 07 | Accessing | Columns | `df["a"]` (Series), `df[["a", "b"]]` (DataFrame), `df.a` only for simple names; `filter(items, like, regex)` |
| 07 | Accessing | Rows and cells | `loc` (labels), `iloc` (positions), `at`, `iat`; `df[1:3]` slices rows by position; `take`, `sample`, `nlargest` |
| 07 | Accessing | Conditions | Masks with `&`, `\|`, `~`, `isin`, `.str`; `query("age > 30 and city == 'Goa'")`, `@variable`; `where` keeps the shape |
| 08 | Modifying | Add and change | `df["c"] = ...`, `assign` (returns a copy), `insert`, `df.loc[mask, "c"] = v`, `rename`, `replace`, `astype`, `round` |
| 08 | Removing | Columns and rows | `drop(columns=...)`, `drop(index=...)`, `pop`, `del`, boolean masks, `dropna`, `drop_duplicates`, `reset_index(drop=True)` |
| 08 | Removing | Style | Methods return new tables: reassign; `inplace=True` returns `None` and does not make it faster |
| 09 | DataFrame arithmetic | Alignment | Aligned on rows and columns; `df + series` matches the columns, `axis=0` matches the rows; `add(fill_value=)` |
| 09 | DataFrame arithmetic | Tools | Reductions with `axis`, `cumsum`, `diff`, `pct_change`, `corr`, `cov`, `dot`, min-max scaling, `combine_first` |
| 10 | Basic functionality | Counting | `count`, `value_counts`, `nunique`, `unique`, `isna().sum()`, `duplicated` |
| 10 | Basic functionality | Summaries | `sum mean median min max std quantile idxmax cumsum agg`; missing values are skipped; `numeric_only=True` |
| 10 | Basic functionality | Order and copies | `sort_values`, `sort_index`, `rank`, `copy`, `equals`, `items`, `iterrows`, `itertuples`, `pipe` |
| 11 | pandas 3 | Copy-on-write | A result never changes its parent; chained assignment `df["a"][0] = 1` does nothing (a warning); use `df.loc[row, col] = v` |
| 11 | pandas 3 | `str` dtype | Text columns are `str` with `NaN` for missing; `object` and `string` still exist |
| 11 | pandas 3 | Nullable dtypes | `Int64`, `Float64`, `boolean`, `string` with `pd.NA` (ambiguous in `bool()`); `convert_dtypes()` |
| 12 | Worked examples | Patterns | ADC to volts with `assign`, flags with `isin`, alignment of two sensors, many output formats, rankings, scaling for machine learning |