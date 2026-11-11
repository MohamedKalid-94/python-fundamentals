"""Small module used to show docstrings and doctest."""

import doctest
import inspect

# A DOCSTRING is a string literal that is the FIRST statement of a module, class or function.
# It becomes the object's __doc__, and tools (help(), editors, Sphinx) show it.


def add(a, b):
    """Return the sum of a and b.

    >>> add(2, 3)
    5
    >>> add("a", "b")
    'ab'
    """
    return a + b


def greet(name, punctuation="!"):
    """Return a greeting.

    Args:
        name: Who to greet.
        punctuation: The last character (default "!").

    Returns:
        The greeting text.

    Raises:
        TypeError: If name is not a string.

    >>> greet("Ann")
    'Hello, Ann!'
    """
    if not isinstance(name, str):
        raise TypeError("name must be a string")
    return f"Hello, {name}{punctuation}"


class Circle:
    """A circle.

    >>> Circle(2).area()
    12.57
    """

    def __init__(self, radius):
        self.radius = radius

    def area(self):
        """Return the area rounded to 2 decimals."""
        return round(3.14159 * self.radius ** 2, 2)


# 1. Reading docstrings
print(add.__doc__.splitlines()[0])              # Return the sum of a and b.
print(inspect.getdoc(greet).splitlines()[0])    # Return a greeting.
print(Circle.__doc__.splitlines()[0], "|", Circle.area.__doc__)     # A circle. | Return the area rounded to 2 decimals.
print(__doc__)                                  # Small module used to show docstrings and doctest.
print(len.__doc__)                              # Return the number of items in a container.
# help(greet) shows the same text formatted; python -m pydoc 15_docstrings opens it from the terminal.

# 2. __doc__ is an ordinary attribute
def noted():
    pass

print(noted.__doc__)                            # None
noted.__doc__ = "set later"
print(noted.__doc__)                            # set later

# 3. doctest: the examples inside docstrings are TESTS
print(doctest.testmod())                        # TestResults(failed=0, attempted=4)

# What a failing example looks like (we hide the details with out=)
test = doctest.DocTestParser().get_doctest(">>> 1 + 1\n3\n", {}, "demo", None, 0)
runner = doctest.DocTestRunner(verbose=False)
print(runner.run(test, out=lambda text: None))  # TestResults(failed=1, attempted=1)
# From the terminal:  python -m doctest -v 15_docstrings.py

# CONVENTIONS (PEP 257)
#  - Triple double quotes """..."""  even for one line.
#  - First line: a short summary in the imperative mood ("Return ...", not "Returns ...").
#  - Then a blank line, then details. Describe WHAT and WHY, not HOW the code works line by line.
#  - Document: the arguments, the return value, the exceptions, and side effects.
#  - Classes: a docstring for the class, plus one for every public method.
#  - Comments (#) explain WHY something is done; docstrings explain WHAT it is for.
#
# THREE POPULAR LAYOUTS FOR THE DETAILS
#   Google style    Args: / Returns: / Raises:       (used above, easy to read)
#   NumPy style     Parameters / Returns with underlines (data science libraries)
#   reST / Sphinx   :param name: text   :returns: text
# TOOLS   Sphinx and MkDocs (+ mkdocstrings) build a website from docstrings; pdoc is quick.
# TYPES   Put types in annotations (def f(x: int) -> str), not in the docstring.
# python -OO removes all docstrings (smaller memory): never depend on __doc__ at run time.