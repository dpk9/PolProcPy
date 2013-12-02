#!/usr/bin/python
"""
initialize_processor.py

Execute this perl script to initialize the image processing pipeline.
The directory should be clean (i.e. no data files present from a
previous run).  Compile must have been run in the src/ directory to
generate the binaries.

Written in Perl by Greg Porreca (Church Lab) 01-23-2008
Translated to Python by David Kalish 11-9-2010
"""

import os
import sys
import glob
import re
#import commands

from PyQt4.QtCore import *

ACQUISITION_NAME = "acq"

# Before we do anything, we need to compile the source
#
working_dir = os.getcwd()
exec_string = "src/compile.py " + working_dir
print "EXECUTING:\t" + exec_string
sys.stdout.flush()
#os.system(exec_string)
proc = QProcess()
proc.setProcessChannelMode(2)
proc.start(exec_string)

QObject.connect(proc, SIGNAL("readyRead()"), proc_readyRead)
QObject.connect(proc, SIGNAL("finished(int)"), proc_finished)

def proc_readyRead(self):
    outtext = (str(proc.readAllStandardOutput()).rstrip('\n'))
    print outtext
    
def proc_finished(self):
    finishedoutput = str(proc.readAllStandardOutput())
    finishederror = str(proc.readAllStandardError())
    print finishedoutput
    print finishederror

# Only call make_regfile.c if we can unambiguously determine the
# name of the bead position file.  There should be one position file
# and one info file (with the same name) in the directory.  If more
# are present, the directory was not cleaned up properly after the
# last run.
# 


# First, execute initialize_processor.c to generate the bead position file
# and the .info file.  Then, when that is finished, run make_regfile to
# generate data files used by processor.c during fluorescence image processing.
#

# Don't go any further if a position file already exists, since we
# may have been run by accident and will clobber the existing pipeline
#
dirlist = glob.glob("*.info")
num_infofiles = len(dirlist)
if num_infofiles > 0:
    print >> sys.stderr, ("ERROR:\tOne or more position info files already exist in the current directory;")
    print >> sys.stderr, ("\tfirst pre-existing position info file found is "
                          + dirlist[0])
    print >> sys.stderr, ("\texiting to prevent accidental clobbering of existing processing pipeline")
    proc.close()
    sys.stdout.flush()
    sys.exit()

# 'initialize_processor' should make some .info files now if there were
# none to begin with:

exec_string = working_dir + "/initialize_processor " + ACQUISITION_NAME
print "EXECUTING:\t" + exec_string
sys.stdout.flush()
num_fcs = os.system(exec_string) >> 8 #initialize_processor.c returns the number of flowcells
print "initialize_processor returned " + str(num_fcs) + " flowcells for this run."
sys.stdout.flush()

# Now, run make_regfile
dirlist = glob.glob("*.info")
num_infofiles = len(dirlist)

# Only call make_regfile.c if we can unambiguously determine the
# name of the bead position file.  There should be one position file
# and one info file (with the same name) in the directory.  If more
# are present, the directory was not cleaned up properly after the
# last run.
# 
if num_infofiles == 2:
    n = 0
    for dir in dirlist:
        n += 1
        if n == 1:
            nth = "1st"
        elif n == 2:
            nth = "2nd"
        else:
            nth = str(n)
        position_filename = re.search("(.+).info", dir).group(1)
        print "the " + nth + " reg file name is: " + position_filename
        sys.stdout.flush()
        print "the total number of files are: " + str(num_infofiles)
        sys.stdout.flush()
        exec_string = "%(working_dir)s/make_regfile %(position_filename)s %(num_fcs)s" % vars()
        print "EXECUTING:\t" + exec_string
        sys.stdout.flush()
        os.system(exec_string)

elif num_infofiles == 1:
    if re.search("(.+).info", dirlist[0]):
        position_filename = re.search("(.+).info", dirlist[0]).group(1)
        exec_string = "%(working_dir)s/make_regfile %(position_filename)s %(num_fcs)s" % vars()
        print "EXECUTING:\t" + exec_string
        sys.stdout.flush()
        os.system(exec_string)
else:
    print >> sys.stderr, ("ERROR:\tNo file in the directory matches the expected pattern (*.info)")
    print >> sys.stderr, ("\tinitialize_processor.c must have failed unexpectedly.")
    print >> sys.stderr, ("\tExiting, pipeline not initialized.")
    proc.close()
    sys.stdout.flush()
    sys.stderr.flush()
    sys.exit()
    
print "initialize_processor.py exiting w/ return value of " + str(num_fcs)
sys.stdout.flush()
num_fcs_file = open("NUMBER_OF_FLOWCELLS.dat", 'w')
print >> num_fcs_file, str(num_fcs)
sys.stdout.flush()
num_fcs_file.close()
proc.close()
exit(str(num_fcs))
