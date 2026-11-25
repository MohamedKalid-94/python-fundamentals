import numpy as np
import pandas as pd

# OPTIONS AND CUSTOMIZATION: how tables are DISPLAYED (the data never change)
#   pd.get_option("name")   pd.set_option("name", value)   pd.reset_option("name")   pd.describe_option("pattern")
#   with pd.option_context("name", value, ...):   a temporary change (restored when the block ends): the safe way
#   pd.options.display.max_rows = 5               the same with attribute access
#   the useful ones: display.max_rows  display.max_columns  display.width  display.max_colwidth  display.precision
#                    display.float_format  display.show_dimensions  display.expand_frame_repr  display.chop_threshold
#   df.to_string(...)  and  df.style  (a Styler) format a table for a report; the Styler needs jinja2

print(pd.get_option("display.max_rows"), pd.get_option("display.max_columns"), pd.get_option("display.width"), pd.get_option("display.max_colwidth"), pd.get_option("display.precision"))

df = pd.DataFrame({"a": range(10), "b": np.arange(10) / 3})
with pd.option_context("display.max_rows", 4):
    print(df)
with pd.option_context("display.max_rows", 4, "display.show_dimensions", False):
    print(df.shape, len(repr(df).splitlines()))
with pd.option_context("display.precision", 2):
    print(df.head(3))
with pd.option_context("display.float_format", "{:,.1f}".format):
    print(pd.DataFrame({"x": [1234.5678, 0.04], "y": [1e6, 2.5]}))
with pd.option_context("display.float_format", lambda v: f"{v:.2e}"):
    print(pd.Series([12345.678, 0.00012]))
print(pd.get_option("display.precision"))                                          # restored after the blocks

# Wide tables and long text
wide = pd.DataFrame(np.arange(30).reshape(2, 15), columns=[f"column_{i}" for i in range(15)])
with pd.option_context("display.max_columns", 4):
    print(wide)
with pd.option_context("display.width", 200, "display.max_columns", None):
    print(len(repr(wide).splitlines()))
with pd.option_context("display.expand_frame_repr", False, "display.max_columns", None):
    print(len(repr(wide).splitlines()[0]) > 80)
text = pd.DataFrame({"note": ["a" * 60]})
with pd.option_context("display.max_colwidth", 20):
    print(text)
with pd.option_context("display.chop_threshold", 0.5):
    print(pd.Series([0.1, 1.0, -0.2]).tolist(), repr(pd.Series([0.1, 1.0, -0.2])).splitlines()[0])

# Setting and resetting
pd.set_option("display.max_rows", 3)
print(len(repr(df).splitlines()), pd.get_option("display.max_rows"))
pd.reset_option("display.max_rows")
print(pd.get_option("display.max_rows"), len(repr(df).splitlines()))
pd.options.display.precision = 3
print(pd.options.display.precision, repr(pd.Series([1 / 3])).splitlines()[0])
pd.reset_option("display.precision")
try:
    pd.set_option("display.no_such_option", 1)
except Exception as error:
    print(type(error).__name__)
print("display.max_rows" in pd.describe_option("display.max_rows", _print_desc=False))

# The same formatting for a single table, without touching the options: to_string
frame = pd.DataFrame({"name": ["Ann", "Bo"], "kg": [55.456, np.nan], "ok": [True, False]})
print(frame.to_string(index=False, float_format="{:.1f}".format, na_rep="-"))
print(frame.to_string(max_rows=1).splitlines())
print(frame.to_string(header=False, index=False).splitlines()[0])
print(frame.round(1).to_string(columns=["name", "kg"], justify="left", col_space=6).splitlines()[0])

# Styles for reports (jinja2): format numbers, highlight values, hide the index
styled = frame.style.format({"kg": "{:.1f}"}, na_rep="n/a").hide(axis="index").highlight_max(subset=["kg"], color="yellow")
html = styled.to_html()
print("55.5" in html, "n/a" in html, "background-color: yellow" in html, "<table" in html)
print(frame.style.format(precision=1, na_rep="-").to_html().count("<td"), frame.style.set_caption("Weights").to_html().count("Weights"))
print(frame.style.map(lambda v: "color: red" if v is True else "", subset=["ok"]).to_html().count("color: red"))
print(frame.to_html(float_format="{:.1f}".format, na_rep="-").count("<td>"), frame.to_html(index=False, na_rep="-").count("-"))

# Number formatting by hand: display strings, keep the numbers
money = pd.Series([1234567.891, 42.0])
print(money.map("{:,.2f}".format).tolist(), (money / 1e6).map("{:.1f}M".format).tolist(), money.round(-2).tolist())

# EXPECTED OUTPUT
# 60 0 80 50 6
#     a         b
# 0   0  0.000000
# 1   1  0.333333
# .. ..       ...
# 8   8  2.666667
# 9   9  3.000000
#
# [10 rows x 2 columns]
# (10, 2) 6
#    a     b
# 0  0  0.00
# 1  1  0.33
# 2  2  0.67
#         x           y
# 0 1,234.6 1,000,000.0
# 1     0.0         2.5
# 0   1.23e+04
# 1   1.20e-04
# dtype: float64
# 6
#    column_0  column_1  ...  column_13  column_14
# 0         0         1  ...         13         14
# 1        15        16  ...         28         29
#
# [2 rows x 15 columns]
# 3
# True
#                   note
# 0  aaaaaaaaaaaaaaaa...
# [0.1, 1.0, -0.2] 0    0.0
# 6 3
# 60 11
# 3 0    0.333
# OptionError
# True
# name   kg    ok
#  Ann 55.5  True
#   Bo    - False
# ['   name      kg    ok', '0   Ann  55.456  True', '..  ...     ...   ...']
# Ann 55.456  True
#        name    kg
# True True True True
# 6 1
# 1
# 6 2
# ['1,234,567.89', '42.00'] ['1.2M', '0.0M'] [1234600.0, 0.0]