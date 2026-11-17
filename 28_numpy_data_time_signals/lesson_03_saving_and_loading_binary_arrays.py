import tempfile
from pathlib import Path

import numpy as np

# SAVING AND LOADING ARRAYS IN BINARY FORM
#   np.save(file, a) / np.load(file)          one array in a .npy file: dtype, shape and byte order are stored
#   np.savez(file, x=a, y=b)                  several arrays in one .npz archive (np.savez_compressed: smaller)
#   a.tofile(file) / np.fromfile(file, dtype) RAW bytes: no header, so YOU must remember dtype and shape
#   np.load(file, mmap_mode="r")              memory-mapped: use a file bigger than your RAM
#   np.lib.format.open_memmap / np.memmap     create or open a big array on disk
# .npy and .npz are NumPy's own formats. For sharing with other tools see lesson 04 (text) and Module 30 (pandas).

with tempfile.TemporaryDirectory() as folder:            # a temporary folder: everything is deleted at the end
    folder = Path(folder)

    a = np.arange(6, dtype=np.int16).reshape(2, 3)
    np.save(folder / "a.npy", a)
    b = np.load(folder / "a.npy")
    print(np.array_equal(a, b), b.dtype, b.shape, (folder / "a.npy").stat().st_size)    # 128 bytes header + 12 bytes data
    print((folder / "a.npy").read_bytes()[:6])                                          # the magic string

    # Several arrays in one archive
    np.savez(folder / "pack.npz", x=a, y=np.linspace(0, 1, 3))
    with np.load(folder / "pack.npz") as archive:
        print(archive.files, archive["x"].tolist(), archive["y"])
    np.savez(folder / "plain.npz", np.zeros(10_000))
    np.savez_compressed(folder / "small.npz", np.zeros(10_000))
    print((folder / "small.npz").stat().st_size < (folder / "plain.npz").stat().st_size)

    # Raw bytes: no dtype or shape is saved
    a.tofile(folder / "raw.bin")
    print((folder / "raw.bin").stat().st_size, np.fromfile(folder / "raw.bin", dtype=np.int16))
    print(np.fromfile(folder / "raw.bin", dtype=np.int16).reshape(2, 3).tolist() == a.tolist())
    print(np.fromfile(folder / "raw.bin", dtype=np.uint8)[:4])                          # the wrong dtype gives other numbers
    a.astype(">i2").tofile(folder / "big.bin")                                           # a big-endian file from a device
    print(np.fromfile(folder / "big.bin", dtype=">i2").tolist(), np.fromfile(folder / "big.bin", dtype="<i2").tolist())

    # Memory mapping: only the parts you touch are read
    big = np.lib.format.open_memmap(folder / "big.npy", mode="w+", dtype=np.float64, shape=(1_000,))
    big[:] = np.arange(1_000)
    big.flush()
    del big
    mapped = np.load(folder / "big.npy", mmap_mode="r")
    print(type(mapped).__name__, mapped.shape, mapped[999], mapped[10:13].tolist())
    raw_map = np.memmap(folder / "raw.bin", dtype=np.int16, mode="r", shape=(2, 3))
    print(raw_map[1, 2], raw_map.flags["WRITEABLE"])
    del mapped, raw_map

    # Object arrays need pickle, which can run code when loading: refuse it for files you do not trust
    np.save(folder / "obj.npy", np.array([{"a": 1}, None], dtype=object), allow_pickle=True)
    try:
        np.load(folder / "obj.npy", allow_pickle=False)
    except ValueError as error:
        print("ValueError:", str(error)[:46])

    # Structured arrays are saved with their dtype
    log = np.array([(1, 2.5), (2, 3.5)], dtype=[("id", "<u2"), ("value", "<f4")])
    np.save(folder / "log.npy", log)
    print(np.load(folder / "log.npy").dtype.names)

# EXPECTED OUTPUT
# True int16 (2, 3) 140
# b'\x93NUMPY'
# ['x', 'y'] [[0, 1, 2], [3, 4, 5]] [0.  0.5 1. ]
# True
# 12 [0 1 2 3 4 5]
# True
# [0 0 1 0]
# [0, 1, 2, 3, 4, 5] [0, 256, 512, 768, 1024, 1280]
# memmap (1000,) 999.0 [10.0, 11.0, 12.0]
# 5 False
# ValueError: Object arrays cannot be loaded when allow_pick
# ('id', 'value')