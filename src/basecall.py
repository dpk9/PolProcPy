#!/usr/bin/python

#------------------------------------------
# Done. Needs testing.
#------------------------------------------

import sys
import os
import time
import glob

argv = sys.argv
del argv[0]
argc = len(argv)

if argc != 3:
    sys.exit("""ERROR: must call with 3 args: base name of output files, percentage of data to
keep, and background subtraction pixel value expressed as a percentage\n""")

try:
    READSPECFILE = open("readspec", 'r')
except IOERROR:
    sys.exit("ERROR:\treadspec (file specifying cycles to call) not present\n")
try:
    PRIMERTHRESH = open("primer_thresholds.dat", 'r')
except IOERROR:
    sys.exit("ERROR:\tprimer_thresholds.dat not present\n")


rdinf_cmd = "output_data/" + str(argv[0]) + ".readfileinfo"
READINFO = open(rdinf_cmd, 'w')
argv0 = argv[0]
argv1 = argv[1]
argv2 = argv[2]
d = time.localtime()
datestamp = str(d[1]) + "-" + str(d[2]) + "-" + str(d[0])
print >> READINFO, "Basecaller executed on " + datestamp + "\n"
print >> READINFO, "Python script called as: python basecall.py %(argv0)s %(argv1)s %(argv2)s" % vars()
print >> READINFO, "--basecall file name: " + argv[0]
print >> READINFO, "--percentage of data to keep: " + str(argv[1]) + "%"
print >> READINFO, "--percentage pixel value for background subtraction: " + str(argv[2]) + "%\n"
print >> READINFO, "Using the following cycles:"

beadfiles = ""
for line in READSPECFILE.readlines():
    line = line.strip("\n")
    fn = "beads/0_" + line
    beadfiles = beadfiles + fn + "_A "
    beadfiles = beadfiles + fn + "_C "
    beadfiles = beadfiles + fn + "_G "
    beadfiles = beadfiles + fn + "_T "
    print >> READINFO, "\t" + line
READSPECFILE.close()

dirlist = glob.glob("*.info")
if not dirlist:
    print 'ERROR:\tNo ".info" file.'
    exit()
infofilename = dirlist[0]
print >> READINFO, "Using info file" + infofilename
print >> READINFO, "Using primer thresholds of: (FC0 lanes 1-8, FC1 lanes 1-8)"
for line in PRIMERTHRESH.readlines():
    print >> READINFO, line.strip("\n")
PRIMERTHRESH.close()

print >> READINFO, "\nExecuting basecaller as follows:"

# Use this one to output tetrahedron info:
basecallercmd = "./basecaller notruncmdln 1 1 %(argv0)s %(infofilename)s %(argv1)s %(argv2)s %(beadfiles)s" % vars()

# Use this one to not output tetrahedron info:
#basecallercmd = "./basecaller notruncmdln 1 0 %(argv0)s %(infofilename)s %(argv1)s %(argv2)s %(beadfiles)s" % vars()

print >> READINFO, basecallercmd

READINFO.close()

print "EXECUTING " + basecallercmd

os.system(basecallercmd)
