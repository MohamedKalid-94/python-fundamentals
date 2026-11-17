import numpy as np

# TIME DELTAS, INDEXING, ARITHMETIC AND TIME SERIES
#   t2 - t1                  a np.timedelta64            t + np.timedelta64(90, "m")
#   delta / np.timedelta64(1, "h")    a plain float (the number of hours)
#   units W D h m s ms us ns for deltas; Y and M are not fixed lengths and cannot be mixed with days
#   everything works on whole arrays: comparisons, np.diff, np.searchsorted, np.unique, np.bincount

a = np.datetime64("2026-11-15T10:00")
b = np.datetime64("2026-11-15T12:30")
delta = b - a
print(delta, delta / np.timedelta64(1, "h"), delta.astype("timedelta64[s]"), delta.astype(int))
print(a + np.timedelta64(90, "m"), a - np.timedelta64(1, "D"), np.timedelta64(2, "h") * 3, np.timedelta64(90, "m") // np.timedelta64(1, "h"))
print(np.datetime64("2026-11-15") + np.timedelta64(6, "h"))                       # the unit grows to hours
print(np.timedelta64(1, "D") == np.timedelta64(24, "h"))
try:
    np.timedelta64(1, "M") + np.timedelta64(1, "D")                              # a month has no fixed number of days
except TypeError as error:
    print("TypeError:", str(error)[:50])

# An hourly series for three days: the value is the hour of the day (0..23)
ts = np.arange("2026-11-13T00", "2026-11-16T00", dtype="datetime64[h]")
values = np.arange(ts.size) % 24
print(ts.size, ts[0], ts[-1])

# INDEXING with dates
day2 = (ts >= np.datetime64("2026-11-14")) & (ts < np.datetime64("2026-11-15"))
print(day2.sum(), ts[day2][[0, -1]], values[day2][:3])
print(np.searchsorted(ts, np.datetime64("2026-11-14T12")), ts[36])                 # the position of a moment in sorted time
print(ts[24:27], ts[::24])

# TIME SERIES ANALYSIS: group by day, bin by 6 hours, weekdays
days = ts.astype("datetime64[D]")
unique_days, inverse = np.unique(days, return_inverse=True)
daily_mean = np.bincount(inverse, weights=values) / np.bincount(inverse)
print(unique_days, daily_mean)
six_hours = ts.astype("datetime64[6h]")
print(np.unique(six_hours)[:5], np.unique(six_hours).size)
weekday = (days.astype(int) + 3) % 7                                              # 1970-01-01 was a Thursday: Monday = 0
print(weekday[[0, 24, 48]], ["Mon Tue Wed Thu Fri Sat Sun".split()[i] for i in weekday[[0, 24, 48]]])

# Differences and gaps
print(np.diff(ts[:4]), np.diff(ts[:4]).astype(int))
with_gap = np.delete(ts, [10, 11])                                                # two readings are missing
steps = np.diff(with_gap)
print(np.flatnonzero(steps > np.timedelta64(1, "h")), steps.max())
full = np.arange(with_gap[0], with_gap[-1] + np.timedelta64(1, "h"))
position = np.searchsorted(with_gap, full)
present = with_gap[np.minimum(position, with_gap.size - 1)] == full
print(full.size, (~present).sum(), full[~present])                                # the timestamps to fill

# A moving average of the hour-of-day values, and a sampling check
moving = np.convolve(values[:8].astype(float), np.ones(3) / 3, mode="valid")
print(moving)
print(np.diff(ts).min() == np.diff(ts).max())                                     # equally spaced?

# NaT in calculations
dates = np.array(["2026-11-15", "NaT", "2026-11-20"], dtype="datetime64[D]")
print(np.isnat(dates), dates > np.datetime64("2026-11-16"), dates[~np.isnat(dates)].max())

# Durations in a log: elapsed time between events, in seconds
events = np.array(["2026-11-15T10:00:00", "2026-11-15T10:00:30", "2026-11-15T10:02:00"], dtype="datetime64[s]")
print(np.diff(events) / np.timedelta64(1, "s"), (events[-1] - events[0]).astype(int))

# EXPECTED OUTPUT
# 150 minutes 2.5 9000 seconds 150
# 2026-11-15T11:30 2026-11-14T10:00 6 hours 1
# 2026-11-15T06
# True
# TypeError: Cannot get a common metadata divisor for Numpy dat
# 72 2026-11-13T00 2026-11-15T23
# 24 ['2026-11-14T00' '2026-11-14T23'] [0 1 2]
# 36 2026-11-14T12
# ['2026-11-14T00' '2026-11-14T01' '2026-11-14T02'] ['2026-11-13T00' '2026-11-14T00' '2026-11-15T00']
# ['2026-11-13' '2026-11-14' '2026-11-15'] [11.5 11.5 11.5]
# ['2026-11-13T00' '2026-11-13T06' '2026-11-13T12' '2026-11-13T18'
#  '2026-11-14T00'] 12
# [4 5 6] ['Fri', 'Sat', 'Sun']
# [1 1 1] [1 1 1]
# [9] 3 hours
# 72 2 ['2026-11-13T10' '2026-11-13T11']
# [1. 2. 3. 4. 5. 6.]
# True
# [False  True False] [False False  True] 2026-11-20
# [30. 90.] 120