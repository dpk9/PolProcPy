#!/usr/bin/python

import sys
import struct

num_perframe = 2000
curr_num = num_perframe

REG = open(sys.argv[1], 'r')

for i in xrange(45252):
    fn = "%(i)07d.coords" % vars()
    FILE = open(fn, 'w')
    for j in xrange(num_perframe):
        buffer = REG.read(4)
        line0, line1 = struct.unpack('HH', buffer)
        print >> FILE, "%(line0)s\t%(line1)s" %vars()
    FILE.close()
REG.close()