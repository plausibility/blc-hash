#!/usr/bin/env python
import sys
import threading
import Queue
import random
import time
import string
import hashlib
import argparse

###
thread_list = []
charmap = string.lowercase + string.uppercase + string.digits
###

parser = argparse.ArgumentParser(description="Mine your way to riches and glory (or something..) with BlooCoins.")
parser.add_argument("-t", "--threads",
                    help="The amount of worker threads",
                    type=int,
                    default=5)
parser.add_argument("-q", "--queue",
                    help="The queue size to work through",
                    type=int,
                    default=50)
parser.add_argument("-u", "--upper-bound",
                    help="The upper bound at which we abandon the job (default: %(default)s)",
                    type=int,
                    default=1.5*(10**6))
parser.add_argument("--debug",
                    help="Spam the terminal with debugging text.",
                    action="store_true")
parser.add_argument("-d", "--difficulty",
                    help="The difficulty as reported by the server",
                    type=int,
                    default=7)
args = parser.parse_args()

start_time = time.time()
 
def start_string():
    return "".join([random.choice(charmap) for _ in xrange(0, 5)])

q = Queue.Queue()

def worker():
    difficulty = args.difficulty
    num = 0
    buf = "0" * difficulty # (7 == difficulty from server atm)
    while True:
        work = q.get()
        num = 0
        sys.stdout.write("[{0}] started work".format(work) + "\n")
        sys.stdout.flush()
        # Layered while loops, because... fuck it.
        while True:
            work_hash = hashlib.sha512(work + str(num)).hexdigest()
            if work_hash[0:difficulty] == buf:
                with open(work + str(num) + '.blc', 'w') as f:
                    f.write(work_hash)
                sys.stdout.write("[{0}] Hit the jackpot! // {0}{1} -> {2}".format(work, num, work_hash) + "\n")
                sys.stdout.flush()
                break
            num += 1
            if num >= args.upper_bound:
                if args.debug:
                    sys.stdout.write("[{0}] hit upper bound: {1}".format(work, num) + "\n")
                sys.stdout.write("[{0}] no success".format(work) + "\n")
                sys.stdout.flush()
                break
        q.task_done()
 
for i in range(args.threads):
    t = threading.Thread(target=worker)
    thread_list.append(t)
    t.daemon = True
    t.start()

for i in range(0, args.queue):
    q.put(start_string())

q.join()

finish_time = time.time()

print "Finished in:", finish_time - start_time, "-", "TADA!"