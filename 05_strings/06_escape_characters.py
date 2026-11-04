# An escape sequence starts with a backslash and stands for a special character.
#
#  \n     newline                \\     backslash
#  \t     tab                    \'     single quote
#  \r     carriage return        \"     double quote
#  \b     backspace              \xhh   character with hex code hh
#  \f     form feed              \ooo   character with octal code ooo
#  \v     vertical tab           \uXXXX      Unicode, 4 hex digits
#  \a     bell (alert)           \UXXXXXXXX  Unicode, 8 hex digits
#  \0     null character         \N{name}    Unicode by name
#  \      (at the end of a line) joins the next line

print("Line1\nLine2")
# Line1
# Line2

print("A\tB\tC")                       # A	B	C   (tabs)
print("He said \"hi\"")                # He said "hi"
print('It\'s')                         # It's
print("C:\\Users\\sam")                # C:\Users\sam

# Escapes are single characters
print(len("a\nb"), len("\\"))          # 3 1
print(repr("a\tb\n"))                  # 'a\tb\n'

# Hex, octal and Unicode escapes
print("\x41", "\101", "\u00e9", "\U0001F600", "\N{SNOWMAN}")   # A A é 😀 ☃

# RAW strings: backslashes are kept as they are
print(r"C:\new\table")                 # C:\new\table
print(len(r"\n"), len("\n"))           # 2 1
print(r"C:\path" + "\\")               # C:\path\
# A raw string cannot end in a single backslash: r"abc\" is a SyntaxError
# Raw strings are the normal way to write regex patterns: r"\d+" (Module 17)

# Line continuation inside a string
text = "abc\
def"
print(text)                            # abcdef

# Triple quotes need no escaping for quotes
print("""She said "hi" and 'bye'""")   # She said "hi" and 'bye'

# Printing a literal backslash-n
print("a\\nb")                         # a\nb

# "\d" or any unknown escape gives a warning in newer Python; use a raw string instead.
# \r moves the cursor to the start of the line on a terminal (output looks overwritten).
# For file paths, prefer pathlib or forward slashes (Module 11).