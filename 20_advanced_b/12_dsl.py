import operator
import re

# A DSL (Domain-Specific Language) is a small language for ONE kind of problem.
#   internal DSL   written inside Python (operators, method chains, "with" blocks, decorators)
#   external DSL   its own syntax that you parse (SQL, regex, config files, a calculator language)

# ---------- INTERNAL DSLs ----------

# 1. Operator overloading: write filters as readable expressions
OPS = {">": operator.gt, ">=": operator.ge, "<": operator.lt,
       "<=": operator.le, "==": operator.eq, "!=": operator.ne}

class Expr:
    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def __invert__(self):
        return Not(self)

class Compare(Expr):
    def __init__(self, name, op, value):
        self.name, self.op, self.value = name, op, value

    def test(self, record):
        return OPS[self.op](record[self.name], self.value)

    def __repr__(self):
        return f"{self.name} {self.op} {self.value!r}"

class And(Expr):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def test(self, record):
        return self.left.test(record) and self.right.test(record)

    def __repr__(self):
        return f"({self.left} and {self.right})"

class Or(And):
    def test(self, record):
        return self.left.test(record) or self.right.test(record)

    def __repr__(self):
        return f"({self.left} or {self.right})"

class Not(Expr):
    def __init__(self, inner):
        self.inner = inner

    def test(self, record):
        return not self.inner.test(record)

    def __repr__(self):
        return f"not ({self.inner})"

class Field:
    def __init__(self, name):
        self.name = name

    def __gt__(self, value):
        return Compare(self.name, ">", value)

    def __ge__(self, value):
        return Compare(self.name, ">=", value)

    def __lt__(self, value):
        return Compare(self.name, "<", value)

    def __le__(self, value):
        return Compare(self.name, "<=", value)

    def __eq__(self, value):
        return Compare(self.name, "==", value)

    def __ne__(self, value):
        return Compare(self.name, "!=", value)

age, country = Field("age"), Field("country")
records = [
    {"name": "Ann", "age": 30, "country": "IN"},
    {"name": "Bob", "age": 17, "country": "IN"},
    {"name": "Cy", "age": 40, "country": "US"},
]

rule = (age > 18) & (country == "IN")           # parentheses are needed: & binds tighter than >
print(rule)                                     # (age > 18 and country == 'IN')
print([r["name"] for r in records if rule.test(r)])             # ['Ann']
rule2 = (age < 18) | ~(country == "IN")
print(rule2)                                    # (age < 18 or not (country == 'IN'))
print([r["name"] for r in records if rule2.test(r)])            # ['Bob', 'Cy']

# 2. A "with"-block DSL: build HTML with the nesting of your code
class HTML:
    def __init__(self):
        self.lines, self.depth = [], 0

    def tag(self, name, **attrs):
        return _Tag(self, name, attrs)

    def text(self, value):
        self.lines.append("  " * self.depth + value)

class _Tag:
    def __init__(self, html, name, attrs):
        self.html, self.name = html, name
        self.attrs = "".join(f' {k.rstrip("_")}="{v}"' for k, v in attrs.items())

    def __enter__(self):
        self.html.lines.append("  " * self.html.depth + f"<{self.name}{self.attrs}>")
        self.html.depth += 1

    def __exit__(self, *exc):
        self.html.depth -= 1
        self.html.lines.append("  " * self.html.depth + f"</{self.name}>")

h = HTML()
with h.tag("ul", class_="menu"):
    for item in ("Home", "About"):
        with h.tag("li"):
            h.text(item)
print("\n".join(h.lines))
# <ul class="menu">
#   <li>
#     Home
#   </li>
#   <li>
#     About
#   </li>
# </ul>

# 3. Method chaining that reads like a sentence
class Expect:
    def __init__(self, value):
        self.value = value

    @property
    def to(self):                               # filler words, for readability
        return self

    @property
    def be(self):
        return self

    def greater_than(self, n):
        assert self.value > n, f"expected {self.value} to be greater than {n}"
        return self

def expect(value):
    return Expect(value)

print(expect(5).to.be.greater_than(3).value)    # 5
try:
    expect(2).to.be.greater_than(3)
except AssertionError as e:
    print(e)                                    # expected 2 to be greater than 3

# 4. A state machine described by a fluent API
class Machine:
    def __init__(self, initial):
        self.state, self.transitions = initial, {}

    def on(self, event, source, target):
        self.transitions[(source, event)] = target
        return self                             # returning self allows chaining

    def fire(self, event):
        try:
            self.state = self.transitions[(self.state, event)]
        except KeyError:
            raise ValueError(f"cannot {event!r} in state {self.state!r}") from None
        return self.state

m = (Machine("idle")
     .on("start", "idle", "running")
     .on("pause", "running", "paused")
     .on("resume", "paused", "running"))
print([m.fire(e) for e in ("start", "pause", "resume")])        # ['running', 'paused', 'running']
try:
    Machine("idle").fire("stop")
except ValueError as e:
    print(e)                                    # cannot 'stop' in state 'idle'

# 5. The | operator as a pipe
class Pipe:
    def __init__(self, func):
        self.func = func

    def __or__(self, other):                    # Pipe | Pipe  makes a new pipe
        return Pipe(lambda x: other.func(self.func(x)))

    def __ror__(self, value):                   # value | Pipe  runs it
        return self.func(value)

double = Pipe(lambda x: x * 2)
inc = Pipe(lambda x: x + 1)
print(5 | double | inc, 5 | (double | inc))     # 11 11

# ---------- EXTERNAL DSL: a tiny expression language with variables ----------
TOKEN = re.compile(r"\s*(?:(\d+\.?\d*)|([A-Za-z_]\w*)|(.))")

def tokenize(text):
    tokens = []
    for match in TOKEN.finditer(text):
        number, name, symbol = match.groups()
        if number:
            tokens.append(("num", float(number)))
        elif name:
            tokens.append(("name", name))
        else:
            tokens.append(("op", symbol))
    return tokens

class Parser:                                   # recursive descent: one method per grammar rule
    def __init__(self, tokens, variables):
        self.tokens, self.pos, self.variables = tokens, 0, variables

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else (None, None)

    def take(self):
        token = self.peek()
        self.pos += 1
        return token

    def expression(self):                       # term (("+" | "-") term)*
        value = self.term()
        while self.peek() in (("op", "+"), ("op", "-")):
            op = self.take()[1]
            right = self.term()
            value = value + right if op == "+" else value - right
        return value

    def term(self):                             # factor (("*" | "/") factor)*
        value = self.factor()
        while self.peek() in (("op", "*"), ("op", "/")):
            op = self.take()[1]
            right = self.factor()
            value = value * right if op == "*" else value / right
        return value

    def factor(self):                           # number | name | "(" expression ")" | "-" factor
        kind, value = self.take()
        if kind == "num":
            return value
        if kind == "name":
            if value not in self.variables:
                raise NameError(f"unknown variable {value!r}")
            return self.variables[value]
        if (kind, value) == ("op", "("):
            result = self.expression()
            self.take()                         # the closing bracket
            return result
        if (kind, value) == ("op", "-"):
            return -self.factor()
        raise SyntaxError(f"unexpected {value}")

def evaluate(text, **variables):
    parser = Parser(tokenize(text), variables)
    result = parser.expression()
    if parser.pos != len(parser.tokens):
        raise SyntaxError("trailing input")
    return result

print(evaluate("2 + 3 * (x - 1)", x=5))         # 14.0
print(evaluate("-(1 + 2) * 4"), evaluate("10 / 4 / 5"))        # -12.0 0.5
for bad in ("2 +", "y + 1"):
    try:
        evaluate(bad)
    except (SyntaxError, NameError) as e:
        print(type(e).__name__, e)
# SyntaxError unexpected None
# NameError unknown variable 'y'

# DESIGN NOTES
#  - Start with an INTERNAL DSL (builders, chains, "with"): no parser to write, full Python available.
#  - An EXTERNAL DSL pays off when non-programmers write it, or it must be stored in a file.
#  - Never "eval" the text of a DSL: write a parser (or use ast.literal_eval for plain data).
#  - Give clear error messages (position, expected token): that is most of the work.
#  - Parser tools: pyparsing, lark, textX, PLY; Python's own "ast" module to parse Python expressions safely.
#  - DSLs you already know: SQL, regular expressions, format strings, Jinja templates, Makefiles, TOML/YAML.