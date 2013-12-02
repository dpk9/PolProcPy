#!/usr/bin/python

# keep track of cycles already done
# iterate over directory listing, and compare each to this list
# if not already done, look for all 4 colors present;
# if all 4 present, make sure all file sizes are equal and nonzero
# if this is true, assume the cycle is finished and run QC metrics
#
# Greg Porreca (Church Lab) 11-10-2008
#

import os
import glob
import re
import time
import commands


LOGFILE = open("autoqc-log", 'a')

qclistfn = "qc_cycle_list.dat"
qclistdonefn = "qc_cycle_list_processing-done.dat"
qclistqcdonefn = "qc_cycle_list_QC-done.dat"

qc_complete = {}
cycles_todo = {}
cycle_toqc = {}
beadfile_size = {}
num_cycles_done = 0
made_defaultprimer = 0 #the first time this runs and finds a cycle, make a primer file out of it

# If these .dat files don't exist, make them.
if os.path.isfile("./" + qclistfn) != True:
    os.system("touch " + qclistfn)
if os.path.isfile("./" + qclistdonefn) != True:
    os.system("touch " + qclistdonefn)
if os.path.isfile("./" + qclistqcdonefn) != True:
    os.system("touch " + qclistqcdonefn)

# load the list of cycles already done
if os.path.isfile(qclistfn):
    QCLIST = open(qclistfn,'r')
    for line in QCLIST.readlines():
        line = line.rstrip()
        if line in qc_complete.keys(): qc_complete[line] += 1
        else: qc_complete[line] = 1
        num_cycles_done += 1
        print str(num_cycles_done)
    QCLIST.close()

# now determine whether each cycle we have bead files for has already been QC'd
beadlist = glob.glob("beads/*.beads")
for beadfile in beadlist:
    if re.search("beads/0_(....)_[ACGT].beads", beadfile):
        match = re.search("beads/0_(....)_[ACGT].beads", beadfile).group(1)
        if qc_complete[match] == 1:
            pass
        else:
            if match in cycle_toqc.keys(): cycle_toqc[match] += 1
            else: cycle_toqc[match] = 1
            size = os.stat(beadfile).st_size
            beadfile_size[beadfile] = size
            print >> LOGFILE, "not yet done cycle %(match)s (%(beadfile)s:%(size)s)" % vars()

# now, for each outstanding cycle to be done, make sure all data is present; if it is,
# add the cycle name to the qclist file, then to the todo list
QCLIST = open(qclistfn, 'a')
for key, value in cycle_toqc.iteritems():
    if value == 4:
        full_filesize = beadfile_size["beads/0_" + key + "_A.beads"]
        if (full_filesize
            == beadfile_size["beads/0_" + key + "_C.beads"] 
            == beadfile_size["beads/0_" + key + "_G.beads"]
            == beadfile_size["beads/0_" + key + "_T.beads"] > 0):
            if key in cycles_todo.keys(): cycles_todo[key] += 1
            else: cycles_todo[key] = 1
            print >> QCLIST, key
            now = time.asctime()
            
            QCDONELIST = open(qclistdonefn,'a')
            print >> QCDONELIST, key
            QCDONELIST.close()
            
            print >> LOGFILE, now + "\tFound new complete cycle " + key
            if num_cycles_done == made_defaultprimer == 0:
                print >> LOGFILE, (now + "\tGenerating default primer file " + 
                                   "from cycle " + key)
                os.system("./makePrimerFile.py " + key)
                made_defaultprimer = 1

QCLIST.close()

# start the Xvfb
now = time.asctime()
print >> LOGFILE, now + "\tStart Xvfb"
os.system("/usr/bin/Xvfb :1 -fp built-ins -once -r -screen 0 1280x1024x24&")

# now, execute the QC for each cycle in the todo list
for key, value in cycles_todo.iteritems():
    now = time.asctime()
    print >> LOGFILE, now + "\tExecuting QC on cycle " + key
    
    now = time.asctime()
    print >> LOGFILE, now + "\tStart Xvfb"
    os.system("/usr/bin/Xvfb :1 -fp built-ins -once -r -screen 0 1280x1024x24&")
    
    cmd = "./disp_regQC.py " + key
    now = time.asctime()
    print >> LOGFILE, "%(now)s\t%(cmd)s" % vars()
    
    output = commands.getoutput(cmd)
    print >> LOGFILE, output
    
    cmd = "./disp_tetra-delta.py " + key
    
    now = time.asctime()
    print >> LOGFILE, "%(now)s\t%(cmd)s" % vars()
    
    output = commands.getoutput(cmd)
    print >> LOGFILE, output
    
LOGFILE.close()
