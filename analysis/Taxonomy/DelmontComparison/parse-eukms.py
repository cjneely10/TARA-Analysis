#!/usr/bin/env python3
import os
import sys

if not os.path.exists(sys.argv[1]):
	exit()
r = open(sys.argv[1], "r")
w = open("/dev/stdout", "a")
w.write(sys.argv[2])
i = 0
tax_levels = ("kingdom", "phylum", "class", "order", "family", "genus")
data = {tax: "." for tax in tax_levels}
for line in r:
	line = line.rstrip("\r\n").split()
	if line[3] in tax_levels and data[line[3]] == ".":
		data[line[3]] = line[5]
	i += 1
	if i > 15:
		break
for t in tax_levels:
	w.write("\t" + data[t])
w.write("\n")
w.close()
