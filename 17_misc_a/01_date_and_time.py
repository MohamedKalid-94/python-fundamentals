import calendar
import time
from datetime import date, datetime, timedelta, timezone
from datetime import time as dtime

# ---------- 1. The time module: seconds since the "epoch" (1970-01-01 00:00:00 UTC) ----------
print(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(0)))       # 1970-01-01 00:00:00
print(time.strftime("%H:%M:%S", time.gmtime(3661)))             # 01:01:01
print(calendar.timegm(time.gmtime(86400)))                      # 86400
print(isinstance(time.time(), float))                           # True    seconds since the epoch

# Measure a duration with perf_counter (it never jumps when the clock is adjusted)
t0 = time.perf_counter()
time.sleep(0.05)
print(time.perf_counter() - t0 >= 0.04)                         # True

# ---------- 2. date, time and datetime ----------
d = date(2026, 11, 10)
print(d, d.year, d.month, d.day)                # 2026-11-10 2026 11 10
print(d.weekday(), d.isoweekday(), d.strftime("%A"))            # 1 2 Tuesday   (Monday is 0 / 1)
print(d.isoformat(), d.replace(day=1))          # 2026-11-10 2026-11-01
print(isinstance(date.today(), date))           # True

t = dtime(14, 30, 15)
print(t, t.hour)                                # 14:30:15 14

dt = datetime(2026, 11, 10, 14, 30, 15)
print(dt)                                       # 2026-11-10 14:30:15
print(dt.isoformat())                           # 2026-11-10T14:30:15
print(dt.date(), dt.time())                     # 2026-11-10 14:30:15
print(datetime.combine(d, t))                   # 2026-11-10 14:30:15
# datetime.now() and date.today() give the current moment (not used here, so the output stays fixed)

# ---------- 3. timedelta: a duration ----------
delta = timedelta(days=1, hours=2, minutes=30)
print(delta, delta.total_seconds())             # 1 day, 2:30:00 95400.0
print(dt + timedelta(days=30))                  # 2026-12-10 14:30:15
print(dt - timedelta(hours=15))                 # 2026-11-09 23:30:15
print((date(2026, 12, 25) - d).days)            # 45       date - date gives a timedelta
print(timedelta(seconds=3725))                  # 1:02:05
print(timedelta(days=-1, hours=23) == timedelta(hours=-1))      # True
print(date(2026, 1, 1) < d, max(date(2026, 1, 1), d))           # True 2026-11-10

# ---------- 4. Formatting with strftime ----------
#   %Y year  %m month  %d day  %H hour(24)  %I hour(12)  %M minute  %S second
#   %A weekday name  %a short  %B month name  %b short  %p AM/PM  %j day of the year
print(dt.strftime("%d/%m/%Y %H:%M"))            # 10/11/2026 14:30
print(dt.strftime("%A, %B %d, %Y"))             # Tuesday, November 10, 2026
print(dt.strftime("%b %d %I:%M %p"))            # Nov 10 02:30 PM
print(dt.strftime("%j"))                        # 314
# (names such as Tuesday depend on the locale; the default is English)

# ---------- 5. Parsing with strptime and fromisoformat ----------
print(datetime.strptime("2026-11-10 14:30", "%Y-%m-%d %H:%M"))  # 2026-11-10 14:30:00
print(repr(datetime.strptime("10/11/26", "%d/%m/%y")))          # datetime.datetime(2026, 11, 10, 0, 0)
print(datetime.fromisoformat("2026-11-10T14:30:15") == dt)      # True
try:
    datetime.strptime("2026-13-01", "%Y-%m-%d")                 # there is no month 13
except ValueError:
    print("ValueError")                                         # ValueError

# ---------- 6. The calendar module ----------
print(calendar.isleap(2024), calendar.isleap(2026))             # True False
print(calendar.monthrange(2026, 2))             # (6, 28)  Feb 1 2026 is a Sunday (6); 28 days
print(calendar.weekday(2026, 11, 10))           # 1
print(calendar.month_name[11], calendar.day_name[1])            # November Tuesday

# ---------- 7. Time zones ----------
# A NAIVE datetime has no time zone. An AWARE datetime knows its offset from UTC.
ist = timezone(timedelta(hours=5, minutes=30))
aware = datetime(2026, 11, 10, 14, 30, tzinfo=ist)
print(aware)                                    # 2026-11-10 14:30:00+05:30
print(aware.astimezone(timezone.utc))           # 2026-11-10 09:00:00+00:00
print(aware.utcoffset())                        # 5:30:00

try:
    aware < dt                                  # aware and naive cannot be compared
except TypeError:
    print("TypeError")                          # TypeError

print(datetime(1970, 1, 1, tzinfo=timezone.utc).timestamp())    # 0.0
print(datetime.fromtimestamp(86400, tz=timezone.utc))           # 1970-01-02 00:00:00+00:00
print(datetime.now(timezone.utc).tzinfo)        # UTC
# Named zones ("Asia/Kolkata", "Europe/London") with daylight saving use zoneinfo:
#     from zoneinfo import ZoneInfo ; datetime(..., tzinfo=ZoneInfo("Asia/Kolkata"))
# (on Windows, run  pip install tzdata  first)

# RULES FOR REAL PROGRAMS
#  - Store and exchange time in UTC (or as an epoch number), convert to local time only to DISPLAY it.
#  - Use ISO 8601 text ("2026-11-10T14:30:15+00:00") when you save or send a time.
#  - Use time.perf_counter() or time.monotonic() to measure durations and timeouts.
#  - On a microcontroller the same ideas apply: an RTC counts seconds, a timer tick counts
#    milliseconds, and a uint32 millisecond counter wraps after 49.7 days.