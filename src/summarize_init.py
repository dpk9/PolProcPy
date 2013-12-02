#!/usr/bin/python
"""Contains a custom python module "commify" found at:
    http://code.activestate.com/lists/python-list/24843/
    """
import sys
import struct

from commify import commify

INF = open(sys.argv[1],'rb')
argc = len(sys.argv)
count = 0
totals = {}

data = INF.read()
a = 0
b = 8
while data[a:b]:
    buffer = data[a:b]
    a += 8
    b += 8
    line0,line1,line2,line3 = struct.unpack('HHHH', buffer)
    if argc > 1:
        if line1 == sys.argv[2]:
            count += line3
            print "%(line0)s\t%(line1)s\t%(line2)s\t%(line3)s"

    else:
        if  totals[line1]:
            totals[line1] += line3
        else:
            totals[line1] = line3
        count += line3
        print "%(line0)s\t%(line1)s\t%(line2)s\t%(line3)s"

INF.close()
commacount = commify(count)
print "TOTAL BEADS: %(commacount)s" %vars()
print "PER ARRAY:";
for i in xrange(line1+1): # the last line in the list tells us how many arrays
    commatotals = commify(totals[i])
    print "%(i)s\t%(commatotals)s" %vars()
