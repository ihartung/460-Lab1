from __future__ import print_function

import sys

sys.path.append('..')

from tahoe import Trans

import os


def main():

    tester = Trans()

    # tester.run("internet-architecture.pdf", [])
    # tester.run("internet-architecture.pdf", [14000])
    # tester.run("internet-architecture.pdf", [14000,28000])
    tester.run("internet-architecture.pdf", [14000,26000,28000])

if __name__ == '__main__':
    main()
