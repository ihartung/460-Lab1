from __future__ import print_function

import sys

sys.path.append('..')

from tahoe import Trans

import os


def main():

    tester = Trans()

    tester.run("internet-architecture.pdf", [])
    # tester.run("internet-architecture.pdf", [15])
    # tester.run("internet-architecture.pdf", [15,29])
    # tester.run("internet-architecture.pdf", [15,27,29])

if __name__ == '__main__':
    main()
