from __future__ import print_function

import sys

sys.path.append('..')

from trans import Trans

import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def main():
    
    
    tester = Trans()
    
    tester.run(3000, 0, "test.txt")
    tester.run(3000, .1, "test.txt")
    tester.run(3000, .2, "test.txt")
    tester.run(3000, .5, "test.txt")
    
    
    tester.run(10000, 0, "internet-architecture.pdf")
    tester.run(10000, .1, "internet-architecture.pdf")






if __name__ == '__main__':
    main()
