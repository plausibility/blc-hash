blc-hash
========

This is a multi-threaded sha512 hashing script to work away at creating hashes viable for [BlooCoin](https://github.com/Max00355/BlooCoin), which is just this little semi-crypto-currency some guy I know made.

This project is MIT licensed, so you can do whatever you want with it, really.

It's pretty simple, just creates a random starting point which is a five long string made up of alphanumeric (uppercase, lowercase, digits) and then just adds a number onto the end until a hash starts with enough zeros for the difficulty of the current server.

The usage is as such:
```
usage: blc_hash.py [-h] [-t THREADS] [-q QUEUE] [-u UPPER_BOUND] [--debug]
                   [-d DIFFICULTY]

Mine your way to riches and glory (or something..) with BlooCoins.

optional arguments:
  -h, --help            show this help message and exit
  -t THREADS, --threads THREADS
                        The amount of worker threads
  -q QUEUE, --queue QUEUE
                        The queue size to work through
  -u UPPER_BOUND, --upper-bound UPPER_BOUND
                        The upper bound at which we abandon the job (default:
                        1500000.0)
  --debug               Spam the terminal with debugging text.
  -d DIFFICULTY, --difficulty DIFFICULTY
                        The difficulty as reported by the server
```

If it gets a hit, it'll create a file which ends in `.blc` so you can filter them and stuff.
