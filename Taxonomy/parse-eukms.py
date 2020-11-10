#!/usr/bin/env python3
import os
import sys

r = open(sys.argv[1], "r")
w = open("/dev/stdout", "a")
w.write(sys.argv[2])
i = 0
for line in r:
	line = line.rstrip("\r\n").split()
	if line[3] in ("kingdom", "phylum", "class", "order", "family"):
		w.write("\t" + line[5])
	elif line[4] == "genus":
		w.write(line[5] + "\n")
		break
	i += 1
	if i > 15:
		w.write("\n")
		break
w.close()
