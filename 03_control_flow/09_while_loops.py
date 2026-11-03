# Basic counting loop
count = 1
while count <= 3:
    print(count)
    count += 1                  # forget this line and the loop never ends!
# 1
# 2
# 3

# Countdown
n = 5
while n > 0:
    print(n, end=" ")
    n -= 1
print("liftoff")                # 5 4 3 2 1 liftoff

# Sum the digits of a number
number = 1234
total = 0
while number > 0:
    total += number % 10        # last digit
    number //= 10               # drop the last digit
print(total)                    # 10

# Repeat until a condition is met (unknown number of steps)
x = 1.0
steps = 0
while x > 0.001:
    x /= 2
    steps += 1
print(steps, x)                 # 10 0.0009765625

# "while True" + break: loop forever until told to stop
while True:
    answer = input("Type 'quit' to stop: ").strip().lower()
    if answer == "quit":
        break
    print("you typed", answer)
# sample run:
# Type 'quit' to stop: hello
# you typed hello
# Type 'quit' to stop: QUIT

# Input validation loop
while True:
    password = input("Choose a password (min 6 chars): ")
    if len(password) >= 6:
        print("Password accepted")
        break
    print("Too short, try again")
# sample run:
# Choose a password (min 6 chars): abc
# Too short, try again
# Choose a password (min 6 chars): secret99
# Password accepted

# while ... else: else runs when the condition becomes false (no break)
attempts = 0
while attempts < 3:
    attempts += 1
else:
    print("loop ended normally after", attempts, "attempts")
# loop ended normally after 3 attempts

# Python has no do-while. Emulate it:
#   while True:
#       ...body that runs at least once...
#       if not condition:
#           break

# WHEN TO USE WHICH
# for   -> you have a collection or a known count
# while -> you repeat until something happens