#!/usr/bin/env python
# coding:utf-8
"""Script entry."""

import sys
import process


if __name__ == '__main__':
    if len(sys.argv) == 4:
        process.process(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print 'Args:'
        print '\ttargetpath:target file path.'
        print '\tstorepath:store file path.'
        print '\tinterval:interval'
