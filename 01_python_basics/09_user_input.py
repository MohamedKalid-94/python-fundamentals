name = input("Enter your name: ")           # ALWAYS returns a str
age = int(input("Enter your age: "))        # cast it yourself
print("Hello,", name)
print(f"Next year you will be {age + 1}")

# Two numbers on one line
a, b = map(int, input("Two numbers: ").split())
print(a + b)

# print() options
print("a", "b", "c", sep="-", end="!\n")    # a-b-c!
print(f"{3.14159:.2f}")                     # 3.14