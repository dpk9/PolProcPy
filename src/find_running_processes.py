#!/usr/bin/python

##############
# Done
##############


import re
import os
import commands

STATUS_FILE = open("/home/polonator/PROCESS_STATUS", 'w')

PS = commands.getoutput("ps aux")
for line in PS:
    line = line.strip("\n")
    if re.search(".+ (.+)/processor acq", line) != None:
        found = re.search(".+ (.+)/processor acq", line).group(1)
        print ("PROCESSOR PROCESS RUNNING: " + found)
        STATUS_FILE.write("P " + found)
        
    if re.search(".+ (.+)/initialize_processor acq", line) != None:
        found = re.search(".+ (.+)/initialize_processor acq", line).group(1)
        print ("INITIALIZE_PROCESSOR PROCESS RUNNING: " + found)
        STATUS_FILE.write("I " + found)
        
    if re.search(".+ (.+)/make_regfile", line) != None:
        found = re.search(".+ (.+)/make_regfile", line).group(1)
        print ("MAKE_REGFILE PROCESS RUNNING: " + found)
        STATUS_FILE.write("R " + found)

STATUS_FILE.close()
