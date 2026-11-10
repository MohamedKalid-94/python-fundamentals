import io
import logging
import os
import sys

# LOGGING records what the program does, with a LEVEL for each message.
# Level numbers:  DEBUG 10, INFO 20, WARNING 30, ERROR 40, CRITICAL 50
print(logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL)
# 10 20 30 40 50

# 1. The quick start: configure the ROOT logger once (the default level is WARNING)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s:%(name)s:%(message)s",
    stream=sys.stdout,                          # the default is stderr
)
log = logging.getLogger("app")                  # one logger per module: getLogger(__name__)
log.debug("debug message")
log.info("info message")
log.warning("careful")
log.error("failed")
log.critical("system down")
# DEBUG:app:debug message
# INFO:app:info message
# WARNING:app:careful
# ERROR:app:failed
# CRITICAL:app:system down

# Pass values as ARGUMENTS (not an f-string): the text is built only if the message is shown
log.info("user %s logged in from %s", "ann", "10.0.0.1")
# INFO:app:user ann logged in from 10.0.0.1


# For the next examples, each logger writes into its own StringIO so the output is predictable.
def make_logger(name, level, fmt="%(levelname)s:%(message)s"):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False                    # do not also send it to the root logger
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(logging.Formatter(fmt))
    logger.addHandler(handler)
    return logger, stream


# 2. The level is a THRESHOLD: lower messages are dropped
lg, out = make_logger("t1", logging.WARNING)
lg.debug("d")
lg.info("i")
lg.warning("w")
lg.error("e")
print(out.getvalue().splitlines())              # ['WARNING:w', 'ERROR:e']

# 3. logging.exception() inside an except block adds the traceback
lg, out = make_logger("t2", logging.INFO)
try:
    1 / 0
except ZeroDivisionError:
    lg.exception("calculation failed")
text = out.getvalue()
print(text.splitlines()[0])                     # ERROR:calculation failed
print("Traceback" in text)                      # True
print(text.splitlines()[-1])                    # ZeroDivisionError: division by zero

# 4. Useful format fields:
#    %(asctime)s time   %(levelname)s level   %(name)s logger   %(message)s text
#    %(filename)s file  %(lineno)d line       %(funcName)s function
lg, out = make_logger("t3", logging.INFO, "%(funcName)s:%(message)s")

def work():
    lg.info("hi")

work()
print(out.getvalue().strip())                   # work:hi

# 5. Log to a FILE
file_logger = logging.getLogger("t4")
file_logger.setLevel(logging.INFO)
file_logger.propagate = False
fh = logging.FileHandler("app.log", encoding="utf-8")
fh.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
file_logger.addHandler(fh)
file_logger.info("started")
file_logger.error("disk full")
fh.close()
file_logger.removeHandler(fh)
with open("app.log", encoding="utf-8") as f:
    print(f.read().splitlines())                # ['INFO started', 'ERROR disk full']
os.remove("app.log")

# 6. Several handlers with different levels (console: warnings only, file: everything)
lg = logging.getLogger("t5")
lg.setLevel(logging.DEBUG)
lg.propagate = False
console, logfile = io.StringIO(), io.StringIO()
h1 = logging.StreamHandler(console)
h1.setLevel(logging.WARNING)
h2 = logging.StreamHandler(logfile)
h2.setLevel(logging.DEBUG)
for h in (h1, h2):
    h.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
    lg.addHandler(h)
lg.debug("trace")
lg.error("boom")
print(console.getvalue().splitlines(), logfile.getvalue().splitlines())
# ['ERROR boom'] ['DEBUG trace', 'ERROR boom']

# 7. Logger names form a hierarchy: "t6.db" is a child of "t6" and shares its handlers
lg, out = make_logger("t6", logging.INFO)
logging.getLogger("t6.db").info("query ok")
print(out.getvalue().strip())                   # INFO:query ok

# WHICH TOOL?
#   print()     quick checks while you write code
#   logging     what a real program records: levels, files, formats, no code changes to silence it
#   exceptions  something went wrong and the caller must react
#   warnings    something is deprecated or suspicious, but the program can continue
# Never log passwords or personal data.