#!/usr/bin/python

import commands

proc_array = commands.getoutput("ps -Afl")
num_procs = len(proc_array)

for i in xrange(num_procs):
    curr_proc = proc_array[i].split("\t")
    print curr_proc