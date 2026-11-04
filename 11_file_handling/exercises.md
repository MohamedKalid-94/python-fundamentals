Write the questions as # comments and your solutions as code below each one. Clean up every file you create.

Write 5 lines of text to a file with write, then read them back with read, readline, readlines and a for loop. Print the result of each.
Append 2 more lines, then print the file with line numbers. Show what happens to the old content when you open the same file with "w".
Write a program that asks for a name and a score (with input()) and appends them to scores.txt. Run it 3 times and print the whole file.
Show the difference between "r+", "w+" and "a+" by writing and reading the same small file in all three modes.
Write count_stats(path) that returns the number of lines, non-empty lines, words and characters of a text file.
Write top_words(path, n) that returns the n most frequent words of a file, ignoring case and punctuation.
Write copy_file(src, dst, chunk=1024) that copies a binary file in chunks and verifies the copy by comparing the sizes and the content.
Write tail(path, n) that returns the last n lines of a file without reading the whole file into memory (hint: collections.deque with maxlen).
Write replace_in_file(path, old, new) that edits a file safely: write to a temporary file, then os.replace.
Create the structure project/src, project/tests and project/docs with makedirs, put 2 files in each folder, then list the whole tree with os.walk and print the total number of files and bytes.
Write find_files(folder, extension) that returns every file with that extension, in all subfolders, using os.walk, and again with Path.rglob.
Write organize(folder) that moves the files of a folder into subfolders named after their extensions (.txt goes to txt/).
Rename 5 files to add a numbered prefix (01_, 02_, ...) in one loop, then undo the rename.
Write safe_delete(path) that deletes a file or a whole folder, and prints a message instead of crashing when the path does not exist.
Read a CSV file with the csv module, compute the average of one column, and write a new CSV that contains only the rows above the average.
Save a nested dictionary as JSON with indent=2, load it back, check that the two are equal, and show what happens when you load a file that contains invalid JSON (catch json.JSONDecodeError).
Write a binary file that holds 100 16-bit samples with array("H"), read it back, reverse the byte order with byteswap(), and compare the first 3 values before and after.
Write a log file with 6 messages (INFO, WARNING, ERROR). Then write filter_log(path, level) that prints only the lines of one level, and a function that counts how many messages each level has.
Use seek and tell on a binary file of 20 bytes to read the last 5 bytes, the bytes 5 to 9, and then rewrite the byte at position 10 (open the file in "r+b").
Use StringIO to test a function that writes a report to any file object (def report(data, out): print(..., file=out)), once with a real file and once with StringIO.
Print the name, extension, parent, absolute path, size and modification time of a file, once with os.path and once with pathlib.
Predict first, then run, and explain each result in a comment:
python
import os
with open("t1.txt", "w", encoding="utf-8") as f:
    print(f.write("ab\ncd"), f.tell())

with open("t1.txt", "a", encoding="utf-8") as f:
    f.write("ef")

with open("t1.txt", encoding="utf-8") as f:
    print(f.readline(), f.read(1), repr(f.read()), repr(f.read()))

with open("t1.txt", "r+", encoding="utf-8") as f:
    f.write("X")
    f.seek(0)
    print(f.read())

print(os.path.splitext("a.b.c"), os.path.join("a", "b", "/c", "d").replace(os.sep, "/"))
os.remove("t1.txt")
print(os.path.exists("t1.txt"))