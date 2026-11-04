# 1. Reverse a string
print("hello"[::-1])                           # olleh

# 2. Palindrome (ignore case, spaces and punctuation)
def is_palindrome(text):
    cleaned = ""
    for ch in text:
        if ch.isalnum():
            cleaned += ch.lower()
    return cleaned == cleaned[::-1]

print(is_palindrome("A man, a plan, a canal: Panama"), is_palindrome("hello"))
# True False

# 3. Count vowels
def count_vowels(text):
    count = 0
    for ch in text.lower():
        if ch in "aeiou":
            count += 1
    return count

print(count_vowels("Hello World"))             # 3

# 4. Character frequency (dictionaries are covered in Module 09)
def char_frequency(text):
    freq = {}
    for ch in text:
        freq[ch] = freq.get(ch, 0) + 1
    return freq

print(char_frequency("banana"))                # {'b': 1, 'a': 3, 'n': 2}

# 5. Word count and longest word
sentence = "the quick brown fox jumps"
words = sentence.split()
print(len(words), max(words, key=len))         # 5 quick

# 6. Capitalize every word
result = []
for w in words:
    result.append(w.capitalize())
print(" ".join(result))                        # The Quick Brown Fox Jumps

# 7. Anagram check
print(sorted("listen") == sorted("silent"))    # True

# 8. Remove duplicate characters, keeping the order
unique = ""
for ch in "banana":
    if ch not in unique:
        unique += ch
print(unique)                                  # ban

# 9. Caesar cipher
def caesar(text, shift):
    result = ""
    for ch in text:
        if ch.islower():
            result += chr((ord(ch) - ord("a") + shift) % 26 + ord("a"))
        elif ch.isupper():
            result += chr((ord(ch) - ord("A") + shift) % 26 + ord("A"))
        else:
            result += ch
    return result

print(caesar("Hello, World!", 3))              # Khoor, Zruog!
print(caesar("Khoor, Zruog!", -3))             # Hello, World!

# 10. Is the text an integer? (allow a leading + or -)
def is_int(text):
    text = text.strip()
    if text[:1] in "+-":
        text = text[1:]
    return text.isdigit()

print(is_int("42"), is_int("-17"), is_int("+5"), is_int("3.5"), is_int(""), is_int("abc"))
# True True True False False False

# 11. Mask all but the last 4 characters
number = "4111111111111111"
print("*" * (len(number) - 4) + number[-4:])   # ************1111

# 12. URL-style slug
print("Hello World From Python".lower().replace(" ", "-"))   # hello-world-from-python

# 13. Run-length encoding
def compress(text):
    if not text:
        return ""
    result = ""
    count = 1
    for i in range(1, len(text)):
        if text[i] == text[i - 1]:
            count += 1
        else:
            result += text[i - 1] + str(count)
            count = 1
    result += text[-1] + str(count)
    return result

print(compress("aaabbc"))                      # a3b2c1

# 14. Parse a serial-style line (embedded-flavoured)
line = "TEMP=36.5;HUM=40;STATE=OK"
fields = {}
for pair in line.split(";"):
    key, value = pair.split("=")
    fields[key] = value
print(fields)                                  # {'TEMP': '36.5', 'HUM': '40', 'STATE': 'OK'}
print(float(fields["TEMP"]) + 1)               # 37.5

# 15. Hex dump of bytes
parts = []
for byte in b"Hi!":                            # iterating bytes gives integers
    parts.append(f"{byte:02x}")
print(" ".join(parts))                         # 48 69 21