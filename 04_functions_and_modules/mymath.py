"""A small module used by 10_modules.py."""

PI = 3.14159


def square(x):
    return x * x


def circle_area(r):
    return PI * square(r)


def _private_helper():
    return "internal"


print("mymath loaded, __name__ =", __name__)

if __name__ == "__main__":
    # This block runs only when the file is executed directly
    print("running mymath directly")
    print(square(4))