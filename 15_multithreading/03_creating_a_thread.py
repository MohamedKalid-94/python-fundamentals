import threading
from concurrent.futures import ThreadPoolExecutor

# Thread(group=None, target=None, name=None, args=(), kwargs=None, daemon=None)

results = []

# 1. A function as the target, with positional and keyword arguments
def greet(name, times=1):
    results.append(f"hello {name} x{times}")

t = threading.Thread(target=greet, args=("Ann",), kwargs={"times": 2})
t.start()
t.join()
print(results)                                  # ['hello Ann x2']

# COMMON BUG: args must be a TUPLE. A single argument needs a trailing comma:
#   args=("Ann")    is just the string "Ann", which Python unpacks into 'A', 'n', 'n'
#   args=("Ann",)   is the tuple you want

# 2. A subclass of Thread that overrides run()
class Worker(threading.Thread):
    def __init__(self, n):
        super().__init__()
        self.n = n
        self.result = None

    def run(self):
        self.result = sum(range(self.n))

w = Worker(5)
w.start()
w.join()
print(w.result)                                 # 10      a thread keeps its result as an attribute

# 3. A callable object
class Task:
    def __call__(self):
        results.append("task ran")

results.clear()
t = threading.Thread(target=Task())
t.start()
t.join()
print(results)                                  # ['task ran']

# 4. Several threads from a loop (any bound method works as a target)
results.clear()
threads = [threading.Thread(target=results.append, args=(i * i,)) for i in range(3)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(sorted(results))                          # [0, 1, 4]       the ORDER may differ, so sort

# 5. Timer: run a function after a delay (it can be cancelled)
results.clear()
timer = threading.Timer(0.1, results.append, args=("timer fired",))
timer.start()
timer.join()
print(results)                                  # ['timer fired']

never = threading.Timer(5, results.append, args=("never",))
never.start()
never.cancel()
never.join()
print(results, never.is_alive())                # ['timer fired'] False

# 6. A thread does not RETURN a value. Use an attribute, a list, a Queue,
#    or a Future from a pool:
with ThreadPoolExecutor(max_workers=1) as pool:
    future = pool.submit(pow, 2, 10)
    print(future.result())                      # 1024

# WAYS TO CREATE A THREAD
#   Thread(target=function, args=...)     the usual choice
#   subclass Thread and override run()    when the thread has its own state
#   Timer(seconds, function)              a delayed call
#   ThreadPoolExecutor.submit(function)   when you need the result (file 08)
