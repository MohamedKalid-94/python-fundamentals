# An if inside another if
age = 25
has_id = True

if age >= 18:
    if has_id:
        print("entry allowed")      # entry allowed
    else:
        print("show your ID")
else:
    print("too young")

# Login check
username = "admin"
password = "1234"

if username == "admin":
    if password == "1234":
        print("welcome")            # welcome
    else:
        print("wrong password")
else:
    print("unknown user")

# Classify a number
n = 15
if n > 0:
    if n % 2 == 0:
        print("positive even")
    else:
        print("positive odd")       # positive odd
elif n < 0:
    print("negative")
else:
    print("zero")

# FLATTEN with "and" when there is no separate else for the inner check
if age >= 18 and has_id:
    print("entry allowed (flat version)")   # entry allowed (flat version)

if n > 0 and n % 2 == 0:
    print("positive even")
elif n > 0:
    print("positive odd (flat version)")    # positive odd (flat version)

# Rule of thumb: more than 3 levels of nesting is hard to read.
# Combine conditions, or use early exits (covered with functions in Module 04).