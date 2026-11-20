import tempfile
from pathlib import Path

import openpyxl
import pandas as pd

# EXCEL FILES: pd.read_excel(path, sheet_name=..., ...)  and  df.to_excel(path_or_writer, sheet_name=..., ...)
# Needs a library: openpyxl for .xlsx (installed in this course).  .xls needs xlrd, .ods needs odfpy.
#   READING   sheet_name (name, position, list, or None for ALL sheets as a dict)  header  skiprows  usecols  nrows
#             index_col  dtype  na_values  parse_dates  converters
#   WRITING   sheet_name  index  startrow  startcol  header  na_rep  float_format  freeze_panes  engine
#   pd.ExcelWriter(path)   write SEVERAL sheets in one file     pd.ExcelFile(path).sheet_names   list the sheets
# Formulas are not calculated by pandas: you get the last value stored by Excel, or you write the numbers yourself.

people = pd.DataFrame({"name": ["Ann", "Bo", "Cy"], "age": [25, 31, None], "joined": pd.to_datetime(["2026-01-05", "2026-02-10", "2026-03-15"])})
scores = pd.DataFrame({"name": ["Ann", "Bo"], "score": [9.5, 7.25]})

with tempfile.TemporaryDirectory() as folder:
    path = Path(folder) / "report.xlsx"
    people.to_excel(path, sheet_name="people", index=False, engine="openpyxl")
    back = pd.read_excel(path, sheet_name="people")
    print(back)
    print(back[["name", "age"]].dtypes.astype(str).to_dict(), back["joined"].dt.month.tolist(), pd.api.types.is_datetime64_any_dtype(back["joined"]))
    print(pd.read_excel(path).equals(back), back["age"].isna().tolist())

    # Several sheets in one file
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        people.to_excel(writer, sheet_name="people", index=False)
        scores.to_excel(writer, sheet_name="scores", index=False, startrow=1, startcol=1)
        scores.to_excel(writer, sheet_name="plain", index=True, na_rep="-", float_format="%.1f", freeze_panes=(1, 0))
    book = pd.ExcelFile(path)
    print(book.sheet_names, book.parse("people").shape)
    print(pd.read_excel(path, sheet_name=1, header=1, usecols=[1, 2]).columns.tolist(), pd.read_excel(path, sheet_name="scores", skiprows=1, header=0, usecols="B:C").shape)
    sheets = pd.read_excel(path, sheet_name=None)                                        # every sheet: a dictionary of tables
    print(list(sheets), {name: frame.shape for name, frame in sheets.items()})
    print(pd.read_excel(path, sheet_name="plain", index_col=0)["name"].tolist(), pd.read_excel(path, sheet_name=["people", "plain"]).keys())
    print(pd.read_excel(path, sheet_name="people", nrows=2, usecols=["name", "age"]).shape, pd.read_excel(path, sheet_name="people", dtype={"age": "float64"})["age"].tolist())

    # Add a sheet to an existing file, or replace one
    with pd.ExcelWriter(path, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
        scores.assign(score=scores["score"] * 10).to_excel(writer, sheet_name="scores", index=False)
        pd.DataFrame({"x": [1]}).to_excel(writer, sheet_name="extra", index=False)
    print(pd.ExcelFile(path).sheet_names, pd.read_excel(path, sheet_name="scores")["score"].tolist())

    # Formatting through the library underneath (openpyxl)
    styled = Path(folder) / "styled.xlsx"
    with pd.ExcelWriter(styled, engine="openpyxl") as writer:
        scores.to_excel(writer, sheet_name="s", index=False, freeze_panes=(1, 0))
        sheet = writer.sheets["s"]
        sheet.column_dimensions["A"].width = 20
        sheet["B1"].font = openpyxl.styles.Font(bold=True)
    workbook = openpyxl.load_workbook(styled)
    worksheet = workbook["s"]
    print(worksheet.freeze_panes, worksheet.column_dimensions["A"].width, worksheet["B1"].font.bold, worksheet["A1"].value)

    # Reading a workbook with formulas: the value is what Excel saved (a file written by openpyxl has none yet)
    formulas = Path(folder) / "formulas.xlsx"
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.append(["a", "b", "total"])
    sheet.append([1, 2, "=A2+B2"])
    workbook.save(formulas)
    print(pd.read_excel(formulas).iloc[0].tolist())
    print(openpyxl.load_workbook(formulas)["Sheet"]["C2"].value)

# Excel limits to remember: 1,048,576 rows, 16,384 columns, and dates before 1900 do not exist
print(1_048_576, 16_384)

# EXPECTED OUTPUT
#   name   age     joined
# 0  Ann  25.0 2026-01-05
# 1   Bo  31.0 2026-02-10
# 2   Cy   NaN 2026-03-15
# {'name': 'str', 'age': 'float64'} [1, 2, 3] True
# True [False, False, True]
# ['people', 'scores', 'plain'] (3, 3)
# ['name', 'score'] (2, 2)
# ['people', 'scores', 'plain'] {'people': (3, 3), 'scores': (3, 3), 'plain': (2, 3)}
# ['Ann', 'Bo'] dict_keys(['people', 'plain'])
# (2, 2) [25.0, 31.0, nan]
# ['people', 'scores', 'plain', 'extra'] [95.0, 72.5]
# A2 20.0 True name
# [1.0, 2.0, nan]
# =A2+B2
# 1048576 16384