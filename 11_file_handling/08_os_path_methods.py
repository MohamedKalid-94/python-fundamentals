import os
import time
from pathlib import Path


def posix(path):
    """Show a path with / on every system, so the output below matches yours."""
    return path.replace(os.sep, "/")


# 1. Build and take apart paths (these only work on STRINGS: no file is needed)
p = os.path.join("data", "logs", "app.log")
print(posix(p))                                 # data/logs/app.log
print(posix(os.path.dirname(p)), os.path.basename(p))           # data/logs app.log
print([posix(x) for x in os.path.split(p)])     # ['data/logs', 'app.log']

# 2. Extensions
print(os.path.splitext("archive.tar.gz"))       # ('archive.tar', '.gz')
print(os.path.splitext("README"))               # ('README', '')
print(os.path.splitext(".bashrc"))              # ('.bashrc', '')
print(os.path.splitext(os.path.basename("/x/y/report.final.pdf"))[0])    # report.final

# 3. Clean up and compare
print(posix(os.path.normpath("a/./b/../c")))    # a/c
print(posix(os.path.join("a", "/b", "c")))      # /b/c       an absolute part RESTARTS the path
print(posix(os.path.relpath(os.path.join("a", "b", "c"), "a")))  # b/c
print(posix(os.path.commonpath(["a/b/c", "a/b/d"])))             # a/b

# 4. Absolute paths
print(os.path.isabs(os.path.abspath("x")))      # True
print(os.path.basename(os.path.abspath("f.txt")))                # f.txt
print(os.path.expanduser("~") != "~")           # True     the home directory

# 5. Questions about real files
with open("f.txt", "w", encoding="utf-8") as f:
    f.write("hello")                            # 5 bytes, no newline

print(os.path.exists("f.txt"), os.path.isfile("f.txt"), os.path.isdir("f.txt"))   # True True False
print(os.path.exists("ghost.txt"))              # False
print(os.path.getsize("f.txt"))                 # 5
print(time.time() - os.path.getmtime("f.txt") < 60)              # True
print(os.path.samefile("f.txt", "./f.txt"))     # True
print(os.path.isdir("."), os.path.islink("f.txt"))               # True False

# 6. pathlib: the modern, object-style alternative
q = Path("data") / "logs" / "app.log"
print(q.as_posix())                             # data/logs/app.log
print(q.name, q.stem, q.suffix)                 # app.log app .log
print(q.parent.as_posix(), q.parts)             # data/logs ('data', 'logs', 'app.log')
print(q.with_suffix(".txt").as_posix())         # data/logs/app.txt
print(q.with_name("x.log").as_posix())          # data/logs/x.log
print(Path("a.tar.gz").suffixes)                # ['.tar', '.gz']

f2 = Path("f.txt")
print(f2.exists(), f2.is_file(), f2.stat().st_size)              # True True 5
f2.write_text("hello world", encoding="utf-8")
print(f2.read_text(encoding="utf-8"))           # hello world

os.remove("f.txt")

# os.path  ->  pathlib
#   os.path.join(a, b)       Path(a) / b
#   os.path.basename(p)      Path(p).name
#   os.path.dirname(p)       Path(p).parent
#   os.path.splitext(p)      Path(p).stem and .suffix
#   os.path.exists(p)        Path(p).exists()
#   os.path.getsize(p)       Path(p).stat().st_size
#   os.path.abspath(p)       Path(p).resolve()