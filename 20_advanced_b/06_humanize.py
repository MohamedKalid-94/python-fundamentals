from datetime import datetime

# HUMANIZE: turn machine values (bytes, seconds, big numbers) into text people read easily.
# The third-party package "humanize" (pip install humanize) does this. To see HOW it works,
# this file writes the main functions itself, using only the standard library.

# 1. File sizes
def naturalsize(num_bytes, binary=False):
    base = 1024 if binary else 1000
    units = ["B", "KiB", "MiB", "GiB", "TiB"] if binary else ["B", "kB", "MB", "GB", "TB"]
    size = float(num_bytes)
    for unit in units:
        if abs(size) < base or unit == units[-1]:
            return f"{size:.0f} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= base

print(naturalsize(300), naturalsize(1500), naturalsize(1_500_000),
      naturalsize(1536, binary=True), naturalsize(5 * 1024 ** 3, binary=True))
# 300 B 1.5 kB 1.5 MB 1.5 KiB 5.0 GiB

# 2. Numbers with separators, ordinals, plurals, number words
def intcomma(n):
    return f"{n:,}"

def ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"

def plural(n, singular, plural_form=None):
    return f"{n} {singular if n == 1 else (plural_form or singular + 's')}"

WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

def apnumber(n):                                # the newspaper rule: spell out 0 to 9
    return WORDS[n] if 0 <= n <= 9 else str(n)

def intword(n):
    for limit, name in ((10 ** 9, "billion"), (10 ** 6, "million"), (10 ** 3, "thousand")):
        if n >= limit:
            return f"{n / limit:.1f} {name}"
    return str(n)

print(intcomma(1234567), intcomma(1234.5))      # 1,234,567 1,234.5
print([ordinal(n) for n in (1, 2, 3, 4, 11, 12, 13, 21, 22, 101, 111)])
# ['1st', '2nd', '3rd', '4th', '11th', '12th', '13th', '21st', '22nd', '101st', '111th']
print(plural(1, "file"), plural(2, "file"), plural(0, "file"), plural(3, "goose", "geese"))
# 1 file 2 files 0 files 3 geese
print([apnumber(n) for n in (0, 1, 9, 10)])     # ['zero', 'one', 'nine', '10']
print(intword(1_200_000), intword(3_000_000_000), intword(15_000), intword(999))
# 1.2 million 3.0 billion 15.0 thousand 999

# 3. Durations and "time ago"
UNITS = [("year", 365 * 86400), ("month", 30 * 86400), ("day", 86400),
         ("hour", 3600), ("minute", 60), ("second", 1)]

def naturaldelta(seconds):                      # the largest unit only
    seconds = abs(int(seconds))
    for name, size in UNITS:
        if seconds >= size:
            return plural(seconds // size, name)
    return plural(0, "second")

def naturaltime(seconds_from_now):
    if seconds_from_now == 0:
        return "now"
    text = naturaldelta(seconds_from_now)
    return f"{text} ago" if seconds_from_now < 0 else f"in {text}"

print([naturaldelta(s) for s in (0, 45, 90, 3700, 200_000, 40 * 86400)])
# ['0 seconds', '45 seconds', '1 minute', '1 hour', '2 days', '1 month']
print(naturaltime(-300), naturaltime(7200), naturaltime(0))     # 5 minutes ago in 2 hours now

then, now = datetime(2026, 11, 10, 12, 0), datetime(2026, 11, 10, 14, 30)
print(naturaltime((then - now).total_seconds()))                # 2 hours ago

# 4. A precise duration, and lists written the way people say them
def human_list(items):
    items = list(items)
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + " and " + items[-1]

def precisedelta(seconds):
    seconds = abs(int(seconds))
    parts = []
    for name, size in UNITS:
        count, seconds = divmod(seconds, size)
        if count:
            parts.append(plural(count, name))
    return human_list(parts) or plural(0, "second")

print(precisedelta(3725), "|", precisedelta(90061), "|", precisedelta(0))
# 1 hour, 2 minutes and 5 seconds | 1 day, 1 hour, 1 minute and 1 second | 0 seconds
print(human_list(["a", "b", "c"]), "|", human_list(["a", "b"]), "|", human_list(["a"]))
# a, b and c | a and b | a

# 5. Percentages and shortened text
def truncate(text, width):
    return text if len(text) <= width else text[:width - 1] + "…"

print(f"{0.256:.0%}", truncate("The quick brown fox", 10))    # 26% The quick…
print(str(__import__("datetime").timedelta(seconds=3725)))      # 1:02:05

# THE REAL PACKAGE (pip install humanize) offers the same ideas and many more:
#   import humanize
#   humanize.naturalsize(1_000_000)             '1.0 MB'        (binary=True gives KiB, MiB ...)
#   humanize.intcomma(12345)                    '12,345'
#   humanize.ordinal(1)                         '1st'
#   humanize.naturaldelta(timedelta(hours=1))   'an hour'
#   humanize.naturaltime(timedelta(minutes=1))  'a minute ago'
#   humanize.intword(1_000_000)                 '1.0 million'
#   humanize.apnumber(4)                        'four'
#   humanize.i18n.activate("fr_FR")             texts in other languages
# Also: rich.filesize (sizes), babel (numbers, dates and currencies for each country's locale).
#
# RULE: store and exchange raw values (bytes, seconds, UTC ISO times); humanize ONLY when you display
# them to a person. Never parse humanized text back into data.