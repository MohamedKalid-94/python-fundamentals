import csv
import hashlib
import io
import os
import re
import sched
import shutil
import subprocess
import sys
import tempfile
import zipfile
from datetime import datetime, timedelta
from pathlib import Path

# AUTOMATION: let Python do the boring, repeated work. Every example works inside a temporary folder.

def rel(root, paths):
    return sorted(str(p.relative_to(root)).replace(os.sep, "/") for p in paths)

# 1. Sort files into folders by extension. A DRY RUN shows what WOULD happen.
def organize(folder, dry_run=False):
    moved = []
    for item in sorted(folder.iterdir()):
        if item.is_file():
            target = folder / (item.suffix.lstrip(".").lower() or "no_extension")
            moved.append((item.name, target.name))
            if not dry_run:
                target.mkdir(exist_ok=True)
                shutil.move(str(item), str(target / item.name))
    return moved

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    for name in ("a.txt", "b.TXT", "c.jpg", "README"):
        (root / name).write_text(name, encoding="utf-8")
    print(organize(root, dry_run=True))
    # [('README', 'no_extension'), ('a.txt', 'txt'), ('b.TXT', 'txt'), ('c.jpg', 'jpg')]
    print(organize(root))                       # the same list, and now the files are moved
    print(rel(root, (p for p in root.rglob("*") if p.is_file())))
    # ['jpg/c.jpg', 'no_extension/README', 'txt/a.txt', 'txt/b.TXT']
    print(organize(root))                       # []      run it again: nothing left to do (IDEMPOTENT)

# 2. Batch rename with a regular expression
def batch_rename(folder, pattern, replacement):
    renamed = []
    for item in sorted(folder.iterdir()):
        new_name = re.sub(pattern, replacement, item.name)
        if new_name != item.name:
            item.rename(folder / new_name)
            renamed.append((item.name, new_name))
    return renamed

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    for name in ("IMG_001.JPG", "IMG_002.JPG", "notes.txt"):
        (root / name).write_text("x", encoding="utf-8")
    print(batch_rename(root, r"^IMG_(\d+)\.JPG$", r"photo_\1.jpg"))
    # [('IMG_001.JPG', 'photo_001.jpg'), ('IMG_002.JPG', 'photo_002.jpg')]
    print(sorted(p.name for p in root.iterdir()))       # ['notes.txt', 'photo_001.jpg', 'photo_002.jpg']

# 3. Find duplicate files by their content hash
def find_duplicates(folder):
    groups = {}
    for path in sorted(folder.rglob("*")):
        if path.is_file():
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            groups.setdefault(digest, []).append(path.name)
    return sorted(names for names in groups.values() if len(names) > 1)

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    for name, text in (("a.txt", "same"), ("b.txt", "same"), ("c.txt", "different")):
        (root / name).write_text(text, encoding="utf-8")
    print(find_duplicates(root))                # [['a.txt', 'b.txt']]

# 4. Delete files older than N days (the clock is a parameter, so the code is easy to test)
def delete_older_than(folder, days, now):
    removed = []
    for path in sorted(folder.iterdir()):
        age = now - datetime.fromtimestamp(path.stat().st_mtime)
        if age > timedelta(days=days):
            path.unlink()
            removed.append(path.name)
    return removed

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    now = datetime(2026, 11, 10, 12, 0)
    for name, days_old in (("old.log", 40), ("new.log", 1)):
        path = root / name
        path.write_text("x", encoding="utf-8")
        stamp = (now - timedelta(days=days_old)).timestamp()
        os.utime(path, (stamp, stamp))
    print(delete_older_than(root, 30, now), sorted(p.name for p in root.iterdir()))
    # ['old.log'] ['new.log']

# 5. A dated backup in a ZIP file
def backup(folder, target_dir, when):
    name = f"backup_{when:%Y%m%d_%H%M}.zip"
    with zipfile.ZipFile(target_dir / name, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(folder.rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(folder).as_posix())
    return name

with tempfile.TemporaryDirectory() as src_tmp, tempfile.TemporaryDirectory() as dst_tmp:
    src, dst = Path(src_tmp), Path(dst_tmp)
    (src / "a.txt").write_text("a", encoding="utf-8")
    (src / "sub").mkdir()
    (src / "sub" / "b.txt").write_text("b", encoding="utf-8")
    name = backup(src, dst, datetime(2026, 11, 10, 14, 30))
    with zipfile.ZipFile(dst / name) as zf:
        print(name, zf.namelist())              # backup_20261110_1430.zip ['a.txt', 'sub/b.txt']

# 6. Scheduling with the standard library. A FAKE clock makes the example instant and repeatable.
class FakeClock:
    def __init__(self):
        self.now = 0.0

    def time(self):
        return self.now

    def sleep(self, seconds):
        self.now += seconds

clock = FakeClock()
scheduler = sched.scheduler(clock.time, clock.sleep)
events = []

def action(name):
    events.append((name, clock.now))

scheduler.enter(5, 1, action, ("b",))           # in 5 seconds
scheduler.enter(1, 1, action, ("a",))           # in 1 second
scheduler.run()
print(events)                                   # [('a', 1.0), ('b', 5.0)]

clock2 = FakeClock()
periodic = sched.scheduler(clock2.time, clock2.sleep)
ticks = []

def tick(n):
    ticks.append((n, clock2.now))
    if n < 3:
        periodic.enter(2, 1, tick, (n + 1,))    # schedule the next run: every 2 seconds

periodic.enter(0, 1, tick, (1,))
periodic.run()
print(ticks)                                    # [(1, 0.0), (2, 2.0), (3, 4.0)]
# For real use:  sched with time.monotonic/time.sleep, the "schedule" package, APScheduler,
# cron (Linux/macOS), Windows Task Scheduler (schtasks), systemd timers.

# 7. Run other programs, and handle their failures
ok = subprocess.run([sys.executable, "-c", "print('done')"], capture_output=True, text=True, check=True)
print(ok.stdout.strip(), ok.returncode)         # done 0

try:
    subprocess.run([sys.executable, "-c", "raise SystemExit(3)"], check=True)
except subprocess.CalledProcessError as e:
    print(e.returncode)                         # 3

try:
    subprocess.run([sys.executable, "-c", "import time; time.sleep(5)"], timeout=0.2)
except subprocess.TimeoutExpired:
    print("TimeoutExpired")                     # TimeoutExpired

# 8. Notice changes in a folder: compare two snapshots (the idea behind "watch" tools)
def snapshot(folder):
    return {p.name: p.stat().st_mtime_ns for p in folder.iterdir()}

def changes(before, after):
    return {
        "created": sorted(set(after) - set(before)),
        "deleted": sorted(set(before) - set(after)),
        "modified": sorted(n for n in before.keys() & after.keys() if before[n] != after[n]),
    }

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    (root / "a.txt").write_text("1", encoding="utf-8")
    (root / "b.txt").write_text("2", encoding="utf-8")
    first = snapshot(root)
    later = (root / "a.txt").stat().st_mtime_ns + 10 ** 9
    os.utime(root / "a.txt", ns=(later, later))
    (root / "b.txt").unlink()
    (root / "c.txt").write_text("3", encoding="utf-8")
    print(changes(first, snapshot(root)))
    # {'created': ['c.txt'], 'deleted': ['b.txt'], 'modified': ['a.txt']}
# Real projects use the "watchdog" package, which asks the operating system for change events.

# 9. A report as CSV
rows = [{"ext": "txt", "count": 2, "bytes": 10}, {"ext": "jpg", "count": 1, "bytes": 3}]
buffer = io.StringIO()
writer = csv.DictWriter(buffer, fieldnames=["ext", "count", "bytes"], lineterminator="\n")
writer.writeheader()
writer.writerows(rows)
print(buffer.getvalue().splitlines())           # ['ext,count,bytes', 'txt,2,10', 'jpg,1,3']

# HABITS OF GOOD AUTOMATION SCRIPTS
#  - A --dry-run option, and logging of what was done.      - Idempotent: running twice is safe.
#  - Take the paths, dates and clocks as PARAMETERS (testable); test with temporary folders.
#  - Write files atomically (temp file, then os.replace); never delete without a safeguard.
#  - Return an exit code; read secrets from environment variables; run inside a virtual environment.
#  - Handle failure: timeouts, retries with backoff, clear error messages.
#
# TOOLS YOU WILL MEET
#   requests / httpx          web APIs                     BeautifulSoup, Scrapy   reading web pages
#   openpyxl, pandas          Excel and tables             pypdf                   PDF files
#   Pillow                    images                       Selenium, Playwright    controlling a browser
#   paramiko, fabric          SSH and remote servers       pyserial, esptool       serial ports and firmware flashing
#   typer / click, rich       command-line tools           APScheduler, Celery     jobs and queues
#   Respect a website's terms of use and robots.txt before you scrape it.