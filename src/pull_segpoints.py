#!/usr/bin/python

"""
Used to generate a binary 'image' of all objects at some array
position.  Object locations are from the location file.  Execute
as:
./pull_segpoints.py a b c > image_filename
where:
  a = the flowcell number ([0..1])
  b = the array number    ([0..17])
  c = the image number    ([0..IMGS_PER_ARRAY])

Written in Perl by Greg Porreca (Church Lab) 12-14-2007
Translated to Python by David Kalish 11-30-2010
"""

import sys
import numpy
import glob
import re
import struct

num_arrays = 8
num_imgs = 2180
reg_pixels = 2000
num_args = len(sys.argv())-1

if num_args < 3:
    print >> stderr, "ERROR:\tMust call as ./pull_segpoints fcnum arraynum imgnum %(num_args)s" %vars()

fc = sys.argv(1)
array = sys.argv(2)
img = sys.argv(3)

# OUTPUT WILL BE BINARY IMAGE W/ 1s AT BEAD PIXELS
image = numpy.zeros((1000,1000), dtype = int)

print >> stderr, "Seeking to position %(fc)s %(array)s %(img)s..." %vars()

# DETERMINE INFO AND SEG FILENAMES
array = glob.glob("*.info")
num_files = len(array)

if re.search("(.+)\.info$", array[0]):
    segfn = re.search("(.+)\.info$", array[0]).group(1)
INFO = open(array[0],'rb')
SEG = open(segfn,'rb')

# LOOK FOR CORRECT RECORD IN INFO FILE
index = 0
while found != 1:
    buffer = INFO.read(8)
    line0,line1,line2,line3 = struct.unpack('HHHH', buffer)
    if line0 == fc and line1 == array and line2 == img:
        index += 20
        num_objs = line3
        found = 1
    else:
        index += 20 + (line3 * 4) + 2
        
# NOW GO THERE IN THE SEGFILE AND READ THE VALUES
SEG.seek(index, 0)
for i in xrange(num_objs):
    buffer = SEG.read(4)
    line0,line1 = unpack('HH', buffer)
    if line0 > 1000 or line1 > 1000:
        sys.exit("POSITION ERROR")
    image[line0, line1] = 1

# OUTPUT IMAGE
string  = ""
for i in xrange(1000):
    for j in xrange(1000):
        string = string + str(image.item(j,i)) + "\t"

SEG.close()
INFO.close()
