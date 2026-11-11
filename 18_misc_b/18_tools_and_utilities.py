import ast
import base64
import binascii
import bisect
import dis
import hashlib
import heapq
import hmac
import io
import platform
import secrets
import string
import subprocess
import sys
import unittest
import uuid
from collections import ChainMap, Counter, OrderedDict, defaultdict, deque

# A tour of standard-library tools you will meet again and again.

# 1. hashlib: fingerprints of data
print(hashlib.sha256(b"hello").hexdigest())
# 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
print(hashlib.md5(b"hello").hexdigest())        # 5d41402abc4b2a76b9719d911017c592
print(hashlib.sha1(b"hello").hexdigest())       # aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d
# md5 and sha1 are fine to detect accidents, NOT for security. Use sha256 or better.
# Passwords need a slow hash: hashlib.scrypt / pbkdf2_hmac, or the packages argon2 and bcrypt.
print(len(hmac.new(b"key", b"msg", "sha256").hexdigest()), hmac.compare_digest("a", "a"))   # 64 True
#   hmac proves a message came from someone who knows the key; compare_digest avoids timing leaks

# 2. base64 and hex
print(base64.b64encode(b"hello"), base64.b64decode(b"aGVsbG8="), base64.b16encode(b"hello"))
# b'aGVsbG8=' b'hello' b'68656C6C6F'
print(binascii.hexlify(b"hi"), b"hi".hex(), bytes.fromhex("6869"))      # b'6869' 6869 b'hi'

# 3. uuid and secrets
print(uuid.uuid4().version, len(str(uuid.uuid4())))             # 4 36          random id
print(uuid.uuid5(uuid.NAMESPACE_DNS, "python.org"))             # 886313e1-3b8a-5372-9b90-0c9aee199e5d
print(len(secrets.token_hex(8)), len(secrets.token_urlsafe(16)) > 0)   # 16 True   secure random values

# 4. collections
print(Counter("banana").most_common(2))         # [('a', 3), ('n', 2)]
dd = defaultdict(list)
dd["x"].append(1)
print(dict(dd))                                 # {'x': [1]}
print(deque(range(5), maxlen=3))                # deque([2, 3, 4], maxlen=3)      a ring buffer
cm = ChainMap({"a": 1}, {"a": 2, "b": 3})
print(cm["a"], cm["b"], sorted(cm))             # 1 3 ['a', 'b']       lookups try each dict in turn
od = OrderedDict(a=1, b=2)
od.move_to_end("a")
print(list(od))                                 # ['b', 'a']

# 5. heapq and bisect
heap = []
for n in (5, 1, 4, 2, 3):
    heapq.heappush(heap, n)
print([heapq.heappop(heap) for _ in range(5)], heapq.nsmallest(2, [5, 1, 4]), heapq.nlargest(2, [5, 1, 4]))
# [1, 2, 3, 4, 5] [1, 4] [5, 4]
print(bisect.bisect_left([1, 3, 5], 4))         # 2      where 4 belongs in a sorted list

# 6. string constants and platform information
print(string.ascii_lowercase[:5], string.digits, string.punctuation[:5])    # abcde 0123456789 !"#$%
print(platform.system() in ("Windows", "Linux", "Darwin"), isinstance(platform.python_version(), str))
# True True

# 7. ast: look at code without running it
print(ast.literal_eval("[1, 2, {'a': 3}]"))     # [1, 2, {'a': 3}]       a SAFE eval for plain data
try:
    ast.literal_eval("__import__('os')")
except ValueError:
    print("ValueError")                         # code is refused
tree = ast.parse("x = 1 + 2")
print(type(tree.body[0]).__name__, [type(node).__name__ for node in ast.walk(tree)][:3])
# Assign ['Module', 'Assign', 'Name']

# 8. dis: the bytecode Python runs
print(len(list(dis.get_instructions(lambda x: x + 1))) > 0)     # True      dis.dis(func) prints it

# 9. Run a module as a program: python -m something
out = subprocess.run([sys.executable, "-m", "json.tool"], input='{"b": 1, "a": [1, 2]}',
                     capture_output=True, text=True).stdout
print(out.strip())
# {
#     "b": 1,
#     "a": [
#         1,
#         2
#     ]
# }
print(subprocess.run([sys.executable, "-c", "print(1 + 1)"], capture_output=True, text=True).stdout.strip())  # 2

# 10. unittest: the built-in test framework
class MathTests(unittest.TestCase):
    def test_add(self):
        self.assertEqual(1 + 1, 2)

    def test_raises(self):
        with self.assertRaises(ZeroDivisionError):
            1 / 0

suite = unittest.defaultTestLoader.loadTestsFromTestCase(MathTests)
result = unittest.TextTestRunner(stream=io.StringIO()).run(suite)
print(result.testsRun, result.wasSuccessful())  # 2 True
# From the terminal:  python -m unittest -v      (pytest, Module 20, is easier to write)

# USEFUL "python -m" TOOLS
#   python -m http.server 8000      serve the current folder at http://localhost:8000
#   python -m json.tool file.json   pretty-print JSON            python -m venv .venv
#   python -m timeit "sum(range(100))"   quick timing             python -m zipfile -l a.zip
#   python -m pdb script.py         the debugger                  python -m pydoc -b   documentation browser
#   python -m calendar 2026         a printed calendar            python -m this       the Zen of Python