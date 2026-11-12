# Module 19: Advanced Concepts A, Concepts Summary

| # | Topic | Concept | Remember |
|---|---|---|---|
| 01 | ABCs | `collections.abc` | `Iterable`, `Sized`, `Container`, `Callable`, `Sequence`, `MutableSequence`, `Mapping`, `MutableMapping`, `Set`, `Iterator` describe what an object can do |
| 01 | ABCs | Mixin methods | Write the abstract methods; receive the rest (`Sequence` gives `index`, `count`, `__contains__`, `__reversed__`; `MutableMapping` gives `get`, `update`, `pop`, `setdefault`, `items`, `==`) |
| 01 | ABCs | Enforcement | An abstract class, or a child with an abstract method left, raises `TypeError` when you CREATE an object |
| 01 | ABCs | `__subclasshook__` | Decide `isinstance` by structure (`"close" in B.__dict__`); return `NotImplemented` to fall back |
| 01 | ABCs | `register` | Makes a virtual subclass: `issubclass` is `True`, but it is not in the MRO and inherits nothing |
| 01 | ABCs | Abstract kinds | `@classmethod` + `@abstractmethod`, `@staticmethod` + `@abstractmethod`, `@property` + `@abstractmethod` |
| 01 | ABCs | Abstract is not "uncallable" | An abstract method can still be called (`Codec.create()`); it only blocks creating objects |
| 01 | ABCs | Template method | The base class fixes the steps, the children implement them |
| 01 | ABCs | Inspect | `inspect.isabstract`, `Cls.__abstractmethods__` |
| 01 | ABCs | `numbers` | `Number` > `Complex` > `Real` > `Rational` > `Integral`; `Decimal` is a `Number` but not a `Real` |
| 01 | ABCs | Metaclass | `ABC` is `ABCMeta` |
| 02 | Custom Exceptions | Base class | One per library: code, message, context data, `to_dict()` |
| 02 | Custom Exceptions | Join a built-in family | `class NotFoundError(AppError, LookupError)` is caught by `except LookupError` |
| 02 | Custom Exceptions | Policy in the error | `retryable = True` lets a generic retry loop decide |
| 02 | Custom Exceptions | Translate | `raise MyError(...) from original`, or a decorator doing it |
| 02 | Custom Exceptions | Pickling | Pass every constructor argument to `super().__init__` (Python rebuilds with `cls(*args)`) |
| 02 | Custom Exceptions | Groups | `ExceptionGroup` and `except*` for several errors at once (3.11+) |
| 02 | Custom Exceptions | Global handler | `sys.excepthook` runs for an unhandled exception |
| 02 | Custom Exceptions | Notes | `e.add_note(text)` and `e.__notes__` (3.11+) |
| 03 | Higher-order | Definition | Takes a function, returns a function, or both |
| 03 | Higher-order | Compose / pipe | `compose(f, g)(x)` is `f(g(x))`; `pipe(x, f, g)` is `g(f(x))` |
| 03 | Higher-order | `reduce` | `reduce(func, items, start)`; `accumulate` keeps every step |
| 03 | Higher-order | `partial` | Fixes arguments (`partial(int, base=2)`); `partialmethod` for methods |
| 03 | Higher-order | Sorting | `key=`, `operator.itemgetter`, `attrgetter`, `methodcaller`, `cmp_to_key` |
| 03 | Higher-order | Currying | `f(a)(b)(c)` built from `f.__code__.co_argcount` |
| 03 | Higher-order | Patterns | Strategy (a dict of functions), callbacks, thunks (`lazy`), callable objects (`__call__`) |
| 03 | Higher-order | Introspection | `inspect.signature`; functions can carry attributes |
| 04 | Object Internals | Identity | `id`, `is`, `type`, `__class__` |
| 04 | Object Internals | `__dict__` | Instance attributes live in it; methods live in the class |
| 04 | Object Internals | Lookup order | Data descriptor (property), instance `__dict__`, class and MRO, then `__getattr__` |
| 04 | Object Internals | Hooks | `__getattribute__` (every lookup), `__getattr__` (failed lookup), `__setattr__`, `__delattr__`; use `object.__setattr__` to bypass |
| 04 | Object Internals | Binding | A method is a function plus `__get__`: `obj.m(x)` is `type(obj).m(obj, x)` |
| 04 | Object Internals | Function parts | `__code__`, `__defaults__`, `__kwdefaults__`, `__annotations__`, `__globals__`, `__closure__` |
| 04 | Object Internals | `__eq__` and `__hash__` | Defining `__eq__` alone removes hashing |
| 04 | Object Internals | Truth value | `__bool__`, otherwise `__len__` |
| 04 | Object Internals | `__slots__` | No per-object `__dict__`: less memory, no new attributes |
| 04 | Object Internals | `__set_name__` | A class attribute learns its own name |
| 05 | Memory | Reference counting | Freed at once when the count reaches 0 (CPython); `sys.getrefcount` counts the call's own argument |
| 05 | Memory | Cycles | Need the cyclic collector: `gc.collect()`; three generations |
| 05 | Memory | `gc` | `disable`, `enable`, `collect`, `get_threshold`, `get_count`, `get_referents`, `get_referrers`, `freeze` |
| 05 | Memory | Sizes | `sys.getsizeof` is shallow: write `deep_size` and count shared objects once |
| 05 | Memory | Growth | Lists over-allocate in steps |
| 05 | Memory | Compact types | `array`, tuples, `__slots__`, generators, `memoryview` |
| 05 | Memory | Sharing | Small integers are cached; do not use `is` on numbers |
| 05 | Memory | Tracing | `tracemalloc.take_snapshot().statistics("lineno")` |
| 05 | Memory | Layout | pymalloc arenas and pools: freed memory may not return to the OS |
| 05 | Memory | Rule | Never depend on WHEN an object is freed; use `with` for cleanup |
| 06 | Metaclasses | Idea | A class is an object; its type is its metaclass (default `type`) |
| 06 | Metaclasses | `type(name, bases, ns)` | What a `class` statement does |
| 06 | Metaclasses | Hooks | `__prepare__` (namespace), `__new__` (create), `__init__` (initialise), `__call__` (when you call the class) |
| 06 | Metaclasses | Order | `new C`, `init C`, then per object: `call C`, `C.__init__` |
| 06 | Metaclasses | Uses | Validate at definition time, registries, change the namespace, count instances, custom `isinstance` |
| 06 | Metaclasses | Metaclass methods | Belong to the class, not to its instances |
| 06 | Metaclasses | Conflict | Two parents with different metaclasses need a combined metaclass |
| 06 | Metaclasses | Simpler first | Class decorator, `__init_subclass__`, descriptor |
| 07 | Metaprogramming | Declarative models | `Field` descriptors + `__set_name__` + a metaclass that collects `_fields` (ORM style) |
| 07 | Metaprogramming | Wrap methods | A metaclass or decorator wraps every function (`inspect.isfunction`) |
| 07 | Metaprogramming | `__init_subclass__` | `class Csv(Plugin, key="csv")` passes keywords to the registry |
| 07 | Metaprogramming | Class decorator | Writes `__repr__` and `__eq__` from `__annotations__` |
| 07 | Metaprogramming | Dynamic classes | `type(...)`, `types.new_class`, `setattr` in a loop |
| 07 | Metaprogramming | Generated code | `exec` of source text; validate names with `isidentifier()` |
| 07 | Metaprogramming | Proxy | `__getattr__` delegates and records calls |
| 07 | Metaprogramming | Signature checks | `inspect.signature(func).bind(...)` plus `__annotations__` |
| 07 | Metaprogramming | Safety | Never `eval` or `exec` text from outside; a restricted globals dict is not a sandbox |