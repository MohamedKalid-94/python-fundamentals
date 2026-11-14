def add(a, b):
    return a + b


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("cannot divide by zero")
    return a / b


def is_even(n):
    return n % 2 == 0


def average(numbers):
    if not numbers:
        raise ValueError("numbers must not be empty")
    return sum(numbers) / len(numbers)