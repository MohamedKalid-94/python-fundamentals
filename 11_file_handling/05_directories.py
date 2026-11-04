import glob
import os
import shutil
import tempfile
from pathlib import Path

shutil.rmtree("demo_dir", ignore_errors=True)       # start clean

# 1. Create
os.mkdir("demo_dir")
print(os.path.isdir("demo_dir"))                    # True

try:
    os.mkdir("demo_dir")
except FileExistsError:
    print("already exists")                         # already exists

os.makedirs("demo_dir/sub/deeper", exist_ok=True)   # creates every missing level
print(os.path.isdir("demo_dir/sub/deeper"))         # True

for name in ["a.txt", "b.txt", "c.py"]:
    with open(os.path.join("demo_dir", name), "w", encoding="utf-8") as f:
        f.write(name)
with open(os.path.join("demo_dir", "sub", "d.txt"), "w", encoding="utf-8") as f:
    f.write("d")

# 2. List (the order is NOT guaranteed, so sort it)
print(sorted(os.listdir("demo_dir")))               # ['a.txt', 'b.txt', 'c.py', 'sub']

with os.scandir("demo_dir") as entries:
    print(sorted((e.name, e.is_dir()) for e in entries))
# [('a.txt', False), ('b.txt', False), ('c.py', False), ('sub', True)]

# 3. Patterns with glob
print([os.path.basename(p) for p in sorted(glob.glob("demo_dir/*.txt"))])
# ['a.txt', 'b.txt']
print([os.path.basename(p) for p in sorted(glob.glob("demo_dir/**/*.txt", recursive=True))])
# ['a.txt', 'b.txt', 'd.txt']

# 4. Walk the whole tree
for folder, subdirs, files in os.walk("demo_dir"):
    subdirs.sort()
    rel = os.path.relpath(folder, "demo_dir").replace(os.sep, "/")
    print(rel, sorted(subdirs), sorted(files))
# . ['sub'] ['a.txt', 'b.txt', 'c.py']
# sub ['deeper'] ['d.txt']
# sub/deeper [] []

total = sum(len(files) for _, _, files in os.walk("demo_dir"))
print(total)                                        # 4

# 5. pathlib
p = Path("demo_dir")
print(sorted(x.name for x in p.iterdir()))          # ['a.txt', 'b.txt', 'c.py', 'sub']
print(sorted(x.name for x in p.glob("*.txt")))      # ['a.txt', 'b.txt']
print(sorted(x.relative_to(p).as_posix() for x in p.rglob("*.txt")))
# ['a.txt', 'b.txt', 'sub/d.txt']

# 6. Change the current directory
old = os.getcwd()
os.chdir("demo_dir")
print(os.path.basename(os.getcwd()))                # demo_dir
os.chdir(old)

# 7. Copy a whole tree
shutil.copytree("demo_dir", "demo_copy")
print(sorted(os.listdir("demo_copy")))              # ['a.txt', 'b.txt', 'c.py', 'sub']

# 8. Remove
try:
    os.rmdir("demo_dir/sub")                        # rmdir only removes EMPTY directories
except OSError:
    print("OSError")                                # OSError

os.rmdir("demo_dir/sub/deeper")
print(os.path.exists("demo_dir/sub/deeper"))        # False

shutil.rmtree("demo_dir")                           # removes a directory and EVERYTHING in it
shutil.rmtree("demo_copy")
print(os.path.exists("demo_dir"), os.path.exists("demo_copy"))  # False False

# 9. A temporary directory that cleans itself up
with tempfile.TemporaryDirectory() as tmp:
    print(os.path.isdir(tmp))                       # True
print(os.path.isdir(tmp))                           # False

# WARNING: shutil.rmtree() cannot be undone. Print the path before you delete it.