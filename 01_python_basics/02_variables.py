age = 30
name = "Sam"
print(age, name)                      # 30 Sam

# Multiple assignment
x = y = z = 0
a, b, c = 1, 2.5, "hi"
print(x, y, z)                        # 0 0 0
print(a, b, c)                        # 1 2.5 hi

# Swap without a temp variable
a, b = b, a
print(a, b)                           # 2.5 1

# A variable is a NAME pointing to an OBJECT (not a memory box like in C)
n = 10
m = n
print(n is m)                         # True  (same object)
n = 20                                # n now points to a NEW object
print(n, m)                           # 20 10
print(id(n) != id(m))                 # True  (id() = object identity)

# Dynamic typing: the name has no type, the object does
v = 5
print(type(v))                        # <class 'int'>
v = "five"
print(type(v))                        # <class 'str'>

# Naming rules
# valid  : user_name, _temp, value2, Total
# invalid: 2value (starts with digit), my-var (hyphen), class (keyword)
# Names are case-sensitive: age and Age are different

# Constants are only a convention (UPPER_CASE); Python will not stop you
MAX_RETRIES = 3

# Deleting a name
del z
# print(z)                            # NameError: name 'z' is not defined