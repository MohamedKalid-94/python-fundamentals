# SINGLETON: a class that has only ONE object, however many times you "create" it.
# Typical uses: configuration, a logger, a hardware peripheral (one UART).

# --- 1. With __new__ ---
class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


a = Singleton()
b = Singleton()
print(a is b)                               # True


# TRAP: __init__ runs on EVERY call, even though the object is the same
class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        print("init")
        self.values = {}                    # reset every time!


c1 = Config()
c1.values["a"] = 1
c2 = Config()
print(c2.values, c1 is c2)                  # {} True       the data was wiped
# init
# init


# FIX: set the data inside __new__ (only the first time)
class Settings:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.values = {}
        return cls._instance


s1 = Settings()
s1.values["debug"] = True
s2 = Settings()
print(s2.values, s1 is s2)                  # {'debug': True} True


# --- 2. With a decorator ---
def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class Logger:
    def __init__(self):
        self.lines = []

    def log(self, message):
        self.lines.append(message)


l1 = Logger()
l2 = Logger()
l1.log("a")
print(l2.lines, l1 is l2)                   # ['a'] True
# (Logger is now a function, so isinstance(l1, Logger) no longer works.)


# --- 3. With a metaclass (metaclasses are explained in Module 19) ---
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    def __init__(self):
        print("connecting")


d1 = Database()
d2 = Database()
print(d1 is d2)
# connecting          (printed only once)
# True

# --- 4. The simplest Pythonic singleton: a MODULE ---
# A module is imported only once, so a variable in app_settings.py is shared everywhere:
#     app_settings.py:   settings = {"debug": False}
#     any other file:    from app_settings import settings

# NOTES
# - Threads: two threads could create two objects at the same moment.
#   Protect the creation with threading.Lock if that can happen.
# - A singleton is global state: it makes tests harder. Prefer passing the object in
#   (dependency injection) unless you really need exactly one.