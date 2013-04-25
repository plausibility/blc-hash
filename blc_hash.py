#!/usr/bin/env python
import sys
import threading
import Queue
import random
import time
import string
import hashlib

###
thread_count = 5
thread_list = []

debug = False
quiet = False

# TODO: submit to sqlite3 database
possible = []
upper_bound = 1.5 * (10**6)

charmap = string.lowercase + string.uppercase + string.digits
###

if len(sys.argv) < 2:
    print "Invalid arguments: <threads>"
    sys.exit(1)
try:
    thread_count = int(sys.argv[1])
    for arg in sys.argv:
        if arg.lower() in ('-d', '--debug'):
            debug = True
            break
        elif arg.lower() in ('-q', '--quiet'):
            quiet = True
            break
except:
    print "Error parsing arguments: <threads>"
    sys.exit(1)

start_time = time.time()
 
def start_string():
    return "".join([random.choice(charmap) for _ in xrange(0, 5)])

q = Queue.Queue()

def worker():
    difficulty = 7
    num = 0
    buf = "0"*7#chr(0) * difficulty # (7 == difficulty from server)
    while True:
        work = q.get()
        num = 0
        sys.stdout.write("Working on: " + work + "\n")
        sys.stdout.flush()
        # Layered while loops, because... fuck it.
        while True:
            work_hash = hashlib.sha512(work + str(num)).hexdigest()
            if work_hash[0:difficulty] == buf:
                with open(work + str(num) + '.blc', 'w') as f:
                    f.write(work_hash)
                sys.stdout.write("Hit the jackpot // " + work + str(num) + " -> " + work_hash + "\n")
                sys.stdout.flush()
                break
            num += 1
            if num >= upper_bound:
                if debug:
                    sys.stdout.write("hit upper bound: " + str(num) + " @" + work + "\n")
                    sys.stdout.flush()
                break
        q.task_done()
 
for i in range(thread_count):
    t = threading.Thread(target=worker)
    thread_list.append(t)
    t.daemon = True
    t.start()

for i in range(0, 50):
    q.put(start_string())

q.join()

finish_time = time.time()

print finish_time - start_time, "!", "TADA!"