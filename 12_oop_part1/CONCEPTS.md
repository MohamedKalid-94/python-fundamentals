# Module 12: OOP Part 1, Concepts Summary

| # | Topic | Concept | Remember |
|---|---|---|---|
| 01 | OOP Concepts | Idea | Bundle data (attributes) and behaviour (methods) in one class |
| 01 | OOP Concepts | Vocabulary | class = blueprint, object = instance, attribute, method, `self` |
| 01 | OOP Concepts | Four pillars | Encapsulation, abstraction, inheritance, polymorphism |
| 01 | OOP Concepts | Everything | In Python every value is an object, and a class is an object too (`type(int)` is `type`) |
| 02 | Classes & Objects | Create | `class Dog:` then `rex = Dog("Rex", 3)` |
| 02 | Classes & Objects | `self` | The object itself: `rex.bark()` is `Dog.bark(rex)` |
| 02 | Classes & Objects | Instance data | Each object has its own `__dict__` |
| 02 | Classes & Objects | Equality | Default `==` compares identity; define `__eq__` to compare content |
| 02 | Classes & Objects | `__str__` / `__repr__` | `__str__` is for people (`print`), `__repr__` for developers and containers |
| 02 | Classes & Objects | References | Objects are passed by reference; functions can change them |
| 02 | Classes & Objects | Names | Classes use `CapWords`; methods and attributes use `snake_case` |
| 03 | Class Attributes | Class vs instance | A class attribute is shared; an instance attribute belongs to one object |
| 03 | Class Attributes | Shadowing | `obj.attr = x` creates an instance attribute that hides the class one |
| 03 | Class Attributes | Counter | `Dog.count += 1` inside `__init__` counts the objects |
| 03 | Class Attributes | `+=` trap | `obj.n += 1` creates `obj.n`; the class value stays |
| 03 | Class Attributes | Mutable trap | A list or dict class attribute is shared by every object |
| 03 | Class Attributes | Constants | `Uart.DEFAULT_BAUD`, `UPPER_CASE` by convention |
| 03 | Class Attributes | Subclasses | `type(self).count += 1` keeps a separate counter per subclass |
| 04 | Class Methods | `@classmethod` | First parameter is `cls` (the class) |
| 04 | Class Methods | Use | Alternative constructors (`from_string`, `from_fahrenheit`) and class state |
| 04 | Class Methods | Subclasses | `cls(...)` builds an object of the class that was called |
| 04 | Class Methods | Calling | On the class or on an object |
| 05 | Static Methods | `@staticmethod` | No `self` and no `cls` |
| 05 | Static Methods | Use | Helper functions that belong to the topic (`is_valid_age`, `crc8`) |
| 05 | Static Methods | Choose | Needs the object: instance; needs the class: class method; needs neither: static |
| 05 | Static Methods | Calling | `Class.method()` or `obj.method()` |
| 06 | Constructors | `__init__` | The initializer: runs after the object is created and must return `None` |
| 06 | Constructors | Arguments | Defaults, keyword-only (`*`), and `TypeError` when required ones are missing |
| 06 | Constructors | Validate | Raise `ValueError` so a bad object cannot exist |
| 06 | Constructors | No overloading | Use defaults and class-method constructors |
| 06 | Constructors | Mutable default | `items=[]` is shared; use `None` and create the list inside |
| 06 | Constructors | `__new__` | Creates the object, then `__init__` runs |
| 06 | Constructors | `__del__` | Destructor; timing is not guaranteed, so use `with` for cleanup |
| 07 | Access Modifiers | `name` | Public |
| 07 | Access Modifiers | `_name` | Protected by convention (internal use) |
| 07 | Access Modifiers | `__name` | Private by name mangling: stored as `_Class__name` |
| 07 | Access Modifiers | Not security | `obj._Class__name` still works |
| 07 | Access Modifiers | Mangling scope | Only inside the class body; `obj.__x = 1` outside creates a new attribute |
| 07 | Access Modifiers | Purpose | Avoid name clashes with subclasses |
| 08 | Inheritance | Syntax | `class Dog(Animal):` |
| 08 | Inheritance | `super()` | Calls the parent: `super().__init__(...)` and `super().speak()` |
| 08 | Inheritance | Forgetting `super().__init__` | Parent attributes are missing (`AttributeError`) |
| 08 | Inheritance | Checks | `isinstance(obj, Class)`, `issubclass(A, B)`, `type(obj) is Class` |
| 08 | Inheritance | Lookup | Object, then class, then parents (`__mro__`) |
| 08 | Inheritance | Root | Every class inherits from `object` |
| 09 | Multiple Inheritance | Syntax | `class C(A, B):` |
| 09 | Multiple Inheritance | MRO | The leftmost parent wins; see `C.__mro__` |
| 09 | Multiple Inheritance | Diamond | `super()` follows the MRO so a shared parent runs once |
| 09 | Multiple Inheritance | Mixins | Small classes that add one ability (`JsonMixin`, `LogMixin`) |
| 09 | Multiple Inheritance | Bad order | An impossible MRO raises `TypeError` when the class is created |
| 09 | Multiple Inheritance | Advice | Prefer mixins and composition over deep multiple inheritance |
| 10 | Multilevel | Chain | `Vehicle -> Car -> ElectricCar` |
| 10 | Multilevel | Init order | Parents initialise first when each `__init__` calls `super().__init__` |
| 10 | Multilevel | Types | Single, multiple, multilevel, hierarchical (one parent, many children), hybrid |
| 10 | Multilevel | Depth | More than 3 levels gets hard to read |
| 11 | Polymorphism | Idea | The same call behaves differently depending on the object |
| 11 | Polymorphism | Inheritance | Subclasses override a method, callers use the base type |
| 11 | Polymorphism | Duck typing | Any object with the needed method works; no common parent required |
| 11 | Polymorphism | Built-ins | `len`, `+`, `max` work on many types |
| 11 | Polymorphism | Operators | `__add__`, `__mul__`, `__eq__`, `__repr__` give your class operator support |
| 11 | Polymorphism | `__eq__` | Defining it without `__hash__` makes objects unhashable |
| 11 | Polymorphism | Interface | Raise `NotImplementedError` in the base method |
| 12 | Examples | Encapsulation | Private balance, validated deposits, history list |
| 12 | Examples | Data structures | Stack and linked list as classes |
| 12 | Examples | Hierarchy | `Device -> Sensor -> TempSensor`, with a static helper |
| 12 | Examples | Mixins | A `LogMixin` adds `log()` to any class |