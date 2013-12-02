#!/usr/bin/python
"""
Call this to display a histogram for a cycle of images; the value for a 
given bead will be its mean value in all 4 channels
"""

import sys
import glob
import os

ARGV = sys.argv
del ARGV[0]

argc = len(ARGV) + 1

if argc == 3:
    ARGV.append("0") #If histogramThreshold field is left blank, make it zero.

dirlist = glob.glob("*.info")
num_infofiles = len(dirlist)

if num_infofiles > 2:#Why would this be 2 instead of 1?  Who's to say what order 
                     #these two files show up, and only one of them is called.
    print >> sys.stderr, ("ERROR:\tthere are " + str(num_infofiles) +
                          " possible input files,\n"
                          + "and I don't know which to use:")
    for infofile in dirlist:
        print >> sys.stderr, "\t" + str(infofile)

else:
    if dirlist:
        exec_string = ("./histogram4 " + dirlist[0] + " beads/" + str(ARGV[1]) + "_"
                       + str(ARGV[0]) + " " + str(ARGV[1]) + " " + str(ARGV[2])
                       + " " + str(ARGV[3]))
        print "EXECUTING:\t" + exec_string
        os.system(exec_string)
