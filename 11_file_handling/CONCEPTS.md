# Module 11: File Handling, Concepts Summary

| # | Topic | Concept | Remember |
|---|---|---|---|
| 01 | File Handling | `open()` | `open(path, mode, encoding=...)` returns a file object |
| 01 | File Handling | Modes | `r` read, `w` write (EMPTIES the file), `a` append, `x` create only, `+` read and write, `b` binary, `t` text |
| 01 | File Handling | `with` | `with open(...) as f:` always closes the file, even on errors |
| 01 | File Handling | Encoding | Always pass `encoding="utf-8"` for text files |
| 01 | File Handling | Errors | `FileNotFoundError` for `r` on a missing file; `FileExistsError` for `x` |
| 01 | File Handling | Closed file | Using it raises `ValueError: I/O operation on closed file` |
| 01 | File Handling | Text vs binary | Text mode gives `str`; binary mode (`rb`, `wb`) gives `bytes` |
| 02 | Write | `write(s)` | Returns the number of characters; adds NO newline |
| 02 | Write | `writelines(list)` | Adds no newlines either |
| 02 | Write | `print(..., file=f)` | Adds spaces and the newline |
| 02 | Write | `"a"` | Adds to the end; `"w"` replaces everything |
| 02 | Write | `"r+"` | Reads and writes from position 0 and overwrites what is there |
| 02 | Write | Type | Text mode needs `str`, binary mode needs `bytes` (else `TypeError`) |
| 02 | Write | UTF-8 | One character can be several bytes: `len("café")` is 4 but its bytes are 5 |
| 02 | Write | JSON | `json.dump(data, f, indent=2)` and `json.load(f)` |
| 03 | Read | `read()` | The whole file as one string |
| 03 | Read | `read(n)` | The next `n` characters or bytes; `''` or `b''` at the end |
| 03 | Read | `readline()` | One line (with its `\n`) |
| 03 | Read | `readlines()` | A list of lines |
| 03 | Read | `for line in f` | Best for large files: one line at a time |
| 03 | Read | Clean lines | `line.rstrip("\n")`, `.strip()`, or `read().splitlines()` |
| 03 | Read | Chunks | `while chunk := f.read(4096):` for binary files |
| 03 | Read | First lines | `islice(f, n)` |
| 03 | Read | `pathlib` | `Path(p).read_text(encoding="utf-8")` |
| 04 | Rename/Delete | Rename | `os.rename(old, new)`; on Windows it fails if `new` exists |
| 04 | Rename/Delete | Replace | `os.replace(old, new)` overwrites on every system |
| 04 | Rename/Delete | Copy and move | `shutil.copy`, `shutil.copy2`, `shutil.move` |
| 04 | Rename/Delete | Delete | `os.remove(p)` or `os.unlink(p)`; `FileNotFoundError` if missing |
| 04 | Rename/Delete | Safe delete | `Path(p).unlink(missing_ok=True)` |
| 04 | Rename/Delete | Extension | `root, ext = os.path.splitext(name)` |
| 05 | Directories | Create | `os.mkdir` (one level), `os.makedirs(path, exist_ok=True)` (all levels) |
| 05 | Directories | List | `os.listdir` (order not guaranteed), `os.scandir` (with details), `glob.glob` (patterns) |
| 05 | Directories | Walk | `os.walk(top)` gives `(folder, subdirs, files)` for every level |
| 05 | Directories | `pathlib` | `Path.iterdir()`, `.glob("*.txt")`, `.rglob("*.txt")`, `.mkdir(parents=True)` |
| 05 | Directories | Remove | `os.rmdir` only removes EMPTY folders; `shutil.rmtree` removes everything (no undo) |
| 05 | Directories | Copy | `shutil.copytree(src, dst)` |
| 05 | Directories | Current folder | `os.getcwd()`, `os.chdir(path)` |
| 05 | Directories | Temporary | `tempfile.TemporaryDirectory()` cleans itself up |
| 06 | File Methods | `seek(offset, whence)` | 0 from the start, 1 from the current position, 2 from the end |
| 06 | File Methods | `tell()` | The current position |
| 06 | File Methods | Text mode | Only simple seeks work; use binary mode for byte positions |
| 06 | File Methods | `flush()` | Pushes the buffer out now; `close()` flushes too |
| 06 | File Methods | `truncate(size)` | Cuts the file to a size |
| 06 | File Methods | State | `readable()`, `writable()`, `seekable()`, `fileno()`, `closed` |
| 06 | File Methods | In memory | `StringIO` and `BytesIO` behave like files without touching the disk |
| 07 | OS Methods | System | `os.name` (`posix` / `nt`), `os.sep`, `os.linesep`, `os.cpu_count()`, `os.getpid()` |
| 07 | OS Methods | Environment | `os.getenv(name, default)`, `os.environ[name] = value` |
| 07 | OS Methods | Information | `os.stat(p)` gives `st_size`, `st_mtime`; `os.access(p, os.R_OK)` |
| 07 | OS Methods | Times | `os.utime(p, (atime, mtime))` |
| 07 | OS Methods | Cleanup | `os.removedirs` removes nested empty folders |
| 07 | OS Methods | Commands | Prefer `subprocess` over `os.system` |
| 08 | OS Path | Build | `os.path.join(a, b)`; an absolute part restarts the path |
| 08 | OS Path | Split | `dirname`, `basename`, `split`, `splitext` |
| 08 | OS Path | Clean | `normpath`, `abspath`, `relpath`, `commonpath`, `expanduser` |
| 08 | OS Path | Test | `exists`, `isfile`, `isdir`, `islink`, `samefile` |
| 08 | OS Path | Size and time | `getsize`, `getmtime` |
| 08 | OS Path | `pathlib` | `Path("a") / "b"`, `.name`, `.stem`, `.suffix`, `.parent`, `.with_suffix()` |
| 08 | OS Path | Portable | Never glue paths with `+ "/" +`; use `join` or `/` |
| 09 | Examples | CSV | `csv.writer(f)` and `csv.DictReader(f)`, files opened with `newline=""` |
| 09 | Examples | Safe write | Write to `file.tmp`, then `os.replace` to the real name |
| 09 | Examples | Binary records | `array.tofile(f)` and `array.fromfile(f, n)` |
| 09 | Examples | Config files | `partition("=")` after skipping comments and blank lines |
| 09 | Examples | Missing files | Catch `FileNotFoundError` instead of checking `exists` first |