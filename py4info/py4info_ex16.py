
'''
Python For Infomatics - Exercise 16

First Created: 2016-Apr-28
Last Updated: 2016-Apr-28
Python 2.7
Chris
'''

import os
import hashlib
from collections import defaultdict

def create_check_sum(filename):
    '''
    Reads a file and generates the checksum/hash
    '''
    fhand = open(filename,'r')
    data = fhand.read()
    fhand.close()
    return hashlib.md5(data).hexdigest()

def check_for_duplicate_files():
    '''
    Looks at all directories and subdirectories.
    For each text file it checks whether the size of file is the same, and/or
    the actual file is the same (by checksum/hashing).
    '''

    count = 0
    check_sums = defaultdict(list)
    file_sizes = defaultdict(list)

    for (dirname, dirs, files) in os.walk('.'):
        for filename in files:
            if filename.endswith('.txt'):
                file_path = os.path.join(dirname, filename)
                checksum = create_check_sum(file_path)
                filesize = os.path.getsize(file_path)

                if filesize in file_sizes:
                    print 'match file size', filename, file_sizes[filesize]

                if checksum in check_sums:
                    print 'chksum', filename, check_sums[checksum]

                file_sizes[filesize].append(filename)
                check_sums[checksum].append(filename)
                count += 1

    print '\nFiles:', count
    print '\n'
    for check_sum, filename in check_sums.iteritems():
        print check_sum, filename

    print '\n'

    for file_size, filename in file_sizes.iteritems():
        print file_size, filename

check_for_duplicate_files()
