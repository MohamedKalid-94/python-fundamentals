import bz2
import gzip
import lzma
import os
import shutil
import tarfile
import tempfile
import zipfile
import zlib
from pathlib import Path

data = b"sensor reading 25.3 C\n" * 200
print(len(data))                                # 4400

# 1. zlib: the engine behind gzip and zip
packed = zlib.compress(data)
print(len(packed) < 100, zlib.decompress(packed) == data)       # True True
print(len(zlib.compress(data, 9)) <= len(zlib.compress(data, 1)))   # True    level 1 fast ... 9 smallest

# Data that is already random cannot be compressed
print(len(zlib.compress(os.urandom(1000))) >= 1000)             # True

# 2. Checksums
print(zlib.crc32(b"hello"), hex(zlib.crc32(b"123456789")), zlib.adler32(b"hello"))
# 907060870 0xcbf43926 103547413
print(zlib.crc32(b"world", zlib.crc32(b"hello ")) == zlib.crc32(b"hello world"))   # True   chunk by chunk

# 3. gzip, bz2, lzma: the same idea, different speed and size
print([len(f(data)) < len(data) for f in (gzip.compress, bz2.compress, lzma.compress)])
# [True, True, True]
print(gzip.decompress(gzip.compress(data)) == data)             # True

# 4. Streaming: compress piece by piece (big files do not fit in memory)
compressor = zlib.compressobj()
out = compressor.compress(data[:2000]) + compressor.compress(data[2000:]) + compressor.flush()
print(zlib.decompress(out) == data)             # True

with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)

    # 5. A compressed text file
    gz = tmp / "log.txt.gz"
    with gzip.open(gz, "wt", encoding="utf-8") as f:
        f.write("line\n" * 100)
    with gzip.open(gz, "rt", encoding="utf-8") as f:
        print(f.read().count("\n"), gz.stat().st_size < 500)    # 100 True

    # 6. A zip archive
    zpath = tmp / "demo.zip"
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("a.txt", "hello " * 100)
        zf.writestr("b.txt", "world")
    print(zipfile.is_zipfile(zpath))            # True
    with zipfile.ZipFile(zpath) as zf:
        print(zf.namelist())                    # ['a.txt', 'b.txt']
        info = zf.getinfo("a.txt")
        print(info.file_size, info.compress_size < info.file_size)      # 600 True
        print(zf.read("b.txt"), zf.testzip())   # b'world' None       testzip() None means "no errors"
        zf.extractall(tmp / "unzipped")
    print(sorted(p.name for p in (tmp / "unzipped").iterdir()))         # ['a.txt', 'b.txt']

    # 7. A tar.gz archive (Linux style)
    src = tmp / "src"
    src.mkdir()
    (src / "a.txt").write_text("alpha", encoding="utf-8")
    (src / "b.txt").write_text("beta", encoding="utf-8")
    tpath = tmp / "demo.tar.gz"
    with tarfile.open(tpath, "w:gz") as tf:
        tf.add(src / "a.txt", arcname="a.txt")
        tf.add(src / "b.txt", arcname="b.txt")
    with tarfile.open(tpath, "r:gz") as tf:
        print(tf.getnames())                    # ['a.txt', 'b.txt']
        try:
            tf.extractall(tmp / "untarred", filter="data")      # the safe way (Python 3.12+)
        except TypeError:
            tf.extractall(tmp / "untarred")     # older Python without the filter argument
    print(sorted(p.name for p in (tmp / "untarred").iterdir()))         # ['a.txt', 'b.txt']

    # 8. One call for a whole folder
    archive = shutil.make_archive(str(tmp / "bundle"), "zip", root_dir=src)
    print(archive.endswith("bundle.zip"))       # True
    shutil.unpack_archive(archive, tmp / "bundle_out")
    print(sorted(p.name for p in (tmp / "bundle_out").iterdir()))       # ['a.txt', 'b.txt']

# CHOOSING
#   zlib / gzip   fast, good ratio, everywhere (HTTP, logs)         bz2   smaller, slower
#   lzma / xz     smallest, slowest                                  zip   many files + random access (Windows friendly)
#   tar.gz        many files in one stream (Linux, backups)
# SAFETY  an archive from outside can contain "../../x" paths or a "zip bomb" (tiny file, huge content):
#         use tarfile's filter="data", check sizes, never extract untrusted archives as administrator.
# EMBEDDED  CRC32 guards firmware images and files; compress logs before you upload them.