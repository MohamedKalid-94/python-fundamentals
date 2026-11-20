# Module 30: pandas IO Tools and Data Handling (part 1), Concepts Summary

| # | Topic | Concept | Remember |
|---|---|---|---|
| 01 | CSV | Reading | `read_csv`: `sep`, `header`, `names`, `usecols`, `index_col`, `dtype`, `converters`, `parse_dates`, `na_values`, `true_values`, `comment`, `decimal`, `thousands`, `nrows`, `skiprows`, `encoding` |
| 01 | CSV | Pitfalls | Leading zeros are lost unless `dtype=str`; dates stay text unless `parse_dates`; sentinels such as `-999` need `na_values`; use `chunksize` for big files |
| 01 | CSV | Writing | `to_csv(index=False, float_format=, na_rep=, sep=, columns=, header=, mode="a", compression=)`; the `.gz` extension compresses |
| 02 | JSON | Orients | `columns`, `records`, `index`, `split`, `values`, `table`; `lines=True` is JSON Lines (one object per line, for big data and LLM datasets) |
| 02 | JSON | Nested data | `pd.json_normalize(data, record_path=, meta=, sep=, max_level=)` flattens nested dictionaries and lists |
| 02 | JSON | Dates and text | `date_format="iso"` (the epoch default is deprecated), `convert_dates=["col"]` when reading, `force_ascii=False`, `precise_float=True` for exact decimals |
| 03 | Excel | Reading | `read_excel(sheet_name=name / position / list / None, header, skiprows, usecols, nrows, index_col, dtype)`; `ExcelFile.sheet_names` |
| 03 | Excel | Writing | `to_excel`, `ExcelWriter` for several sheets, `mode="a"` with `if_sheet_exists`, `startrow`, `startcol`, `freeze_panes`; formatting through `openpyxl`; formulas are not calculated |
| 04 | HTML | Tables | `read_html(StringIO(...))` returns a list of tables (`match=`, `attrs=`); `to_html` |
| 04 | SQL | sqlite3 | `to_sql(name, conn, if_exists="fail"/"replace"/"append")`, `read_sql_query(sql, conn, params=, index_col=, chunksize=)`; `?` parameters avoid injection |
| 04 | Other | Formats | Pickle (Python only, trusted files only), `read_fwf`, `to_markdown`, `to_string`; clipboard, HDF5, Parquet and Feather need extra packages or a desktop (not run here) |
| 05 | SQL comparison | Mapping | `SELECT` is `df[[...]]`, `WHERE` is a mask or `query`, `ORDER BY` is `sort_values`, `LIMIT` is `head`, `DISTINCT` is `drop_duplicates`, `JOIN` is `merge`, `UNION ALL` is `concat`, `CASE` is `np.where`, `GROUP BY` is `groupby` |
| 05 | SQL comparison | NULL | In SQL a comparison with `NULL` is unknown, so the row is dropped; in pandas `NaN > x` is `False` and `~False` is `True`: test `notna()` yourself |
| 06 | Sorting | `sort_values` | `by=` (list), `ascending=` (list), `na_position`, `ignore_index`, `key=` (case-insensitive or custom order), `kind="stable"` for ties |
| 06 | Sorting | Others | `sort_index(axis=)`, `nlargest`, `nsmallest(keep=)`, `rank(method=, pct=)`, `argsort`, `searchsorted` on a sorted Series; sort dates as dates, not text |
| 07 | Reindexing | `reindex` | New labels give `NaN` (or `fill_value`); `columns=` forces a schema; `method="ffill"/"bfill"/"nearest"` needs a sorted index; duplicates raise `ValueError` |
| 07 | Reindexing | Related | `reindex_like`, `align(join=)`, `set_axis`, `rename`, `reset_index`; `loc` with a missing label raises `KeyError`, `reindex` does not |
| 07 | Reindexing | Time series | Reindex to a full `date_range`, then `interpolate()`, `ffill()` or `fillna()` |
| 08 | Iteration | Tools | `for col in df`, `items()`, `iterrows()` (slow, one dtype per row), `itertuples()` (faster, keeps types), `zip(...)`, `to_dict("records")` |
| 08 | Iteration | Advice | Prefer vectorized operations; loops are for steps that depend on the previous one; changing the row in a loop does not change the table |
| 09 | Function application | Tools | `Series.map` (dict or function), `DataFrame.map` (the old `applymap` is gone), `apply(axis=0/1)`, `pipe`, `eval`, `assign` |
| 09 | Aggregations | `agg` | Names, lists or a dict per column; named aggregation `agg(total=("a", "sum"))`; `transform` keeps the shape (centering, scaling, `cumsum`, `rank`) |