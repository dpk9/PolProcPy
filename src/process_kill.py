#!/usr/bin/python
"""
Kills acqiusition-associated processes running on either the acquisition
computer (by passing "acq" as the first argument) or the processing
computer (by passing "proc" as the argument).  If running on the acq, 
will execute the complete-scan routine after killing the processes.

Written by Greg Porreca (Church Lab) 08-08-2008
Translated to python by David Kalish 11-19-2010
"""

import subprocess
import re
import sys
import os

# These lists define the names of the processes to kill.  We iterate over this list,
# and for each entry, kill all running processes matching the current list element.
# Then, we re-call ps to get a new process list, and kill all processes matching the
# next element in the list
# Note the order below is important -- parents must be killed before children, since
# parents can spawn new children
#
#if($ARGV[0] eq "acq"){
#    @findcmd = ("polonator_main", "Polonator-stagealign", "Polonator-acquirer");
#    $acq=1;
#}
#elsif($ARGV[0] eq "proc"){
findcmd = ("perl ./initialize_processor", "initialize_processor", "perl ./processor", "processor")
#}

proclist = list()
for cmditem in findcmd:
    input, PS_F = os.popen2("ps -Af")
    PS_F.readline()
    for line in PS_F:
        proclist.append(line)
        for proc in proclist:
            procsplit = proc.split(None)
            pid = procsplit[1]
            command = procsplit[-1]
#            (user, pid, ppid, nice, stime, tty, rtime, command) = proc.split(None)
            command = command.rstrip()
            if re.search(cmditem, command):
                if acq == 1:
                    exec_cmd = "sudo kill " + str(pid)
                else:
                    exec_cmd = "kill " + str(pid)
                print exec_cmd
                os.system(exec_cmd)
    input.close()
    PS_F.close()
if len(sys.argv) > 1:
    if sys.argv[1] == "acq":
        exec_cmd = "/home/polonator/G.007/G.007_acquisition/PolonatorUtils complete-scan"
        print exec_cmd
        os.system(exec_cmd)
    
