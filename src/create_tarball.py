#!/usr/bin/python

import time
from glob import glob

d = time.localtime()[0:3]
year = d[0]
mon = d[1]
day = d[2]
datestamp = "%(day)s-%(mon)s-%(year)s" % vars()
print datestamp
tarfilename = "processor_pipeline_%(datestamp)s" % vars()

args = ["tar", "-cPvf", tarfilename]
#args.append("tar", "-cPvf", tarfilename)
for pl in glob("*.pl"): args.append(str(pl))
for py in glob("*.py"): args.append(str(py))
for mtemp in glob("*.mtemplate"): args.append(str(mtemp))
for G007 in glob("G007.positions*"): args.append(str(G007))
for item in ["src", "create_tarball.py", "GUI-data", "lib",
             "PolonatorProcessorControl.jar", "disp_cfd.m"]: args.append(item)
for ctf in glob("*.ctf"): args.append(str(ctf))
for sh in glob("*.sh"): args.append(str(sh))
for item in ["disp_regQC", "disp_delta", "disp_tetra", "display_objects",
            "display_color_raw", "disp_delta_mcr", "disp_regQC_mcr",
            "disp_tetra_mcr", "display_objects_mcr", "display_color_raw_mcr",
            "/home/polonator/NetBeansProjects"]: args.append(item)

print args