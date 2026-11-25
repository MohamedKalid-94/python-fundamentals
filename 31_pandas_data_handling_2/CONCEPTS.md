# Module 31: pandas Data Handling (part 2), Concepts Summary

| # | Topic | Concept | Remember |
|---|---|---|---|
| 01 | Concatenation | Rows | `pd.concat([a, b])` stacks rows and matches columns by name; missing columns give `NaN`; `join="inner"` keeps the common columns; `ignore_index=True` renumbers |
| 01 | Concatenation | Labels and checks | `keys=[...]` records where each row came from (a MultiIndex); `verify_integrity=True` rejects repeated index values |
| 01 | Concatenation | Columns | `axis=1` matches rows by index label; `DataFrame.append` is gone; build a list of tables and concat once |
| 01 | Concatenation | Filling | `combine_first`, `fillna(other_table)`, `update` fill gaps from another table |
| 02 | Merge | Types | `how="inner"` (both), `"left"`, `"right"`, `"outer"`, `"cross"`; `on`, `left_on`/`right_on`, `left_index`/`right_index`; `suffixes` |
| 02 | Merge | Safety | `validate="one_to_one"/"many_to_one"` raises `MergeError`; duplicate keys multiply rows; `indicator=True` adds `_merge` (anti-join with `left_only`) |
| 02 | Merge | Traps | `NaN` matches `NaN` (SQL `NULL` never matches); keys of different types raise `ValueError`: convert first |
| 02 | Join | Index | `left.join(right, on=...)` joins on the right table's index; `lsuffix`, `rsuffix` |
| 02 | Merge | By time | `merge_asof` (nearest earlier, `direction`, `tolerance`, `by`), `merge_ordered(fill_method="ffill")` |
| 03 | Statistics | Centre and spread | `mean`, `median`, `mode`, `std` and `var` (`ddof=1` by default, unlike NumPy), `sem`, `skew`, `kurt`, `quantile`, `describe(percentiles=, include=, exclude=)` |
| 03 | Statistics | Relations | `corr` (pearson, spearman), `cov`, `corrwith`, `autocorr`; `min_periods`; `NaN` pairs are skipped |
| 03 | Statistics | Options | `skipna`, `min_count`, `numeric_only`; `diff`, `pct_change`, `cumsum`, `cummax`, `rank`; z-score, min-max scaling, IQR outliers |
| 04 | Text | Accessor | `.str.lower/upper/title/strip/replace/contains/startswith/split/extract/cat/slice/zfill/pad/get_dummies/normalize` on Series, columns and index |
| 04 | Text | Regular expressions | `replace`, `contains`, `split` use regex by default: `regex=False` for plain text; `extract` with named groups gives columns; `extractall`, `findall` |
| 04 | Text | Missing text | Stays `NaN`; `contains(na=...)`; `len` gives float with `NaN`; `str` dtype in pandas 3 |
| 05 | Options | Use | `get_option`, `set_option`, `reset_option`, `describe_option`, and `option_context` (temporary): `display.max_rows`, `max_columns`, `width`, `max_colwidth`, `precision`, `float_format` |
| 05 | Options | Formatting a table | `to_string(float_format=, na_rep=, max_rows=)`, `to_html`, `Styler` (`format`, `highlight_max`, `hide`, `map`, `set_caption`; needs jinja2); display strings, not data |
| 06 | Windows | `rolling` | `rolling(n, min_periods, center, closed, step)`, or a time span `"2s"` on a sorted DatetimeIndex; `mean sum min max median std count quantile corr apply(raw=True) agg` |
| 06 | Windows | `expanding` and `ewm` | Running statistics; `ewm(alpha / span / halflife, adjust=False)` is `y = alpha * x + (1 - alpha) * y_previous` |
| 06 | Windows | Related | `shift`, `diff`, `pct_change`, `cummax`; the first `n - 1` results are `NaN` |
| 07 | Masks | Rules | Comparisons give bool Series; combine with `&`, `\|`, `~`, `^` and parentheses (never `and`/`or`); `NaN` compares `False` |
| 07 | Masks | Tools | `isin`, `between(inclusive=)`, `str.contains`, `isna`, `any/all(axis=1)`, `where`, `mask`, `np.where`, `np.select`, `clip`, `query` (`@var`, backticks, `in`) |
| 07 | Masks | Changing | `df.loc[mask, col] = value`; a filtered table is a new table (copy-on-write) |
| 08 | Missing data | Find | `isna`, `notna`, `isna().sum()`, `isna().mean()`; `NaN == NaN` is `False`, `Series.equals` treats them as equal |
| 08 | Missing data | Fill | `fillna(value / dict / Series)`, `ffill(limit)`, `bfill`, `interpolate` (`limit`, `limit_direction`, `limit_area`, `method="index"/"time"`); `fillna(method=)` is gone |
| 08 | Missing data | Remove and replace | `dropna(how, thresh, subset, axis)`, `replace(-999, np.nan)`, `to_numeric(errors="coerce")`; ints with a gap become float; `Int64` keeps `pd.NA` |
| 09 | Duplicates | Rows | `duplicated(subset, keep="first"/"last"/False)`, `drop_duplicates(subset, keep, ignore_index)`; sort first to choose which row to keep; normalise text before comparing |
| 09 | Duplicates | Counting | `value_counts`, `nunique`, `unique`, `Index.duplicated`, `is_unique` |
| 09 | Duplicates | Labels | `loc[label]` returns several rows; `df[~df.index.duplicated()]`; duplicate columns; `set_flags(allows_duplicate_labels=False)` raises `DuplicateLabelError`; `reindex` fails on duplicates |
| 10 | Worked examples | Patterns | Combine monthly logs, clean text, replace markers, remove duplicates, merge with validation, parse log lines, mask outliers, interpolate, rank and report |