# A try block can sit inside another try block, or inside an except or finally block.

# 1. The inner handler does not match, so the exception goes to the outer one
try:
    try:
        {}["a"]
    except ValueError:
        print("inner")
except KeyError:
    print("outer caught KeyError")              # outer caught KeyError

# 2. Different handling at different levels
def process(items):
    results = []
    for item in items:
        try:
            try:
                value = int(item)
            except ValueError:
                print(f"skip bad value {item!r}")
                continue
            results.append(10 // value)
        except ZeroDivisionError:
            print("zero found")
            results.append(None)
    return results

print(process(["5", "x", "0", "2"]))
# skip bad value 'x'
# zero found
# [2, None, 5]

# 3. An error INSIDE an except block
try:
    try:
        1 / 0
    except ZeroDivisionError:
        int("x")                                # a new error while handling the first
except ValueError:
    print("error while handling")               # error while handling

# 4. A try inside finally: cleanup that may fail must not hide the real result
def cleanup_demo():
    try:
        print("work")
    finally:
        try:
            raise OSError("cleanup failed")
        except OSError as e:
            print("cleanup error ignored:", e)

cleanup_demo()
# work
# cleanup error ignored: cleanup failed

# 5. The stack unwinds: every finally runs on the way up
def level3():
    try:
        raise RuntimeError("boom")
    finally:
        print("leaving level3")

def level2():
    try:
        level3()
    finally:
        print("leaving level2")

def level1():
    try:
        level2()
    finally:
        print("leaving level1")

try:
    level1()
except RuntimeError as e:
    print("caught:", e)
# leaving level3
# leaving level2
# leaving level1
# caught: boom

# 6. A fallback chain
def primary():
    raise OSError("primary sensor offline")

def backup():
    return 21.5

def read_sensor():
    try:
        return primary()
    except OSError:
        try:
            return backup()
        except OSError:
            return None

print(read_sensor())                            # 21.5

# 7. Too much nesting is hard to read: move the inner part into a small function
def parse_int(text):
    try:
        return int(text)
    except ValueError:
        return None

print([parse_int(t) for t in ["1", "x", "3"]])  # [1, None, 3]