#!/usr/bin/python
"""
Call this to generate a .beads file for the basecaller which is a 4-color
composite from a single ligation cycle.  This is used to determine which beads
are amplified and which are not.

Execute as ./makePrimerFile.py cyclename

Written in Perl by Greg Porreca (Church Lab) 11-10-2008
Translated to Python by David Kalish 11-29-2010

 
NOTE: fix for dual-flowcell by removing flowcellnum arg and auto-determine how
many flowcells' worth of data are present.
"""

import glob
import re
import sys
import os

dirlist = glob.glob("*.info")
if not dirlist:
    print 'ERROR:\tThere are no ".info" files.'
    sys.exit(1)
num_infofiles = len(dirlist)

if num_infofiles > 2:
    print "ERROR:\tthere are %(num_infofiles)s possible input files, and I don't know which to use:" % vars()
    for i in xrange(num_infofiles):
        print "\t" + dirlist[i]
elif re.search("(.+).info", dirlist[0]):
    dirlist0 = dirlist[0]
    argv0 = sys.argv[1]
    exec_string = "./makePrimerFile %(dirlist0)s 0 %(argv0)s" % vars()
    print "EXECUTING:\t" + exec_string
    os.system(exec_string)
else: pass
