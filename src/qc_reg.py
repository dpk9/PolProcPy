#!/usr/bin/python
"""
usage:
./qc_reg cyclename
 where:
  cyclename is the cyclename (without extension) we want to look at;
     software assumes it is looking for files cyclename.beadsums and
     cyclename.register-log

OUTPUT is: fcnum\tarraynum\timgnum\tnum_objs\tbeadsum\tdiff_x\tdiff_y\n

Greg Porreca (Church Lab) 12-05-2007
Translated to Python by David Kalish 11-30-2010
"""

import glob
import sys
import struct

array = glob.glob("*.info")
num_files = len(array)
INF = open(array[0],'rb')

beadsumfilename = sys.argv[1] + ".beadsums"
BEADSUM = open(beadsumfilename)

reglogfilename = sys.argv[1] + ".register-log"
REGLOG = open(reglogfilename)

for line in REGLOG.readlines():
    buffer = INF.read(8)
    line0,line1,line2,line3 = struct.unpack('HHHH', buffer)
    curr_img = line2
    if curr_img == 0:
	   last_x = 0
	   last_y = 0
    

    buffer = BEADSUM.read(8)
    sumline = struct.unpack('q', buffer)
    sumline = sumline[0]
    
    line = line.rstrip()
    regline = line.split("\t")
    curr_x = regline[0]
    curr_y = regline[1]
    x_diff = curr_x - last_x
    y_diff = curr_y - last_y
    
    last_x = curr_x
    last_y = curr_y
    
    print "%(line0)s\t%(line1)s\t%(line2)s\t%(line3)s\t%(sumline)s\t%(x_diff)s\t%(y_diff)s\t%(surr_x)s\t%(curr_y)s" %vars()

INF.close()
BEADSUM.close()
REGLOG.close()
