#!/usr/bin/python

import sys

# the expected[] array defines the expected sequences in the readfile
score = {}
expected = {}
expected[0] = "AAAAAA"
expected[1] = "CCCCCC"
expected[2] = "GGGGGG"
expected[3] = "TTTTTT"
expected_length = len(expected[0])

Argv = sys.argv
Argv0 = Argv[1]
#Argv0 = "Argv0"
deltafilename = "tetrahedra/%(Argv0)s.delta" % vars()
try:
    DELTAFILE = open(deltafilename, 'r')
except IOError:
    sys.exit("ERROR opening delta file " + deltafilename)

curr_array = -1

for Line in DELTAFILE.readlines():
    Line = Line.rstrip()
    line = Line.split("\t")
    
    # Open new read file if we're on a new array (each array has its own read file)
    if line[1] != curr_array:
        curr_array = line[1]
        line0 = line[0]
        readfilename = "output_data/%(Argv0)s_%(line0)s_%(curr_array)02d.basecalls" % vars()
        try:
            READFILE = open(readfilename, 'r')
        except IOERROR:
            sys.exit("ERROR opening read file " + readfilename)
            
    # Now load in the delta values for the current array position
    curr_img = line[2]
    num_deltas = len(line)-3
    i = 0
    while i < num_deltas:
        mean_deltas[i/4] = line[i+3]
        mean_deltas[i/4] += line[i+4]
        mean_deltas[i/4] += line[i+5]
        mean_deltas[i/4] += line[i+6]
        mean_deltas[i/4] = mean_deltas[i/4] / 4
        mean_deltas[i/4] = int(mean_deltas[i/4] * 1000)
        i += 4
    
    delta_mean = 0
    while i < expected_length:
        delta_mean += mean_deltas[i]
        i += 1
    delta_mean /= expected_length
    
    correct = {}
    incorrect = {}
    total = {}
    accuracy = {}
    for n in xrange(num_deltas/4):
        correct[n] = 0
        incorrect[n] = 0
        total[n] = 0
    
    # Now, iterate over the current image in the readfile
    for curr_read in READFILE.readlines():
        curr_read.rstrip()
        readline = curr_read.split("\t")
        # Have we reached the next image?
        if readline[2] != curr_img:
            READFILE.seek(((-1)*len(curr_read))-1, 1) #move file pointer back this line (plus newline)
            break
        
        # If not, is this a 'bad' bead
        elif "." in readline[4]: pass
        
        # If not, compute error rates
        else:
            # first, determine what the read 'should' be; compare it to each of
            # the expected sequences, and pick the one it's closest to; if it is
            # equally close to 2 sequences, mark it as '='
            read = readline[4]
            for i in xrange(expected_length):
                score[i] = 0
                for j in xrange(num_deltas/4):
                    expectedi = expected[i]
                    if read[j] == expectedi[j]:
                        score[i] += 1
            
            best_match = "."
            best_score = 0
            for i in xrange(expected_length):
                if score[i] > best_score:
                    best_score = score[i]
                    best_match = expected[i]
                elif score[i] == best_score:
                    best_match = "="
        
            # now, output each basecall, what we think it should be, its quality
            # and delta score, and whether it's correct (+), incorrect (-), or 
            # incorrect because we don't know what the call should be (/)
            for i in xrange(num_deltas/4):
#            for i in xrange(6,21):
                r = read[i]
                if best_match == "=":
                    b = "." # b is the basecall; '.' means the correct basecall is ambiguous
                    c = "/" # c is a code that describes whether the basecall is correct, incorrect, or ambiguous
                else:
                    b = best_match[i]
                    if r == b: c = "+"
                    else: c = "-"
#                    print "$readline[0]\t$readline[1]\t$readline[2]\t$readline[3]\t$best_score\t$i\t$r\t$b\t$c\t$readline[$i+5]\t$mean_deltas[$i]\n";
                if x == "+":
                    correct[i] += 1
#                    total[i] += 1
                else: #incorrect and ambiguous basecalls are considered errors
                    incorrect[i] += 1
#                    total[i] += 1
                total[i] += 1
    """
    end "for curr_read in READFILE.readlines():"
    """

    for i in xrange(num_deltas/4):
        if total[i] > 0:
            accuracy[i] = correct[i]/total[i]
        else:
            accuracy[i] = 0
            total[i] = 0
        if total[i] == 1:
            accuracy[i] = 0
            total[i] = 0
            correct[i] = 0
        accuracyi = accuracy[i]
        deltai = mean_deltas[i]
        accuracy_str = "%(accuracyi)0.5f" % vars()
        delta_str = "%(deltai)0.f" % vars()
        line0,line1,line2,correcti,incorrecti,totali = line[0],line[1],line[2],correct[i],incorrect[i],total[i]
        print "%(line0)s\t%(line1)s\t%(line2)s\t%(i)s\t%(accuracy_str)s\t%(delta_str)s\t%(correcti)s\t%(incorrecti)s\t%(totali)"%vars()
        sys.stdout.flush()
"""
end 'for Line in DELTAFILE.readlines():"
"""
