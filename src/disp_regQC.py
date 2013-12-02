#!/usr/bin/python

#------------------------------------------
# Done, except for line 11.
#------------------------------------------

import sys
import os

#cw = getcwd
#$ENV{'MATLABPATH'} = $cw;

argv = sys.argv
del argv[0]


mlarg1 = "logs/0_" + argv[0] + "_A.register-log"; # RED
mlarg2 = "logs/0_" + argv[0] + "_C.register-log"; # GREEN
mlarg3 = "logs/0_" + argv[0] + "_G.register-log"; # BLUE
mlarg4 = "logs/0_" + argv[0] + "_T.register-log"; # BLACK
mlarg5 = argv[0]

os.system("./run_disp_regQC.sh /opt/MATLAB/MATLAB_Component_Runtime/v77/ %(mlarg1)s %(mlarg2)s %(mlarg3)s %(mlarg4)s %(mlarg5)s" % vars())
