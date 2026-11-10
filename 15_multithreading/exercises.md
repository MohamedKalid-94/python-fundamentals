Write the questions as # comments and your solutions as code below each one. Make your outputs deterministic: sort the results, join the threads, and use Events instead of sleeps for ordering.

Create 5 threads that each print their own name and a number, and join them. Run the program 5 times and note that the order of the lines changes. Then collect the lines in a list and print them sorted.
Write download(url) that sleeps for a random time between 0.1 and 0.3 seconds (use a fixed random.seed), and measure with time.perf_counter() how long 8 downloads take one after the other, with 8 threads, and with a pool of 3 workers.
Show that two CPU-bound threads (a loop of 5 million additions each) are not faster than running the loops one after the other. Print the two times and explain in a comment (the GIL).
Subclass Thread to make a SumWorker that adds the numbers of a range and keeps its result; split range(1, 1_000_001) over 4 workers and add the partial sums.
Demonstrate the thread life cycle: print the state of a thread before start(), while it waits on an Event, and after it ends. Then show what happens when you call start() twice.
Show run() versus start() by printing the current thread name in each case.
Write a program with a deliberately unsafe counter (read, sleep(0.001), write) and show the wrong result. Then fix it with a Lock, with an RLock, and by using a Queue so that only one thread changes the counter.
Write a BankAccount class with deposit and withdraw protected by a lock. Run 10 threads that deposit 100 times each and 10 threads that withdraw 100 times each, and show that the final balance is correct.
Use a Semaphore(3) so that at most 3 of 10 threads are in a “database connection” section at once, and prove it by recording the peak number of active threads.
Use a Barrier(4) to make 4 threads finish “stage 1” before any of them starts “stage 2”, and print the stages from a list to prove the order.
Write a producer-consumer program with a bounded Queue(maxsize=5): one producer, three consumers, and a sentinel for each consumer. Count how many items each consumer handled and show that the total is correct.
Write a two-stage pipeline with queues: read numbers, filter the even ones, square them, and sum them. Compare the answer with a plain single-threaded loop.
Use a Condition to build a thread-safe bounded buffer class with put(item) and get() that block when the buffer is full or empty.
Use threading.local() to give each thread its own “request id”, and show that each thread sees only its own value, even though they all use the same function.
Build a ThreadPoolExecutor job that checks 20 “ports” (a function that sleeps and returns open or closed from a fixed list), print the open ones in order, and show how a task that raises an error is reported through its Future.
Use as_completed to print results in the order tasks finish, with different sleep times, and use future.add_done_callback to log each finished task.
Write a Heartbeat daemon thread that increments a counter every 0.05 seconds, and a version with a normal thread and a stop Event. Show that the second one can be stopped cleanly and the first one cannot.
Write a StoppableThread class with stop() and stopped() that reads items from a queue with a timeout, and stop it while the queue is empty and while it is busy. Show that both cases end quickly.
Reproduce a deadlock with two locks and two threads using acquire(timeout=...) and Barriers (as in file 14), then fix it with ordered locking, and again by using one single lock. Explain which of the four conditions each fix removes.
Write run_with_timeout(func, seconds) that raises TimeoutError when func takes too long, and returns the result otherwise, plus a version that uses ThreadPoolExecutor and future.result(timeout=...). Explain why the slow function still keeps running.
Embedded exercise: simulate a sensor board with three threads: a “sensor” thread that produces readings every 0.02 s, a “filter” thread that averages the last 4 readings, and a “display” thread that prints the average with logging (use the thread names in the log). Stop everything cleanly after 10 readings.
Predict first, then run, and explain each result in a comment:
python
import threading, queue

results = []
t = threading.Thread(target=results.append, args=("a"))
try:
    t.start()
    t.join()
except Exception as e:
    print(type(e).__name__)

lock = threading.Lock()
print(lock.acquire(blocking=False), lock.acquire(blocking=False))
lock.release()

e = threading.Event()
print(e.wait(0.01), e.is_set())

q = queue.Queue(maxsize=1)
q.put(1)
try:
    q.put(2, block=False)
except queue.Full:
    print("full")

d = threading.Thread(target=lambda: None, daemon=True)
d.start()
d.join()
print(d.daemon, d.is_alive(), threading.active_count())