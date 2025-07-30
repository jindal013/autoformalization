# test.py
import sys

print("Reading input:")
for line in sys.stdin:
    print("Got:", line.strip()) # not the same as .split(), which returns a list