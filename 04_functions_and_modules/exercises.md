Write the questions as # comments and your solutions as code below each one.

Write is_even(n) that returns True or False. Test it with 0, 7 and -4.
Write stats(numbers) that returns the minimum, maximum and average as a tuple. Unpack the result into three variables.
Write greet(name, greeting="Hello") and call it three ways: positionally, with the default, and with keywords in reversed order.
Reproduce the mutable default trap with add_item, then fix it with None. Print the results of 3 calls for each version.
Write format_price(amount, *, currency="INR", decimals=2) that returns a string like INR 1234.50. Show that format_price(1234.5, "USD") raises a TypeError.
Write clamp(value, low, high, /) (positional-only) that limits a value to a range. Show what happens with keyword arguments.
Write mean(*numbers) that returns the average of any number of arguments, and handle the empty call by returning None.
Write build_profile(name, **details) that returns a dictionary containing the name and all the extra details.
Call add3(a, b, c) using * with a list and ** with a dictionary.
Predict first, then run, and explain each line in a comment:
python
x = 5
def f():
    print(x)
def g():
    x = 10
    print(x)
def h():
    global x
    x = 20
f(); g(); print(x); h(); print(x)
Write make_counter() that returns an inner function using nonlocal, so each call to the inner function returns 1, 2, 3, and so on.
Show that a function can change a list passed to it, but cannot change an integer passed to it. Explain why in a comment.
Write average(values: list[float]) -> float with annotations, and print its __annotations__.
Create temperature.py with c_to_f(c) and f_to_c(f) (sensor-style conversions). Add an if __name__ == "__main__": block with a few test prints. Then create main.py that imports it in three different ways and prints the conversion for 0, 37 and 100 degrees Celsius.
Use star unpacking to get the first, last and middle values of [10, 20, 30, 40, 50], then merge two dictionaries where the second overrides the first.
Predict first, then run:
python
def f(x, items=[]):
    items.append(x)
    return items
print(f(1), f(2))
Rewrite a for loop that sums the even numbers of a list as one line using sum(), then find the longest word of a list using max(..., key=len).
Show what happens when you name a variable max or list and then call the built-in. Fix it with del, and write a comment on how to avoid it.