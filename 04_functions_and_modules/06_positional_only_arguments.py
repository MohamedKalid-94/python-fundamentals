# Parameters BEFORE a "/" can only be passed by position (Python 3.8+)

def area(length, width, /):
    return length * width

print(area(3, 4))               # 12

try:
    area(length=3, width=4)
except TypeError as e:
    print(e)
# area() got some positional-only arguments passed as keyword arguments: 'length, width'

# All three kinds together
def demo(a, b, /, c, *, d):
    return a, b, c, d
#           |    |      |
#           |    |      +-- keyword-only (after *)
#           |    +--------- positional OR keyword
#           +-------------- positional-only (before /)

print(demo(1, 2, 3, d=4))       # (1, 2, 3, 4)
print(demo(1, 2, c=3, d=4))     # (1, 2, 3, 4)

# Built-ins use this: len(obj, /)
try:
    len(obj=[1, 2])
except TypeError as e:
    print(type(e).__name__)     # TypeError

# WHY: the parameter names are not part of the public interface,
# so you can rename them later without breaking callers.