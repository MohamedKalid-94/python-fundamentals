import io

import numpy as np
import pandas as pd

# WORKED EXAMPLES that combine the lessons of this module

# 1. Two monthly logs from several devices: concatenate, clean the text, handle markers and duplicates, merge with a device table
jan = "device,time,temp,site\nd1,2026-01-01 00:00,20.5, North \nd1,2026-01-01 01:00,,North\nd2,2026-01-01 00:00,18.0,south\nd2,2026-01-01 00:00,18.0,south\n"
feb = "device,time,temp,site\nd1,2026-02-01 00:00,21.5,north\nd3,2026-02-01 00:00,25.0,EAST\nd2,2026-02-01 00:00,-999,South\n"
frames = [pd.read_csv(io.StringIO(text), parse_dates=["time"]) for text in (jan, feb)]
log = pd.concat(frames, keys=["jan", "feb"], names=["month", "row"]).reset_index(level="month")
print(log.shape, log["site"].unique().tolist())
log["site"] = log["site"].str.strip().str.title()
log["temp"] = log["temp"].replace(-999, np.nan)
log = log.drop_duplicates(["device", "time"]).reset_index(drop=True)
print(log.shape, log["site"].value_counts().sort_index().to_dict(), int(log["temp"].isna().sum()))
devices = pd.DataFrame({"device": ["d1", "d2", "d4"], "owner": ["Ann", "Bo", "Cy"]})
report = log.merge(devices, on="device", how="left", indicator=True, validate="many_to_one")
print(report[["device", "owner"]].values.tolist(), report["_merge"].astype(str).value_counts().sort_index().to_dict())
print(report.loc[report["owner"].isna(), "device"].tolist(), devices[~devices["device"].isin(log["device"])]["device"].tolist())
filled = log["temp"].fillna(log.groupby("device")["temp"].transform("mean"))                  # a preview of groupby (Module 32)
print(filled.round(2).tolist())

# 2. Parse text log lines, convert, mask bad values, smooth
lines = pd.Series([
    "2026-11-15 10:00:00 sensor=a value=21.5", "2026-11-15 10:00:05 sensor=b value=19.0", "2026-11-15 10:00:10 sensor=a value=21.7",
    "2026-11-15 10:00:15 sensor=a value=99.9", "2026-11-15 10:00:20 sensor=b value=19.2", "2026-11-15 10:00:25 sensor=a value=21.9",
    "2026-11-15 10:00:30 sensor=a value=err", "2026-11-15 10:00:35 sensor=a value=22.0",
])
data = lines.str.extract(r"^(?P<time>\S+ \S+) sensor=(?P<sensor>\w+) value=(?P<value>\S+)$")
data["time"] = pd.to_datetime(data["time"])
data["value"] = pd.to_numeric(data["value"], errors="coerce")
print(data["value"].isna().sum(), data["sensor"].value_counts().sort_index().to_dict(), data["value"].describe().round(2).to_dict())
a = data[data["sensor"] == "a"].set_index("time")["value"]
q1, q3 = a.quantile([0.25, 0.75])
bad = (a < q1 - 1.5 * (q3 - q1)) | (a > q3 + 1.5 * (q3 - q1))
print(a.tolist(), bad.tolist())
clean = a.mask(bad).interpolate(method="time")
print(clean.round(2).tolist(), clean.rolling("20s").mean().round(2).tolist())
print(round(a.mean(), 2), round(clean.mean(), 2), round(a.median(), 2), round(clean.median(), 2))

# 3. Customers and orders from two sources: normalise the keys, find duplicates, merge safely, add statistics
customers = pd.DataFrame({"email": ["Ann@x.com", " bo@x.com", "ann@x.com ", "cy@x.com"], "name": ["Ann", "Bo", "Ann L.", "Cy"]})
customers["email"] = customers["email"].str.strip().str.lower()
print(customers["email"].duplicated().sum(), customers.drop_duplicates("email", keep="last")["name"].tolist())
unique_customers = customers.drop_duplicates("email", keep="last")
orders = pd.DataFrame({"email": ["ann@x.com", "bo@x.com", "ann@x.com", "dee@x.com"], "total": [10.0, 5.5, 7.0, 3.0]})
joined = orders.merge(unique_customers, on="email", how="left", validate="many_to_one")
print(joined[["email", "name", "total"]].values.tolist())
print(joined["name"].isna().sum(), joined["total"].sum(), joined.loc[joined["name"].notna(), "total"].agg(["count", "sum", "mean"]).round(2).to_dict())
print(joined.sort_values("total", ascending=False).head(2)["email"].tolist(), joined["total"].rank(ascending=False).tolist())

# 4. A report table: statistics, ranks and a formatted text
scores = pd.DataFrame({"team": list("ABCDE"), "points": [31, 25, 31, 18, 27], "games": [10, 9, 12, 8, 10]})
scores["per_game"] = (scores["points"] / scores["games"]).round(2)
scores["rank"] = scores["per_game"].rank(ascending=False, method="min").astype(int)
print(scores.sort_values("rank")[["team", "per_game", "rank"]].values.tolist())
print(scores[["points", "games"]].describe().loc[["mean", "std", "max"]].round(2).values.tolist(), scores["points"].corr(scores["games"]).round(3))
print(scores.sort_values("rank").assign(line=lambda d: d["team"] + ": " + d["per_game"].map("{:.2f}".format))["line"].tolist())

# EXPECTED OUTPUT
# (7, 5) [' North ', 'North', 'south', 'north', 'EAST', 'South']
# (6, 5) {'East': 1, 'North': 3, 'South': 2} 2
# [['d1', 'Ann'], ['d1', 'Ann'], ['d2', 'Bo'], ['d1', 'Ann'], ['d3', nan], ['d2', 'Bo']] {'both': 5, 'left_only': 1}
# ['d3'] ['d4']
# [20.5, 21.0, 18.0, 21.5, 25.0, 18.0]
# 1 {'a': 6, 'b': 2} {'count': 7.0, 'mean': 32.17, 'std': 29.89, 'min': 19.0, '25%': 20.35, '50%': 21.7, '75%': 21.95, 'max': 99.9}
# [21.5, 21.7, 99.9, 21.9, nan, 22.0] [False, False, True, False, False, False]
# [21.5, 21.7, 21.77, 21.9, 21.95, 22.0] [21.5, 21.6, 21.66, 21.79, 21.87, 21.95]
# 37.4 21.8 21.9 21.83
# 1 ['Bo', 'Ann L.', 'Cy']
# [['ann@x.com', 'Ann L.', 10.0], ['bo@x.com', 'Bo', 5.5], ['ann@x.com', 'Ann L.', 7.0], ['dee@x.com', nan, 3.0]]
# 1 25.5 {'count': 3.0, 'sum': 22.5, 'mean': 7.5}
# ['ann@x.com', 'ann@x.com'] [1.0, 3.0, 2.0, 4.0]
# [['A', 3.1, 1], ['B', 2.78, 2], ['E', 2.7, 3], ['C', 2.58, 4], ['D', 2.25, 5]]
# [[26.4, 9.8], [5.37, 1.48], [31.0, 12.0]] 0.861
# ['A: 3.10', 'B: 2.78', 'E: 2.70', 'C: 2.58', 'D: 2.25']