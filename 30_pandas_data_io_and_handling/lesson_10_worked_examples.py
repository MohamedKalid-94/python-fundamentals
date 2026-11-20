import io
import sqlite3
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

# WORKED EXAMPLES that combine the lessons of this module

# 1. A small ETL job: extract (CSV text), transform (clean, derive), load (CSV, JSON Lines, Excel, SQLite)
raw = """# log from device 7
time;channel;counts;note
2026-11-15 10:00:00;a;512;ok
2026-11-15 10:00:10;b;4095;clipped
2026-11-15 10:00:20;a;530;ok
2026-11-15 10:00:30;b;;missing
2026-11-15 10:00:40;a;548;ok
"""
log = pd.read_csv(io.StringIO(raw), sep=";", comment="#", parse_dates=["time"], dtype={"channel": "str"})
log["volts"] = (log["counts"] * 3.3 / 4095).round(3)
log["valid"] = log["counts"].between(1, 4094)
clean = log[log["valid"]].sort_values("time").reset_index(drop=True)
print(clean[["channel", "counts", "volts"]])
print(len(log), len(clean), int(log["counts"].isna().sum()), log.loc[~log["valid"], "note"].tolist())

with tempfile.TemporaryDirectory() as folder:
    folder = Path(folder)
    clean.to_csv(folder / "clean.csv", index=False)
    clean.to_json(folder / "clean.jsonl", orient="records", lines=True, date_format="iso")
    clean.to_excel(folder / "clean.xlsx", index=False, engine="openpyxl")
    conn = sqlite3.connect(folder / "clean.db")
    clean.to_sql("clean", conn, index=False)
    loaded = {
        "csv": pd.read_csv(folder / "clean.csv", parse_dates=["time"]),
        "jsonl": pd.read_json(folder / "clean.jsonl", lines=True, convert_dates=["time"], precise_float=True),   # exact decimal numbers
        "excel": pd.read_excel(folder / "clean.xlsx", engine="openpyxl"),
        "sqlite": pd.read_sql_query("SELECT * FROM clean", conn, parse_dates=["time"]),
    }
    conn.close()
    for name, frame in loaded.items():
        print(f"{name:<7}", frame.shape, frame["volts"].tolist() == clean["volts"].tolist(), frame["time"].dt.second.tolist())

# 2. A dataset of prompts as JSON Lines (the usual format for language-model data): filter, sort, save, reload
prompts = pd.DataFrame({
    "id": range(1, 7),
    "prompt": ["Explain DNS", "What is TCP?", "Define UART in two lines", "Summarise the SPI protocol for a beginner", "Hi", "Compare I2C and SPI"],
    "label": ["net", "net", "emb", "emb", "chat", "emb"],
})
prompts["words"] = prompts["prompt"].str.split().str.len()
keep = prompts[prompts["words"] >= 3].sort_values(["label", "words"], ascending=[True, False]).reset_index(drop=True)
jsonl = keep.to_json(orient="records", lines=True)
print(len(jsonl.splitlines()), jsonl.splitlines()[0])
back = pd.read_json(io.StringIO(jsonl), lines=True)
print(back.equals(keep), back["label"].value_counts().to_dict(), back["words"].agg(["min", "max", "mean"]).round(2).to_dict())

# 3. A time series with gaps: sort, reindex to every hour, interpolate
messy = pd.DataFrame({"time": pd.to_datetime(["2026-11-15 13:00", "2026-11-15 10:00", "2026-11-15 11:00", "2026-11-15 15:00"]), "temp": [24.0, 21.0, 22.0, 26.0]})
series = messy.sort_values("time").set_index("time")["temp"]
hourly = series.reindex(pd.date_range(series.index.min(), series.index.max(), freq="h"))
print(hourly.isna().sum(), hourly.interpolate().round(2).tolist(), hourly.ffill().tolist())
print(hourly.index[hourly.isna()].strftime("%H:%M").tolist(), series.index.is_monotonic_increasing)

# 4. Decoding a status byte: apply with a Python function against the vectorized bit tests
status = pd.DataFrame({"id": [1, 2, 3, 4], "flags": [0b0001, 0b0110, 0b1000, 0b1111]})


def describe(flags):
    names = []
    if flags & 0b0001:
        names.append("ready")
    if flags & 0b0010:
        names.append("error")
    if flags & 0b0100:
        names.append("overrun")
    if flags & 0b1000:
        names.append("busy")
    return ",".join(names) or "idle"


status["text"] = status["flags"].map(describe)
status["error"] = (status["flags"] & 0b0010) != 0
status["bits"] = status["flags"].map(lambda value: bin(value).count("1"))
print(status)
print(status.loc[status["error"], "id"].tolist(), status["flags"].map(describe).eq(status["text"]).all())

# 5. The same question in SQL and in pandas, on the same data
conn = sqlite3.connect(":memory:")
sales = pd.DataFrame({"shop": ["A", "A", "B", "B", "B"], "item": ["pen", "ink", "pen", "pen", "cap"], "qty": [3, 1, 4, 2, 6], "price": [1.5, 4.0, 1.5, 1.5, 3.0]})
sales.to_sql("sales", conn, index=False)
by_sql = pd.read_sql_query("SELECT shop, SUM(qty * price) AS revenue FROM sales GROUP BY shop ORDER BY revenue DESC", conn)
by_pandas = sales.assign(revenue=sales["qty"] * sales["price"]).groupby("shop", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False).reset_index(drop=True)
print(by_sql.values.tolist(), by_sql.equals(by_pandas))
conn.close()

# EXPECTED OUTPUT
#   channel  counts  volts
# 0       a   512.0  0.413
# 1       a   530.0  0.427
# 2       a   548.0  0.442
# 5 3 1 ['clipped', 'missing']
# csv     (3, 6) True [0, 20, 40]
# jsonl   (3, 6) True [0, 20, 40]
# excel   (3, 6) True [0, 20, 40]
# sqlite  (3, 6) True [0, 20, 40]
# 4 {"id":4,"prompt":"Summarise the SPI protocol for a beginner","label":"emb","words":7}
# True {'emb': 3, 'net': 1} {'min': 3.0, 'max': 7.0, 'mean': 4.75}
# 2 [21.0, 22.0, 23.0, 24.0, 25.0, 26.0] [21.0, 22.0, 22.0, 24.0, 24.0, 26.0]
# ['12:00', '14:00'] True
#    id  flags                      text  error  bits
# 0   1      1                     ready  False     1
# 1   2      6             error,overrun   True     2
# 2   3      8                      busy  False     1
# 3   4     15  ready,error,overrun,busy   True     4
# [2, 4] True
# [['B', 27.0], ['A', 8.5]] True