import csv
import json
import os
import shutil
from array import array
from collections import Counter


def write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


write("story.txt", "the cat sat\nthe dog ran\n\nthe end\n")
text = read("story.txt")
lines = text.splitlines()

# 1. Count lines, non-empty lines, words and characters
print(len(lines), len([l for l in lines if l]), len(text.split()), len(text))    # 4 3 8 33

# 2. The most frequent words
print(Counter(text.split()).most_common(2))     # [('the', 3), ('cat', 1)]

# 3. The longest line, and the last two lines
print(max(lines, key=len))                      # the cat sat
print(lines[-2:])                               # ['', 'the end']

# 4. Reverse the order of the lines into a new file
with open("rev.txt", "w", encoding="utf-8") as out:
    out.writelines(line + "\n" for line in reversed(lines))
print(repr(read("rev.txt")))                    # 'the end\n\nthe dog ran\nthe cat sat\n'

# 5. Copy a binary file in chunks
with open("src.bin", "wb") as f:
    f.write(b"0123456789" * 3)
with open("src.bin", "rb") as src, open("dst.bin", "wb") as dst:
    while chunk := src.read(8):
        dst.write(chunk)
print(os.path.getsize("src.bin"), os.path.getsize("dst.bin"))   # 30 30
print(read.__name__, open("src.bin", "rb").read() == open("dst.bin", "rb").read())   # read True

# 6. Read a KEY=VALUE config file (skip comments and blank lines)
write("app.cfg", "# settings\nbaud=9600\n\nparity = N\n# end\n")
cfg = {}
for line in read("app.cfg").splitlines():
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    key, _, value = line.partition("=")
    cfg[key.strip()] = value.strip()
print(cfg)                                      # {'baud': '9600', 'parity': 'N'}

# 7. Save and load settings as JSON, with defaults
defaults = {"theme": "dark", "size": 12}
with open("settings.json", "w", encoding="utf-8") as f:
    json.dump({"size": 14}, f)
with open("settings.json", encoding="utf-8") as f:
    loaded = json.load(f)
print({**defaults, **loaded})                   # {'theme': 'dark', 'size': 14}

# 8. CSV: write and read with the csv module
with open("scores.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows([["name", "score"], ["Ann", 90], ["Bob", 85]])
with open("scores.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
print(rows)                 # [{'name': 'Ann', 'score': '90'}, {'name': 'Bob', 'score': '85'}]
print(sum(int(r["score"]) for r in rows) / len(rows))           # 87.5

# 9. Append to a log, then count the errors
with open("app.log", "a", encoding="utf-8") as f:
    for msg in ["INFO start", "ERROR disk", "INFO done", "ERROR net"]:
        f.write(msg + "\n")
with open("app.log", encoding="utf-8") as f:
    print(sum(1 for line in f if line.startswith("ERROR")))     # 2

# 10. Binary records: save 16-bit samples with array and read them back
samples = array("H", [100, 200, 65535])
with open("samples.bin", "wb") as f:
    samples.tofile(f)
print(os.path.getsize("samples.bin"))           # 6
back = array("H")
with open("samples.bin", "rb") as f:
    back.fromfile(f, 3)
print(back == samples)                          # True

# 11. A safe write: write to a temporary file, then replace the real one
def safe_write(path, content):
    tmp = path + ".tmp"
    write(tmp, content)
    os.replace(tmp, path)       # the file is never left half-written

safe_write("settings.txt", "v1")
safe_write("settings.txt", "v2")
print(read("settings.txt"), os.path.exists("settings.txt.tmp"))     # v2 False

# 12. Search for text in every file of a folder
os.makedirs("docs", exist_ok=True)
write("docs/a.txt", "hello world")
write("docs/b.txt", "goodbye")
write("docs/c.txt", "hello again")
print([n for n in sorted(os.listdir("docs")) if "hello" in read(os.path.join("docs", n))])
# ['a.txt', 'c.txt']

# 13. A read that never crashes
def read_or_default(path, default=""):
    try:
        return read(path)
    except FileNotFoundError:
        return default

print(repr(read_or_default("nope.txt", "none")))                # 'none'

# Cleanup
for name in ["story.txt", "rev.txt", "src.bin", "dst.bin", "app.cfg", "settings.json",
             "scores.csv", "app.log", "samples.bin", "settings.txt"]:
    os.remove(name)
shutil.rmtree("docs")
