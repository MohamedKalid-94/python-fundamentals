import os
import shutil
import time

# 1. System information
print(os.name in ("posix", "nt"))               # True     "nt" is Windows, "posix" is Linux/macOS
print(os.sep in ("/", "\\"))                    # True     path separator
print(os.linesep in ("\n", "\r\n"))             # True     line ending of this system
print(os.cpu_count() >= 1)                      # True
print(isinstance(os.getpid(), int))             # True     process id
print(len(os.urandom(4)))                       # 4        random bytes from the system

# 2. Environment variables
print(os.getenv("NOT_SET_XYZ", "default"))      # default
os.environ["MY_VAR"] = "42"                     # only for this process and its children
print(os.getenv("MY_VAR"))                      # 42
print("PATH" in os.environ)                     # True

# 3. File information
with open("s.bin", "wb") as f:
    f.write(b"hello")

st = os.stat("s.bin")
print(st.st_size)                               # 5        size in bytes
print(abs(time.time() - st.st_mtime) < 60)      # True     modified a moment ago

os.utime("s.bin", (0, 0))                       # set access and modification times
print(os.stat("s.bin").st_mtime)                # 0.0

print(os.access("s.bin", os.R_OK), os.access("s.bin", os.W_OK))      # True True
print(os.access("ghost.bin", os.F_OK))          # False

# 4. Directory entries with details
os.makedirs("tree/sub", exist_ok=True)
for path, data in [("tree/a.bin", b"123"), ("tree/b.bin", b"1234"), ("tree/sub/c.bin", b"12345")]:
    with open(path, "wb") as f:
        f.write(data)

with os.scandir("tree") as entries:
    for e in sorted(entries, key=lambda e: e.name):
        print(e.name, e.is_file(), e.is_dir(), e.stat().st_size if e.is_file() else "-")
# a.bin True False 3
# b.bin True False 4
# sub False True -

# 5. Total size of a tree
total = 0
for folder, _, files in os.walk("tree"):
    for name in files:
        total += os.path.getsize(os.path.join(folder, name))
print(total)                                    # 12

# 6. Remove nested empty directories in one call
os.makedirs("x/y/z")
os.removedirs("x/y/z")                          # removes z, then y, then x (each if empty)
print(os.path.exists("x"))                      # False

# 7. unlink() is the same as remove()
os.unlink("s.bin")
print(os.path.exists("s.bin"))                  # False

shutil.rmtree("tree")