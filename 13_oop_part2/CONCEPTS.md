# Module 13: OOP Part 2, Concepts Summary

| # | Topic | Concept | Remember |
|---|---|---|---|
| 01 | Overriding | What | A child defines a method with the same name as its parent's; the child's version wins |
| 01 | Overriding | `super()` | Extends the parent's version instead of replacing it |
| 01 | Overriding | Attributes | Class attributes and constants can be overridden too |
| 01 | Overriding | Parent calls child | `self.method()` inside the parent runs the child's override |
| 01 | Overriding | Signature | Keep it compatible, or callers written for the parent break |
| 01 | Overriding | Built-ins | You can override methods of `list`, `dict` and others (prefer `UserList`, `UserDict`) |
| 01 | Overriding | No `final` | Python cannot forbid overriding (`typing.final` is only a hint) |
| 02 | Overloading | Not supported | The last `def` with a name replaces the earlier ones |
| 02 | Overloading | Alternatives | Default arguments, `*args`, `isinstance` checks, `functools.singledispatch`, keyword-only options |
| 02 | Overloading | `singledispatch` | Picks the function by the type of the FIRST argument; `singledispatchmethod` for methods |
| 02 | Overloading | `typing.overload` | Only describes variants for type checkers |
| 02 | Overloading | Operator overloading | `__add__`, `__radd__`, `__eq__` define what operators mean for your class; return `NotImplemented` for unknown types |
| 03 | Dynamic Binding | What | The method that runs is chosen at CALL time from the real object type |
| 03 | Dynamic Binding | Runtime changes | Methods can be added to a class later; instance attributes hide class methods |
| 03 | Dynamic Binding | Bound method | Remembers its object (`__self__`) and function (`__func__`) |
| 03 | Dynamic Binding | Errors | A missing method raises `AttributeError` only when that line runs |
| 03 | Dynamic Binding | vs C | Like a vtable of function pointers; every Python call works this way |
| 04 | Dynamic Typing | Names | A name has no type; the value has one |
| 04 | Dynamic Typing | Strong | `"5" + 5` raises `TypeError`; there is no silent mixing |
| 04 | Dynamic Typing | Hints | Annotations are not enforced at run time |
| 04 | Dynamic Typing | `isinstance` | `isinstance(True, int)` is `True`; `type(True) is int` is `False` |
| 04 | Dynamic Typing | LBYL / EAFP | Check first (`hasattr`) or try and catch (`try/except`); EAFP is common in Python |
| 04 | Dynamic Typing | Checkers | `mypy` and Pyright read the hints before you run the code |
| 05 | Abstraction | `ABC` | `class Shape(ABC):` with `@abstractmethod` methods |
| 05 | Abstraction | Instantiation | An abstract class, or a subclass that misses a method, raises `TypeError` |
| 05 | Abstraction | Concrete methods | An abstract class can contain normal methods that use the abstract ones |
| 05 | Abstraction | Abstract body | The abstract method may have code that children call with `super()` |
| 05 | Abstraction | Abstract property | `@property` above `@abstractmethod` |
| 05 | Abstraction | vs encapsulation | Abstraction hides complexity (WHAT you call); encapsulation protects data (WHERE it lives) |
| 06 | Encapsulation | `@property` | Looks like an attribute but runs a getter |
| 06 | Encapsulation | Setter | `@name.setter` validates new values |
| 06 | Encapsulation | Read-only | A property without a setter raises `AttributeError` when assigned |
| 06 | Encapsulation | Computed | A property can calculate its value (`fahrenheit`, `area`) |
| 06 | Encapsulation | Deleter | `@name.deleter` |
| 06 | Encapsulation | `cached_property` | Computed once, then stored |
| 06 | Encapsulation | Advice | Start with a plain attribute; add a property later without breaking callers; skip Java-style getters |
| 07 | Interfaces | No keyword | Use an ABC, a `Protocol`, or duck typing |
| 07 | Interfaces | ABC interface | Only abstract methods; a class can implement several; enforced at creation |
| 07 | Interfaces | `Protocol` | Matches by having the methods, no inheritance needed; `@runtime_checkable` allows `isinstance` |
| 07 | Interfaces | `register` | `Plugin.register(External)` makes a class you cannot change a virtual subclass |
| 07 | Interfaces | Testing | A fake with the same methods replaces the real device |
| 08 | Packages | Package | A folder with `__init__.py` that holds modules |
| 08 | Packages | `__init__.py` | Runs once on import; re-export names with `from .shapes import Circle` |
| 08 | Packages | Imports | `import pkg.mod`, `from pkg import mod`, `from pkg.mod import name as alias` |
| 08 | Packages | Relative vs absolute | `.` and `..` inside the package; the full path outside |
| 08 | Packages | `__all__` | The names exported by `from pkg import *` |
| 08 | Packages | Cache | Imported modules live in `sys.modules`; `importlib.import_module("a.b")` imports by string |
| 08 | Packages | Circular imports | Avoid them; move shared code to a third module |
| 09 | Inner Classes | What | A class defined inside another class, reached as `Outer.Inner` |
| 09 | Inner Classes | Outer object | Not visible automatically; pass `self` in |
| 09 | Inner Classes | Names | `__qualname__` is `Outer.Inner` |
| 09 | Inner Classes | Style | A module-level `_Helper` class is often clearer than nesting |
| 09 | Inner Classes | In functions | A class inside a function can use the function's variables |
| 10 | Anonymous | Dynamic class | `type("Name", bases, attributes)` |
| 10 | Anonymous | `SimpleNamespace` | A quick object with attributes; `object_hook` turns JSON into objects |
| 10 | Anonymous | `object()` | A unique plain object (sentinel) |
| 10 | Anonymous | Callable object | `__call__` lets an object behave like a function with state |
| 10 | Anonymous | Temporary object | `Temp()` without a name is destroyed right after the statement |
| 10 | Anonymous | `lambda` | The anonymous function |
| 11 | Singleton | Idea | One object only, however many times you create it |
| 11 | Singleton | `__new__` | Keep `_instance` and return it; `__init__` still runs every time (trap) |
| 11 | Singleton | Other ways | A decorator, a metaclass, or simply a module-level variable |
| 11 | Singleton | Threads | Protect creation with `threading.Lock` if threads may race |
| 11 | Singleton | Caution | Global state makes tests harder |
| 12 | Wrapper Classes | Python values | `int`, `float`, `str`, `bool` are already objects |
| 12 | Wrapper Classes | Subclass a value | `class Positive(int)` with `__new__` for validation |
| 12 | Wrapper Classes | Delegation | `__getattr__` forwards unknown names; special methods like `__len__` are NOT forwarded |
| 12 | Wrapper Classes | `UserList` / `UserDict` | The safe base classes for custom containers |
| 12 | Wrapper Classes | Adapter | A wrapper that makes one interface fit another |
| 12 | Wrapper Classes | `NewType` | A name for type checkers only; at run time it is the plain type |
| 13 | Enums | Define | `class Color(Enum): RED = 1` |
| 13 | Enums | Access | `.name`, `.value`, `Color(1)`, `Color["RED"]`, `list(Color)` |
| 13 | Enums | Compare | Members are singletons: use `==` or `is`; `Color.RED == 1` is `False` |
| 13 | Enums | Constants | Members cannot be reassigned; plain enums have no ordering |
| 13 | Enums | Aliases | Same value, one member; `@unique` forbids it |
| 13 | Enums | Helpers | `auto()` for values, `IntEnum` (an int), `IntFlag` (bit flags), `StrEnum` (3.11+) |
| 13 | Enums | Extras | Methods, tuple values with `__init__`, use in `match` |
| 14 | Reflection | Look | `type`, `dir`, `vars`, `__dict__`, `__class__`, `__doc__`, `__mro__`, `__subclasses__()` |
| 14 | Reflection | Change | `getattr`, `setattr`, `hasattr`, `delattr` with a name stored in a string |
| 14 | Reflection | `inspect` | `signature`, `getmembers`, `isfunction`, `getsource` |
| 14 | Reflection | Dispatch | `getattr(self, f"do_{cmd}", None)` selects a handler by name |
| 14 | Reflection | Safety | Never feed unchecked user text to `getattr`, `eval` or `exec` |
| 15 | Data Classes | `@dataclass` | Generates `__init__`, `__repr__` and `__eq__` from annotated fields |
| 15 | Data Classes | Options | `frozen=True` (immutable and hashable), `order=True`, `kw_only=True`, `slots=True` |
| 15 | Data Classes | Defaults | A mutable default needs `field(default_factory=list)` |
| 15 | Data Classes | `__post_init__` | Validation and computed fields (`field(init=False)`) |
| 15 | Data Classes | Hide | `field(repr=False)` |
| 15 | Data Classes | Helpers | `asdict`, `astuple`, `replace`, `fields` |
| 15 | Data Classes | Field order | A field without a default cannot follow one with a default |
| 16 | Examples | Factory | A dict from `Enum` member to class builds objects |
| 16 | Examples | State machine | Enum states in a dataclass |
| 16 | Examples | Register | Property setter validates 0..255; `IntFlag` names the bits |
| 16 | Examples | Event bus | A singleton holding callable subscribers |