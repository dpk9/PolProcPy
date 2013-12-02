#!/usr/bin/python

import sys
import struct

INF = open(sys.argv(1), 'rb')
BEADSUM = open(sys.argv(2), 'rb')

buffer = INF.read(8)
buffer2 = BEADSUM.read(8)
line0,line1,line2,line3 = struct.unpack('HHHH', buffer)
line4 = struct.unpack('q', buffer2)
line4 = line4[0]
print "%(line0)s\t%(line1)s\t%(line2)s\t%(line3)s\t%(line4)s" %vars()

INF.close()
BEADSUM.close()

"""
while(read(INF, $buffer, 8) and @line = unpack('SSSS', $buffer) and print "$line[0]\t$line[1]\t$line[2]\t$line[3]\t" and read(BEADSUM, $buffer2, 8) and @line = unpack('q', $buffer2) and print "$line[0]\n"){;}
close INF;
close BEADSUM;
"""