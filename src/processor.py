#!/usr/bin/python
#
# processor.py
#
# Execute this perl script to start the image processing pipeline.
# Initialize_processor must have already been run for this to work.
#
# Written by Greg Porreca (Church Lab) 01-23-2008
# Translated from Perl to Python by David Kalish 11-12-2010

import os
import sys
import commands
import glob
import re

ACQUISITION_NAME = "acq"
current_dir = os.getcwd()

# first, make sure there isn't another processor.py or processor
# process running; if so, display information and exit.
#
running_processes1 = commands.getoutput("ps -C processor -o pid=")
running_processes2 = commands.getoutput("ps -C processor.py -o pid=")

if len(running_processes1) > 1 or len(running_processes2) > 1:
    len1 = str(len(running_processes1))
    len2 = str(len(running_processes2))
    print >> sys.stderr, "ERROR:\tThere are " + len1 + ' instances of "processor",'
    print >> sys.stderr, "\tand " + len2 + ' instances of "processor.py" running,'
    os.system("ps -flC processor")
    os.system("ps -flC processor.py")
    sys.exit()

dirlist = glob.glob("*.info")
num_infofiles = len(dirlist)

# Only call processor.c if we can unambiguously determine the
# name of the bead position file.  There should be one position file
# and one info file (with the same name) in the directory.  If more
# are present, the directory was not cleaned up properly after the
# last run.
# 
if num_infofiles < 3:
    if re.search("(.+).info", dirlist[0]):
        position_filename = re.search("(.+).info", dirlist[0]).group(1)
        try:
            NUM_FCS = open("NUMBER_OF_FLOWCELLS.dat")
            num_fcs = NUM_FCS.readline().strip()
            NUM_FCS.close()

            exec_string = "%(current_dir)s/processor %(ACQUISITION_NAME)s %(position_filename)s %(num_fcs)s" % vars()
            print "EXECUTING:\t" + exec_string
            os.system(exec_string)
        except IOError:
            print >> sys.stderr, "ERROR:\tCould not find file \"NUMBER_OF_FLOWCELLS.dat\""
            sys.exit(1)
    else:
        print >> sys.stderr, "ERROR:\tThere are more that 2 .info files."
        print >> sys.stderr, "\tTerminating program (*.info);"
        exit()
