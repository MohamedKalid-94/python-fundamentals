# 1. Age check
age = int(input("Enter your age: "))          # sample: 20
if age >= 18:
    print("You can vote")                     # You can vote
else:
    print("You cannot vote yet")

# 2. Validate before converting (int("abc") would crash)
text = input("Enter a whole number: ")        # sample: 42
if text.isdigit():
    number = int(text)
    print("even" if number % 2 == 0 else "odd")   # even
else:
    print("That is not a valid whole number")
# Note: isdigit() rejects "-5" and "3.5". Full error handling comes in Module 14.

# 3. Case-insensitive yes/no
answer = input("Continue? (y/n): ").strip().lower()    # sample:  YES
if answer in ("y", "yes"):
    print("Continuing")                       # Continuing
elif answer in ("n", "no"):
    print("Stopping")
else:
    print("Please answer y or n")

# 4. Menu
print("1) Add  2) Subtract  3) Quit")
choice = input("Choose: ").strip()            # sample: 2
if choice == "1":
    print("Adding")
elif choice == "2":
    print("Subtracting")                      # Subtracting
elif choice == "3":
    print("Bye")
else:
    print("Invalid choice")

# 5. Grade with range validation
marks = float(input("Enter marks (0-100): ")) # sample: 82.5
if not 0 <= marks <= 100:
    print("Marks must be between 0 and 100")
elif marks >= 75:
    print("Grade B or above")                 # Grade B or above
else:
    print("Below grade B")

# 6. Calculator
a = float(input("First number: "))            # sample: 8
op = input("Operator (+ - * /): ").strip()    # sample: /
b = float(input("Second number: "))           # sample: 2

if op == "+":
    print(a + b)
elif op == "-":
    print(a - b)
elif op == "*":
    print(a * b)
elif op == "/":
    if b == 0:
        print("Cannot divide by zero")
    else:
        print(a / b)                          # 4.0
else:
    print("Unknown operator")