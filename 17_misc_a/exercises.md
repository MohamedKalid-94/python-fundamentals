Write the questions as # comments and your solutions as code below each one. Use fixed dates and fixed seeds so your outputs stay the same.

Date & Time

Print the weekday name of 2026-02-14, the day of the year of 2026-12-31, and whether 2100 is a leap year. Then find the next Friday the 13th after 2026-11-10.
Write age_in_days(born, on) and next_birthday(born, today) that returns the date of the next birthday (handle 29 February).
Parse the text "10 Nov 2026, 02:30 PM" into a datetime, add 90 minutes, and print it in ISO format. Then convert it from UTC+5:30 to UTC and to UTC-8.
Write format_duration(seconds) that turns 3725 into "1h 02m 05s" and handles days (90061 becomes "1d 1h 01m 01s").
Write a function that takes a list of ISO timestamps from a sensor log (not sorted, some with a different time zone offset), converts them to UTC, sorts them, and prints the time between each pair of neighbours.

Maths

Write quadratic(a, b, c) that returns both roots with cmath (so a negative discriminant works) and test it on three equations.
Compute the mean, median, mode, sample standard deviation and the z-score of every value for [12, 15, 11, 18, 15, 20, 13].
Show that 0.1 + 0.2 != 0.3, then add 0.1 ten times with sum, with math.fsum and with Decimal, and print the three results.
Convert a 12-bit ADC value to volts, to a temperature (10 mV per degree), and to a Q8.8 fixed-point integer. Write from_q8_8(x) and check that the round trip stays within 1/256.
With random.seed(7), simulate 1000 rolls of two dice and print how many times each sum appeared (use a dictionary). Check that the total is 1000.

Iterators, generators, expressions

Write a class Fibonacci(limit) that is an iterator, then rewrite it as a generator function and as a generator expression where possible. Compare the code length.
Write a generator read_lines(text) that yields the lines of a multi-line string without the blank ones, and a generator pipeline that keeps only the lines starting with ERROR, strips them, and counts them.
Write batched(iterable, n) that yields lists of n items (the last one may be shorter) using itertools.islice, and test it on range(10).
Write running_max(values) as a generator, and sliding_window(values, size) as a generator that yields tuples. Use collections.deque.
Write a coroutine-style generator accumulator() that receives numbers with send() and yields the running total, and one that receives strings and yields the number of words seen so far.
Use itertools to: list all 2-letter passwords made from "abc" with repeats, all ways to choose 2 of 5 sensors, the cumulative sum of [5, 3, 8], and the first 5 multiples of 7.
Show with sys.getsizeof and a timer that sum(x * x for x in range(10**6)) uses far less memory than sum([x * x for x in range(10**6)]), and say which is faster.

Lambda, closures, decorators

Sort a list of dictionaries (name, age, city) by city, then by age descending, using key=lambda and again with operator.itemgetter.
Write make_counter(step=1) and make_accumulator(start=0) as closures, and make_rate_limiter(max_calls) that returns True for the first max_calls calls and False after.
Write decorators @timed (stores the last duration), @debug (records the arguments and the result in a list), @retry(times), @validate_types(int, int) and @memoize. Apply two of them to one function and explain the order.
Write a @deprecated("use new_func") decorator that raises a DeprecationWarning (with stacklevel=2), and capture the warning with warnings.catch_warnings.
Write a class Counter decorator @count_calls as a class with __call__, and a version as a function with an attribute. Which one works better with methods, and why?

Recursion

Write recursive functions for: the sum of a nested list, the number of digits of an integer, n choose k (Pascal’s triangle rule), the greatest common divisor, converting a decimal number to a binary string, and checking that brackets are balanced.
Solve the “climbing stairs” problem (1 or 2 steps at a time, how many ways for n steps) with plain recursion, with lru_cache, and with a loop. Time all three for n = 30.
Write a recursive permutations(items) and combinations(items, k) and check them against itertools. Write a function that lists all subsets of a list whose sum is exactly target.
Write walk(tree, depth=0) that prints a nested dictionary as an indented tree, and find(tree, name) that returns the path to a key (as a list), or None.
Show the recursion limit being hit with a naive sum_to(n) recursion, then fix it with a loop and with the formula n * (n + 1) // 2.

Regular expressions

Write patterns that find: all integers (with an optional minus) and decimals in a text, all words that start with a capital letter, all hex colours like 
#1a2B3c, and all dates in dd/mm/yyyy format. Test each on a text of your own.
Write parse_log(line) with a named-group regex for lines like [2026-11-10 14:30:15] <uart> ERROR: timeout after 100 ms and return a dictionary with the timestamp, the module, the level, the message and the number of milliseconds (as an integer, or None).
Write mask_card(text) that replaces all but the last 4 digits of any 16-digit number (with optional spaces or dashes) by *, and slugify(title) that turns "Hello, World! 2026" into "hello-world-2026".
Write a function that checks a password against these rules with regexes: at least 8 characters, one lowercase, one uppercase, one digit, one symbol. Return the list of rules that fail.
Parse the text "TEMP=36.5;HUM=40;STATE=OK;ERR=-3" into a dictionary with the right types (floats, integers, strings) using one regex with finditer.
Predict first, then run, and explain each result in a comment:
python
import re
from itertools import islice, count, accumulate

print(re.findall(r"(a)(b)?", "ab a"))
print(re.sub(r"(?P<x>\d)(?P=x)", "<>", "112233 45"))
print(re.split(r"\s*,\s*", " a , b,c "))

fs = [lambda x, n=n: x * n for n in range(3)]
print([f(10) for f in fs])

def gen():
    received = yield 1
    print("got", received)
    yield 2

g = gen()
print(next(g), g.send("hello"))

print(list(islice(accumulate(count(1)), 5)))

def f(n, memo=[]):
    memo.append(n)
    return len(memo) if n == 0 else f(n - 1)

print(f(3), f(2))