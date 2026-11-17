import datetime
import warnings

import numpy as np

# DATE AND TIME BASICS: np.datetime64 and np.timedelta64
#   np.datetime64("2026-11-15")            a date (unit D)           np.datetime64("2026-11-15T10:30:45")   unit s
#   units: Y (year) M (month) W (week) D (day) h m s ms us ns      the unit comes from the text, or from dtype="datetime64[h]"
#   everything is stored as an integer count of units since 1970-01-01T00:00 (the "epoch")
#   np.datetime_data, astype (change the unit), np.arange (date ranges), np.datetime_as_string
#   business days: np.is_busday  np.busday_count  np.busday_offset         NaT = "not a time" (a missing date)
# NumPy has NO time zones and ignores leap seconds: see the end of this lesson.

d = np.datetime64("2026-11-15")
t = np.datetime64("2026-11-15T10:30:45")
print(d, d.dtype, t, t.dtype, np.datetime64("2026-11"), np.datetime64("2026-11").dtype)
print(np.datetime_data(d.dtype), np.datetime_data(t.dtype))
print(d.astype(int), np.datetime64(0, "s"), np.datetime64(20_000, "D"))          # days since 1970-01-01

arr = np.array(["2026-11-15", "2026-11-16", "2026-12-25"], dtype="datetime64[D]")
print(arr, arr.dtype)
print(arr.astype("datetime64[M]"), arr.astype("datetime64[Y]"), arr.astype("datetime64[h]")[0])
print(np.datetime_as_string(t, unit="m"), str(t)[:10], np.datetime_as_string(arr))

# Date ranges
print(np.arange("2026-11-01", "2026-11-06", dtype="datetime64[D]"))
print(np.arange(np.datetime64("2026-11-01"), np.datetime64("2026-12-01"), np.timedelta64(7, "D")))
print(np.arange("2026-11-15T00", "2026-11-15T04", dtype="datetime64[h]"))

# Python datetime objects
dt = datetime.datetime(2026, 11, 15, 10, 30)
print(np.datetime64(dt), np.datetime64(dt).astype(datetime.datetime), np.datetime64("2026-11-15").item())
print(np.array([1_760_000_000]).astype("datetime64[s]"))                         # Unix timestamps in seconds

# Business days (Monday to Friday, with optional holidays)
print(np.busday_count("2026-11-01", "2026-12-01"), np.is_busday(["2026-11-14", "2026-11-16"]))
print(np.busday_offset("2026-11-13", 1), np.busday_offset("2026-11-14", 0, roll="forward"))
print(np.busday_count("2026-11-01", "2026-12-01", holidays=["2026-11-26"]))

# Not a time
missing = np.array(["2026-11-15", "NaT"], dtype="datetime64[D]")
print(missing, np.isnat(missing), missing[1] == missing[1])

# Leap years are handled
print(np.datetime64("2028-02-28") + np.timedelta64(2, "D"), np.datetime64("2027-02-28") + np.timedelta64(2, "D"))

# TIME ZONES: there are none. A string with an offset is converted to UTC, with a warning.
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    utc = np.datetime64("2026-11-15T10:00+0530")
print(utc, caught[0].category.__name__)
local = utc + np.timedelta64(330, "m")                       # show it again as India time: add the offset yourself
print(local)
# Advice: store and calculate in UTC with NumPy; convert to local time only for display,
# with datetime and zoneinfo, or with pandas (Module 31), which supports real time zones.

# LEAP SECONDS: not represented. Every day has exactly 86400 seconds.
try:
    np.datetime64("2016-12-31T23:59:60")
except ValueError as error:
    print("ValueError:", str(error)[:40])
gap = np.datetime64("2017-01-01T00:00:00") - np.datetime64("2016-12-31T23:59:59")
print(gap)                                                    # 1 second here; UTC really took 2 seconds (a leap second)

# EXPECTED OUTPUT
# 2026-11-15 datetime64[D] 2026-11-15T10:30:45 datetime64[s] 2026-11 datetime64[M]
# ('D', 1) ('s', 1)
# 20772 1970-01-01T00:00:00 2024-10-04
# ['2026-11-15' '2026-11-16' '2026-12-25'] datetime64[D]
# ['2026-11' '2026-11' '2026-12'] ['2026' '2026' '2026'] 2026-11-15T00
# 2026-11-15T10:30 2026-11-15 ['2026-11-15' '2026-11-16' '2026-12-25']
# ['2026-11-01' '2026-11-02' '2026-11-03' '2026-11-04' '2026-11-05']
# ['2026-11-01' '2026-11-08' '2026-11-15' '2026-11-22' '2026-11-29']
# ['2026-11-15T00' '2026-11-15T01' '2026-11-15T02' '2026-11-15T03']
# 2026-11-15T10:30:00.000000 2026-11-15 10:30:00 2026-11-15
# ['2025-10-09T08:53:20']
# 21 [False  True]
# 2026-11-16 2026-11-16
# 20
# ['2026-11-15'        'NaT'] [False  True] False
# 2028-03-01 2027-03-02
# 2026-11-15T04:30 UserWarning
# 2026-11-15T10:00
# ValueError: Seconds out of range in datetime string
# 1 seconds