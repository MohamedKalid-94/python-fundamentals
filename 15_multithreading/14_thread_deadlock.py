import threading

# DEADLOCK: threads wait for each other FOREVER.
# It needs four conditions together (Coffman):
#   1. mutual exclusion   a resource can be held by only one thread
#   2. hold and wait      a thread holds one resource while waiting for another
#   3. no preemption      a resource cannot be taken away
#   4. circular wait      A waits for B, and B waits for A
# Remove ANY ONE and deadlock cannot happen.

# The classic recipe (do not run it, it hangs forever):
#   Thread 1:  lock_a.acquire(); lock_b.acquire()
#   Thread 2:  lock_b.acquire(); lock_a.acquire()
# If each thread gets its first lock, both wait for the second one for ever.

# 1. A SAFE demonstration: acquire() with a timeout, and Barriers to force the bad moment
lock_a, lock_b = threading.Lock(), threading.Lock()
both_hold_first = threading.Barrier(2)
both_tried = threading.Barrier(2)
log = []

def worker(name, first, second):
    with first:
        both_hold_first.wait()                  # make sure BOTH threads hold their first lock
        if second.acquire(timeout=0.2):
            log.append(f"{name} got both")
            second.release()
        else:
            log.append(f"{name} timed out: deadlock")
        both_tried.wait()                       # keep the first lock until both have tried

t1 = threading.Thread(target=worker, args=("T1", lock_a, lock_b))
t2 = threading.Thread(target=worker, args=("T2", lock_b, lock_a))
t1.start()
t2.start()
t1.join()
t2.join()
print(sorted(log))
# ['T1 timed out: deadlock', 'T2 timed out: deadlock']

# 2. FIX 1: always take the locks in the SAME ORDER (removes the circular wait)
log = []

def safe_worker(name, a, b):
    first, second = sorted((a, b), key=id)      # one global order for every thread
    with first, second:
        log.append(f"{name} ok")

t1 = threading.Thread(target=safe_worker, args=("T1", lock_a, lock_b))
t2 = threading.Thread(target=safe_worker, args=("T2", lock_b, lock_a))
t1.start()
t2.start()
t1.join()
t2.join()
print(sorted(log))                              # ['T1 ok', 'T2 ok']

# 3. A thread can deadlock ALONE: a Lock is not re-entrant
single = threading.Lock()
single.acquire()
print(single.acquire(timeout=0.05))             # False   it would wait for itself for ever
single.release()

reentrant = threading.RLock()
reentrant.acquire()
print(reentrant.acquire(timeout=0.05))          # True    the same thread may take it again
reentrant.release()
reentrant.release()

# OTHER WAYS TO PREVENT IT
#   - hold only ONE lock at a time (best)
#   - use timeouts: acquire(timeout=...), then back off and retry
#   - use a Queue: a single thread owns the data, others send it requests
#   - an RLock when the same thread re-enters its own code
#
# OTHER PROBLEMS
#   livelock     threads keep reacting to each other but make no progress
#   starvation   one thread never gets the lock because others always win
#
# FINDING A DEADLOCK
#   import faulthandler
#   faulthandler.dump_traceback_later(10, exit=True)   # prints every thread's stack after 10 s
#   (or the external tool py-spy: "py-spy dump --pid <pid>")