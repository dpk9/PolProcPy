#!/usr/bin/python

#------------------------------------------
# Done, except for lines 10 and 11.
#------------------------------------------

import os
import sys

cw = os.getcwd()
#$ENV{'MATLABPATH'} = $cw;
#$ENV{'LIBXCB_ALLOW_SLOPPY_LOCK'} = 1;

argv = sys.argv

argv0 = argv[1]
argv1 = argv[2]
os.system("./run_disp_delta.sh /opt/MATLAB/MATLAB_Component_Runtime/v77/ %(argv0)s %(argv1)s" % vars())

cyclename = argv[1][3:4]

try:
    QCDONE = open("qc_cycle_list_QC-done.dat", 'r')
except IOERROR:
    sys.exit('ERROR: "qc_cycle_list_QC-done.dat" is not present.')
found = 0
for line in QCDONE.readlines():
    line = line.strip("\n")
    if line.find(cyclename) != -1:
        found = 1
QCDONE.close()

if found == 0:
    QCDONE = open("qc_cycle_list_QC-done.dat", 'w')
    print >> QCDONE, cyclename
    QCDONE.close()
