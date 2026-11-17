import io
import struct
import tempfile
from pathlib import Path

import numpy as np

# WORKED EXAMPLES that combine the lessons of this module

# 1. A binary sensor log: 8-byte packets  [time u32][channel u8][value i16][flags u8], little endian
packet = np.dtype([("t", "<u4"), ("ch", "u1"), ("value", "<i2"), ("flags", "u1")])
records = [(1000, 0, 215, 0), (1010, 1, -40, 1), (1020, 0, 218, 0), (1030, 1, -38, 0), (1040, 0, -999, 2), (1050, 1, -36, 0)]
raw = b"".join(struct.pack("<IBhB", *r) for r in records)
log = np.frombuffer(raw, dtype=packet)
print(log.shape, log.itemsize, len(raw))
value = np.where(log["value"] == -999, np.nan, log["value"] / 10.0)          # tenths of a degree; -999 means "error"
print(value)
for channel in (0, 1):
    chosen = log["ch"] == channel
    print(channel, round(float(np.nanmean(value[chosen])), 2), float(np.nanmax(value[chosen])))
print(log["t"][log["flags"] > 0])
with tempfile.TemporaryDirectory() as folder:
    path = Path(folder) / "log.npz"
    np.savez_compressed(path, log=log)
    with np.load(path) as archive:
        back = archive["log"]
print(back.dtype == log.dtype, np.array_equal(back, log))

# 2. Repair a time series (missing values), then average it per hour
start = np.datetime64("2026-11-15T00:00:00")
seconds = np.arange(0, 3 * 3600, 600)                                         # a sample every 10 minutes for 3 hours
times = start + seconds * np.timedelta64(1, "s")
temps = 20.0 + seconds / 3600.0
temps[[4, 5, 11]] = np.nan                                                    # three samples were lost
good = ~np.isnan(temps)
filled = np.interp(seconds, seconds[good], temps[good])
print(np.round(filled[3:7], 3))
hours = times.astype("datetime64[h]")
unique_hours, inverse = np.unique(hours, return_inverse=True)
hourly = np.bincount(inverse, weights=filled) / np.bincount(inverse)
print(unique_hours, np.round(hourly, 3))

# 3. The dominant frequencies of a vibration, and a low-pass filter
fs = n = 2000
tt = np.arange(n) / fs
vibration = np.sin(2 * np.pi * 120 * tt) + 0.3 * np.sin(2 * np.pi * 360 * tt) + 0.1 * np.sin(2 * np.pi * 31 * tt)
amplitude = 2 * np.abs(np.fft.rfft(vibration)) / n
frequencies = np.fft.rfftfreq(n, 1 / fs)
top = np.argsort(amplitude)[-3:][::-1]
print(frequencies[top], np.round(amplitude[top], 3))
spectrum = np.fft.rfft(vibration)
spectrum[frequencies > 200] = 0
smooth = np.fft.irfft(spectrum, n=n)
print(np.allclose(smooth, np.sin(2 * np.pi * 120 * tt) + 0.1 * np.sin(2 * np.pi * 31 * tt)))

# 4. A text log: parse, group by kind, and find the gaps in time
text = ("2026-11-15T10:00:00,temp,21.5\n2026-11-15T10:00:10,hum,40.0\n2026-11-15T10:00:20,temp,21.7\n"
        "2026-11-15T10:01:30,temp,21.9\n2026-11-15T10:01:40,hum,41.0\n")
rows = np.genfromtxt(io.StringIO(text), delimiter=",", dtype=None, encoding="utf-8", names=["time", "kind", "value"])
moments = rows["time"].astype("datetime64[s]")
print(rows.dtype.names, moments[0], rows["kind"])
for kind in np.unique(rows["kind"]):
    print(kind, round(float(rows["value"][rows["kind"] == kind].mean()), 2))
gaps = np.diff(moments) / np.timedelta64(1, "s")
print(gaps, moments[1:][gaps > 30])

# 5. Clean the labels, then count them
labels = np.array([" Cat", "dog ", "CAT", "Dog", "bird", "cat "])
cleaned = np.strings.lower(np.strings.strip(labels))
values, counts = np.unique(cleaned, return_counts=True)
print(dict(zip(values.tolist(), counts.tolist())))

# EXPECTED OUTPUT
# (6,) 8 48
# [21.5 -4.  21.8 -3.8  nan -3.6]
# 0 21.65 21.8
# 1 -3.8 -3.6
# [1010 1040]
# True True
# [20.5   20.667 20.833 21.   ]
# ['2026-11-15T00' '2026-11-15T01' '2026-11-15T02'] [20.417 21.417 22.417]
# [120. 360.  31.] [1.  0.3 0.1]
# True
# ('time', 'kind', 'value') 2026-11-15T10:00:00 ['temp' 'hum' 'temp' 'temp' 'hum']
# hum 40.5
# temp 21.7
# [10. 10. 70. 10.] ['2026-11-15T10:01:30']
# {'bird': 1, 'cat': 3, 'dog': 2}