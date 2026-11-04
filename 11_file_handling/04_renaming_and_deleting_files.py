import os
import shutil
from pathlib import Path


def make(path, text="x"):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


# 1. Rename
make("old.txt", "data")
print(os.path.exists("old.txt"))                    # True
os.rename("old.txt", "new.txt")
print(os.path.exists("old.txt"), os.path.exists("new.txt"))     # False True

# 2. replace(): rename AND overwrite the target (the same on every system)
make("a.txt", "A")
make("b.txt", "B")
os.replace("a.txt", "b.txt")
print(os.path.exists("a.txt"), read("b.txt"))       # False A
# os.rename() onto an existing file raises FileExistsError on Windows

# 3. Copy (shutil)
shutil.copy("new.txt", "copy.txt")
print(read("copy.txt"), os.path.exists("new.txt"))  # data True

# 4. Move
shutil.move("copy.txt", "moved.txt")
print(os.path.exists("copy.txt"), read("moved.txt"))            # False data

# 5. Delete
os.remove("new.txt")
print(os.path.exists("new.txt"))                    # False

# 6. Errors
try:
    os.remove("new.txt")
except FileNotFoundError:
    print("FileNotFoundError")                      # FileNotFoundError

try:
    os.rename("ghost.txt", "x.txt")
except FileNotFoundError:
    print("FileNotFoundError")                      # FileNotFoundError

# 7. Safe delete with pathlib (no error if the file is already gone)
Path("moved.txt").unlink(missing_ok=True)
Path("moved.txt").unlink(missing_ok=True)
print(os.path.exists("moved.txt"))                  # False

# 8. Change an extension
root, ext = os.path.splitext("report.txt")
print(root + ".bak")                                # report.bak
make("report.txt", "r")
os.rename("report.txt", root + ".bak")
print(os.path.exists("report.bak"))                 # True

# 9. Rename many files
names = [f"img{i}.txt" for i in range(3)]
for n in names:
    make(n)
for n in names:
    os.rename(n, "photo_" + n)
print([os.path.exists("photo_" + n) for n in names])            # [True, True, True]

# 10. pathlib versions
Path("t.txt").write_text("t", encoding="utf-8")
Path("t.txt").rename("u.txt")
print(Path("u.txt").exists())                       # True
Path("u.txt").unlink()

# Cleanup
for n in ["b.txt", "report.bak"] + ["photo_" + n for n in names]:
    os.remove(n)

# Related: shutil.copy2() also copies the timestamps, shutil.copyfile() copies only the content.
# Directories are removed with os.rmdir() or shutil.rmtree() (next file).