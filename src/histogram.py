#!/usr/bin/python
"""
Call this to display a histogram for a single set of images
(i.e. either a set of primer images, or one color from a sequencing cycle)
"""

import sys
import glob
import os

ARGV = sys.argv
del ARGV[0]
argc = len(ARGV) 

if argc == 3:
    ARGV.append("0") #If histogramThreshold field is left blank, make it zero.
    print "ARGV has been appended to " + str(ARGV)

dirlist = glob.glob("*.info")
num_infofiles = len(dirlist)
 
if num_infofiles > 2:
    print >> sys.stderr, ("ERROR:\tthere are " + str(num_infofiles) + " possible input files,"
            + "\nand I don't know which to use:")
    for infofile in dirlist:
        print >> sys.stderr, "\t" + str(infofile)
 
else:
    if dirlist:
        exec_string = ("./histogram " + dirlist[0] + " beads/" + str(ARGV[1])
                       + "_" + str(ARGV[0]) + ".beads " + ARGV[1] + " " + ARGV[2]
                       + " " + ARGV[3])
        print "EXECUTING:\t" + exec_string
        os.system(exec_string)
