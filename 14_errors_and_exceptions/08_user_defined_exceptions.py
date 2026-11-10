# Create your own exception by subclassing Exception.

# 1. The smallest version
class EmptyStackError(Exception):
    """Raised when popping from an empty stack."""


class Stack:
    def __init__(self):
        self._items = []

    def pop(self):
        if not self._items:
            raise EmptyStackError("stack is empty")
        return self._items.pop()


try:
    Stack().pop()
except EmptyStackError as e:
    print(e)                                    # stack is empty


# 2. A family of errors with a common base class
class AppError(Exception):
    """Base class for every error of this application."""


class ValidationError(AppError):
    def __init__(self, field, message):
        super().__init__(f"{field}: {message}")
        self.field = field
        self.message = message


class InsufficientFunds(AppError):
    def __init__(self, balance, amount):
        super().__init__(f"balance {balance} is less than {amount}")
        self.balance = balance
        self.amount = amount
        self.shortfall = amount - balance


try:
    raise ValidationError("age", "must be positive")
except ValidationError as e:
    print(e, "|", e.field)                      # age: must be positive | age

try:
    raise InsufficientFunds(50, 80)
except AppError as e:                           # the base class catches every child
    print(type(e).__name__, e, e.shortfall)     # InsufficientFunds balance 50 is less than 80 30

print([c.__name__ for c in ValidationError.__mro__])
# ['ValidationError', 'AppError', 'Exception', 'BaseException', 'object']
print(issubclass(ValidationError, AppError))    # True

for exc in (ValidationError("a", "b"), InsufficientFunds(1, 2)):
    try:
        raise exc
    except AppError as e:
        print("app error:", type(e).__name__)
# app error: ValidationError
# app error: InsufficientFunds


# 3. Error codes and a custom __str__
class DeviceError(Exception):
    def __init__(self, code, text):
        super().__init__(code, text)
        self.code = code
        self.text = text

    def __str__(self):
        return f"[E{self.code:03d}] {self.text}"


try:
    raise DeviceError(7, "bus busy")
except DeviceError as e:
    print(e, e.code)                            # [E007] bus busy 7


# 4. A hierarchy that lets callers choose how precise to be
class SensorError(Exception):
    pass


class SensorTimeout(SensorError):
    pass


class SensorCrc(SensorError):
    pass


for exc in (SensorTimeout("t"), SensorCrc("c")):
    try:
        raise exc
    except SensorError as e:
        print(type(e).__name__)
# SensorTimeout
# SensorCrc

# GUIDELINES
# - Names end with "Error" (ValidationError). Warnings end with "Warning".
# - Inherit from Exception (never from BaseException).
# - One base class per package/application, so users can catch everything with one except.
# - Create a custom type only when callers need to treat it differently;
#   otherwise ValueError, TypeError or RuntimeError are fine.
# - Call super().__init__(...) so str(e) and e.args work.
# - Put useful data on the object (field, code, shortfall), not only in the message.