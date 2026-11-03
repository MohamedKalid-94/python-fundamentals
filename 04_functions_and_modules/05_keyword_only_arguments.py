# Parameters AFTER a bare * can only be passed by keyword

def connect(host, *, port=80, timeout=5):
    return f"{host}:{port} (timeout={timeout})"

print(connect("example.com"))                 # example.com:80 (timeout=5)
print(connect("example.com", port=8080))      # example.com:8080 (timeout=5)

try:
    connect("example.com", 8080)
except TypeError as e:
    print(e)        # connect() takes 1 positional argument but 2 were given

# Keyword-only parameters can be REQUIRED (no default)
def resize(image, *, width, height):
    return f"{image} -> {width}x{height}"

print(resize("a.png", width=10, height=20))   # a.png -> 10x20

try:
    resize("a.png", width=10)
except TypeError as e:
    print(e)        # resize() missing 1 required keyword-only argument: 'height'

# After *args, parameters are automatically keyword-only
def total(*numbers, scale=1):
    return sum(numbers) * scale

print(total(1, 2, 3))                         # 6
print(total(1, 2, 3, scale=10))               # 60

# WHY: stops confusing calls like  connect("x", 8080, 3)
# Built-ins do this: print(sep=...), sorted(key=...)