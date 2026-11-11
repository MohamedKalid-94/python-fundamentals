import io
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.dom import minidom

XML = """<library>
  <book id="1"><title>Python</title><price>30.5</price></book>
  <book id="2"><title>C</title><price>25</price></book>
</library>"""

# 1. Read: an XML document is a TREE of elements (tag, attributes, text, children)
root = ET.fromstring(XML)
print(root.tag, len(root), root[0].attrib)      # library 2 {'id': '1'}
print([b.get("id") for b in root.findall("book")])          # ['1', '2']
print(root.find("book/title").text)             # Python
print(root.find("book[@id='2']/title").text)    # C           a simple XPath: attribute test
print([t.text for t in root.iter("title")])     # ['Python', 'C']      iter() searches ALL levels
print(sum(float(p.text) for p in root.iter("price")))       # 55.5
print({b.get("id"): b.find("title").text for b in root})    # {'1': 'Python', '2': 'C'}

# 2. Change
root.find("book/price").text = "35"
root.find("book").set("lang", "en")
root.remove(root.findall("book")[1])
print(root.find("book").attrib, root.find("book/price").text, len(root))
# {'id': '1', 'lang': 'en'} 35 1

# 3. Build and write
cfg = ET.Element("config")
ET.SubElement(cfg, "port").text = "8080"
ET.SubElement(cfg, "device", name="uart0")
cfg.find("device").set("baud", "9600")
ET.indent(cfg)                                  # pretty printing (Python 3.9+)
print(ET.tostring(cfg, encoding="unicode"))
# <config>
#   <port>8080</port>
#   <device name="uart0" baud="9600" />
# </config>

with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp) / "config.xml"
    ET.ElementTree(cfg).write(path, encoding="utf-8", xml_declaration=True)
    print(ET.parse(path).getroot().find("port").text)       # 8080

# 4. Special characters are escaped for you
x = ET.Element("x")
x.text = 'a < b & "c"'
print(ET.tostring(x, encoding="unicode"))       # <x>a &lt; b &amp; "c"</x>

# 5. Text that follows a child element is its "tail"
p = ET.fromstring("<p>Hello <b>bold</b> world</p>")
print(repr(p.text), p[0].text, repr(p[0].tail))             # 'Hello ' bold ' world'

# 6. Namespaces
ns_doc = ET.fromstring('<a:root xmlns:a="http://x"><a:item>1</a:item></a:root>')
print(ns_doc.tag)                               # {http://x}root
print(ns_doc.find("a:item", {"a": "http://x"}).text)        # 1

# 7. Errors
try:
    ET.fromstring("<a><b></a>")
except ET.ParseError:
    print("ParseError")                         # ParseError

# 8. Huge files: iterparse reads one element at a time
titles = []
for event, element in ET.iterparse(io.StringIO(XML)):       # by default you get "end" events
    if element.tag == "title":
        titles.append(element.text)
    element.clear()                             # free the memory of elements you are done with
print(titles)                                   # ['Python', 'C']

# 9. minidom: another API, with pretty printing
print(minidom.parseString("<a><b>1</b></a>").toprettyxml(indent="  ").strip())
# <?xml version="1.0" ?>
# <a>
#   <b>1</b>
# </a>

# XML vs JSON
#   XML   attributes, namespaces, schemas, mixed text (documents, SVG, Office files, SOAP, many device configs)
#   JSON  simpler, smaller, the default for web APIs
# SECURITY  ElementTree is NOT safe against malicious XML (entity expansion, "billion laughs").
#           For XML from outside use the third-party package "defusedxml".
