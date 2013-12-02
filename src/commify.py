#!/bin/env python

import re
regex = re.compile(r'^(-?\d+)(\d{3})')

def commify(num, separator=','):
    """commify(num, separator) -> string

    Return a string representing the number num with separator inserted
    for every power of 1000.   Separator defaults to a comma.
    E.g., commify(1234567) -> '1,234,567'
    """
    num = str(num)  # just in case we were passed a numeric value
    more_to_do = 1
    while more_to_do:
        (num, more_to_do) = regex.subn(r'\1%s\2' % separator,num)
    return num

if __name__ == '__main__':

    test_vals = (12345,
                 -12345,
                 1234567,
                 -1234567,
                 1234567.89,
                 -1234567.89,
                 1234567.8901,
                 -1234567.8901)

    print "If you use '.' as your decimal indicator..."
    for number in test_vals:
        print commify(number)


    weirdo_test_vals = ('12345',
                 '-12345',
                 '1234567',
                 '-1234567',
                 '1234567,89',
                 '-1234567,89',
                 '1234567,8901',
                 '-1234567,8901')

    print "If you use ',' as your decimal indicator..."
    for number in weirdo_test_vals:
        print commify(number,'.')
