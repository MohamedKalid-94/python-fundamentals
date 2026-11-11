import html
import re
import textwrap
from string import Template

# A TEMPLATE is text with holes that you fill with values.

# 1. string.Template ($name or ${name})
t = Template("Hello $name, you are ${age}yo")
print(t.substitute(name="Ann", age=30))         # Hello Ann, you are 30yo
try:
    t.substitute(name="Ann")                    # a value is missing
except KeyError:
    print("KeyError")                           # KeyError
print(Template("Hello $name, $other").safe_substitute(name="Ann"))      # Hello Ann, $other
print(t.get_identifiers(), t.is_valid())        # ['name', 'age'] True        (Python 3.11+)
print(Template("Price: $$5").substitute())      # Price: $5          $$ is a literal dollar sign

class PercentTemplate(Template):                # change the delimiter
    delimiter = "%"

print(PercentTemplate("Hi %name").substitute(name="Ann"))   # Hi Ann

# 2. format_map with a dictionary that tolerates missing keys
class SafeDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"

print("{a} and {b}".format_map({"a": 1, "b": 2}))           # 1 and 2
print("{a} {z}".format_map(SafeDict(a=1)))                  # 1 {z}

# 3. HTML: ALWAYS escape values that come from users
print(html.escape('<a href="x">T&C</a>'))       # &lt;a href=&quot;x&quot;&gt;T&amp;C&lt;/a&gt;
print(html.unescape("&lt;b&gt;") == "<b>")      # True

row = Template("<tr><td>$name</td><td>$note</td></tr>")
rows = [("Ann", "<b>"), ("Bob", "5 > 3")]
print("\n".join(row.substitute(name=html.escape(n), note=html.escape(v)) for n, v in rows))
# <tr><td>Ann</td><td>&lt;b&gt;</td></tr>
# <tr><td>Bob</td><td>5 &gt; 3</td></tr>

# 4. A tiny template engine with a regular expression: {{ name }}
def render(template, context):
    return re.sub(r"\{\{\s*(\w+)\s*\}\}", lambda m: str(context.get(m.group(1), "")), template)

print(render("Hi {{ name }}!", {"name": "Ann"}))            # Hi Ann!

# 5. Code generation (embedded style): a C header from a dictionary
pins = {"LED": 13, "BTN": 2}
header = "".join(Template("#define PIN_$name $number\n").substitute(name=k, number=v)
                 for k, v in pins.items())
print(header, end="")
# #define PIN_LED 13
# #define PIN_BTN 2

# 6. textwrap: shape plain text
text = "The quick brown fox jumps over the lazy dog"
print(textwrap.wrap(text, width=20))            # ['The quick brown fox', 'jumps over the lazy', 'dog']
print(textwrap.fill(text, width=20))
# The quick brown fox
# jumps over the lazy
# dog
print(repr(textwrap.dedent("   a\n   b")))      # 'a\nb'
print(textwrap.indent("a\nb", "> "))
# > a
# > b
print(textwrap.shorten("Hello wonderful world", width=15))      # Hello [...]

# FOR REAL WEB PAGES AND E-MAILS use Jinja2 (pip install jinja2):
#   from jinja2 import Environment
#   env = Environment(autoescape=True)
#   env.from_string("Hello {{ name }}! {% for x in items %}{{ x }} {% endfor %}").render(name="Ann", items=[1, 2])
# Jinja2 gives you loops, conditions, inheritance and automatic escaping.