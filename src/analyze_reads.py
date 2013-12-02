#!/usr/bin/python

import sys
import re
import fileinput

num_imgs=xrange(2180)
correct = dict({})
incorrect = dict({})

for j in num_imgs:
    correct[j] = 0
    incorrect[j] = 0

print correct
print incorrect

a,c,g,t = "","","",""
input = sys.stdin.readlines()
for line in input:
    line = line.rstrip()
    line = line.split("\t")
    curr_fc = line[0]
    curr_array = line[1]
    seq = line[4]
    readlength = len(seq)
#    print >> sys.stderr, "{0}\t{1}\t{2}".format(curr_fc,curr_array,readlength)
    print >> sys.stderr, "%(curr_fc)s\t%(curr_array)s\t%(readlength)s" % vars()
    Range = xrange(readlength)
    for n in Range:
        a += "A"
        c += "C"
        g += "G"
        t += "T"

if re.search(".\..", seq): pass
else:
    if seq == a or seq == c or seq == g or seq == t:
        correct[line[2]] += 1
    else:
        incorrect[line[2]] += 1

for line in fileinput.input():
    line = line.rstrip()
    line = line.split("\t")
    seq = line[4]
    if re.search(".\..", seq): pass
    else:
        if seq == a or seq == c or seq == g or seq == t:
            correct[line[2]] += 1
        else:
            incorrect[line[2]] += 1
            
for j in num_imgs:
    sum = correct[j] + incorrect[j]
    if sum > 0:
        error_rate = incorrect[j]/sum
    else:
        error_rate = 0
    corr = correct[j]
    incorr = incorrect[j]
    print "%(curr_fc)s\t%(curr_array)s\t%(j)s\t%(corr)s\t%(incorr)s\t%(sum)s\t%(error_rate)s" % vars()
