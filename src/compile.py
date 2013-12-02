#!/usr/bin/python

import os
import sys

argv = sys.argv
del argv[0]
num_args = len(argv)
if(num_args<1):
    wd = os.getcwd() + "/src"

else:
    wd = str(argv[0]) + "/src"
print "Compiling directory " + wd + "..."

print "Building processor..."
os.system("g++ -O3 -fexpensive-optimizations -funroll-loops -o " + wd + "/../processor " + wd + "/processor.c " + wd + "/ProcessImage.c " + wd + "/ProcessImage_register.c " + wd + "/ProcessImage_extract.c " + wd + "/ReceiveData.c " + wd + "/ReceiveFilename.c " + wd + "/ReceiveFCNum.c " + wd + "/GetSock.c " + wd + "/Polonator_logger.c")

print "Building initialize_processor..."
os.system("g++ -O3 -funroll-loops -Wno-deprecated -o " + wd + "/../initialize_processor " + wd + "/initialize_processor.c " + wd + "/ReceiveInitData.c " + wd + "/ReceiveFilename.c " + wd + "/ReceiveFCNum.c " + wd + "/GetSock.c " + wd + "/find_objects.c " + wd + "/img_tools.c " + wd + "/Polonator_logger.c")

print "Building make_regfile..."
os.system("g++ -O3 -fexpensive-optimizations -o " + wd + "/../make_regfile " + wd + "/MakeRegfile.c " + wd + "/Polonator_logger.c")

print "Building Basecaller..."
os.system( "g++ -O3 -funroll-loops -o " + wd + "/../basecaller " + wd + "/Basecaller.c " + wd + "/Polonator_logger.c")
#os.system( "g++ -o " + wd + "/../basecaller " + wd + "/Basecaller.c " + wd + "/Polonator_logger.c -g -pg")

os.system("g++ -O3 -o " + wd + "/../histogram " + wd + "/Histogram.c")
os.system("g++ -O3 -o " + wd + "/../histogram4 " + wd + "/Histogram4.c")
os.system("g++ -O3 -o " + wd + "/../makePrimerFile " + wd + "/MakePrimerFile.c")
