exercises.py

Write the questions as # comments and your solutions as code below each one.

Read a number and print whether it is positive, negative or zero.
Read three numbers and print the largest, using if / elif only (no max()).
Read a year and print whether it is a leap year (divisible by 4, except centuries, unless divisible by 400). Test with 1900, 2000, 2024 and 2023.
Read a mark from 0 to 100 and print the grade (A 90+, B 75+, C 60+, F below). Reject values outside 0 to 100.
Rewrite exercise 4 as a ternary for a pass/fail message (pass at 40 or above).
Build a calculator that reads two numbers and an operator, and handles division by zero and unknown operators.
Use match-case to print the day name for numbers 1 to 7, with _ for anything else. Add an OR pattern that prints “Weekend” for 6 and 7.
Use match-case on a tuple (x, y) to print which quadrant the point is in, or whether it is on an axis or the origin.
Print the multiples of 7 from 7 to 70, then the same list in reverse using range with a negative step.
Compute the sum of the numbers from 1 to 100, and the sum of only the even ones, with a for loop.
Print the factorial of a number using a for loop, then again with a while loop. Test with 0, 5 and 10.
Count the vowels in a string using a for loop.
FizzBuzz for 1 to 30: print Fizz for multiples of 3, Buzz for multiples of 5, FizzBuzz for both, otherwise the number.
Read numbers until the user types done, then print the count, sum and average. Use while True and break, and use continue to skip invalid input.
Print all prime numbers between 2 and 50 using for ... else.
Reverse the digits of an integer with a while loop (for example 1234 becomes 4321).
Number guessing game: pick a fixed secret number, give the user 5 attempts, print “too high” or “too low” each time, and use while ... else or for ... else to print a message if all attempts fail.
Print this pattern with nested loops (a right triangle of numbers), then a pyramid of height 5:
1
1 2
1 2 3
1 2 3 4
For matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]], print the sum of each row, the sum of each column and the sum of the anti-diagonal.
Predict first, then run: what do these print, and why?
python
for i in range(3):
    for j in range(3):
        if j == 1:
            continue
        if i == 2:
            break
        print(i, j)