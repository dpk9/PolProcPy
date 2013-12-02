#!/usr/bin/python

"""
Used to generate a binary 'image' of all objects used for registration of
a given array position.  Object locations are from the reg file.  Execute
as:
./pull_regpoints.py a b c > image_filename
where:
  a = the flowcell number ([0..1])
  b = the array number    ([0..17])
  c = the image number    ([0..IMGS_PER_ARRAY])

Written in Perl by Greg Porreca (Church Lab) 12-14-2007
Translated to Python by David Kalish 11-30-2010
"""

import sys
import glob
import numpy

num_arrays = 8
num_imgs = 2180
reg_pixels = 20000

fc = sys.argv[1]
array = sys.argv[2]
img = sys.argv[3]

image = list()

print >> stderr, "Seeking to position %(fc)s %(array)s %(img)s: " %vars()

# DETERMINE REG FILENAME
array = glob.glob("*.info")
num_files = len(array)

if re.search("(.+)\.info", array[0]):
    one = re.search("(.+)\.info", array[0]).group(1)
    regfn = str(one) + ".reg"

REG = open(regfn,'rb')

index = ((reg_pixels * img * 4) + (array * num_imgs * reg_pixels * 4) +
         (fc * num_arrays * num_imgs * reg_pixels * 4))

print >> stderr, "byte %(index)s..." %vars()

REG.seek(index, 0)

# INITIALIZE IMAGE
image = zeros((1000,1000), dtype=int)
    
# SET REG PIXELS TO 1
string = ""
for i in xrange(reg_pixels):
    buffer = REG.read(4)
    line0, line1 = struct.unpack('HH', buffer)
    image[line0,line1] = 1
for i in xrange(1000):
    for j in xrange(1000):
        string = string + str(arr.item(j,i)) + "\t"
print string

REG.close()