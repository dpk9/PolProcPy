#!/usr/bin/python

import os
import sys

Argv = sys.argv
del Argv[0]

cw = os.getcwd()
os.environ['MATLABPATH'] = cw
os.environ['LIBXCB_ALLOW_SLOPPY_LOCK'] = "1"

Argv0 = Argv[0]
Argv1 = Argv[1]
Argv2 = Argv[2]
cmd = "./run_disp_tetra.sh /opt/MATLAB/MATLAB_Component_Runtime/v77/ %(Argv0)s %(Argv1)s %(Argv2)s" % vars()
print cmd
os.system(cmd)

"""Commented lines in the original Perl file"""
#open(OUTFILE, ">disp_tetra.m");
#open(TEMPL, "disp_tetra.mtemplate");
#
#print OUTFILE "filename = '$ARGV[0]';\n";
#print OUTFILE "frame = $ARGV[1];\n";
#print OUTFILE "outputfilename = '$ARGV[2]';\n";
#
#while(<TEMPL>){
#    print OUTFILE "$_";
#}
#close OUTFILE;
#close TEMPL;
#
#system "matlab -display :1 -nosplash -r disp_tetra";


