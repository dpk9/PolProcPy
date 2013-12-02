#!/usr/bin/python

import sys
import glob
import os

#TETRA_FRAME = 1151
TETRA_FRAME = 1000
PERCENT_TOKEEP = 50
PERCENT_BGSUBTRACT = 5

if len(sys.argv) > 1:
    Argv = sys.argv
    del Argv[0]
else:
    print >> sys.stderr, "ERROR:\tNo command line arguments. Exiting."
    sys.exit(1)

# Verify basecaller input files are present
#
argv0 = Argv[0]
beadfn1 = "beads/0_" + Argv[0] + "_A"
beadfn2 = "beads/0_" + Argv[0] + "_C"
beadfn3 = "beads/0_" + Argv[0] + "_G"
beadfn4 = "beads/0_" + Argv[0] + "_T"
beadfns = (beadfn1, beadfn2, beadfn3, beadfn4)

for beadfn in beadfns:
    globstring = beadfn + "*"
    if len(glob.glob(globstring)) == 0:
        print >> sys.stderr, "ERROR:\tbead file $(beadfn)s does not exist. Exiting." % vars()
        sys.exit(1)
        
# Run basecaller to generate .tetra files and .delta files
#
dirlist = glob.glob("*.info")
num_infofiles = len(dirlist)
if num_infofiles > 2:
    print >> sys.stderr, "ERROR:\tToo many info files (expecting 2 max). Exiting."
    sys.exit(1)
elif num_infofiles == 0:
    print >> sys.stderr, "ERROR:\tUnable to find a .info file. Exiting."
    sys.exit(1)

info_filename = dirlist[0]

exec_cmd = "./basecaller notruncmdln 0 1 %(argv0)s-QC %(info_filename)s %(PERCENT_TOKEEP)s %(PERCENT_BGSUBTRACT)s %(beadfn1)s %(beadfn2)s %(beadfn3)s %(beadfn4)s" % vars()
print "EXECUTING:\t" + exec_cmd
os.system(exec_cmd)

# Run matlab QC routines
#$exec_cmd = "./disp_regQC.py $ARGV[0]";
#print "EXECUTING:\t$exec_cmd\n";
#system "$exec_cmd";

exec_cmd = "./disp_delta.py tetrahedra/%(argv0)s-QC.delta QC-%(argv0)s-delta" % vars()
print "EXECUTING:\t" + exec_cmd
os.system(exec_cmd)

n = xrange(8)
for i in n:
    numstr = "%02d" % i
    exec_cmd = "./disp_tetra.py tetrahedra/%(argv0)s-QC_0_%(numstr)s.tetracoords %(TETRA_FRAME)s QC-%(argv0)s-0_%(numstr)s-tetra" % vars()
    print "EXECUTING:\t" + exec_cmd
    os.system(exec_cmd)
