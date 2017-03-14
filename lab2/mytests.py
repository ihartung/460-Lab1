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
    
    #Basic Tests
    
    #tester.run(3000, 0, "test.txt", False)
    #tester.run(3000, .1, "test.txt", False)
    #tester.run(3000, .2, "test.txt", False)
    #tester.run(3000, .5, "test.txt", False)
    
    
    #tester.run(10000, 0, "internet-architecture.pdf", False)
    #tester.run(10000, .1, "internet-architecture.pdf", False)

    #Fast Retransmit

    tester.run(10000, 0, "internet-architecture.pdf", True)
    tester.run(10000, .2, "internet-architecture.pdf", True)
    tester.run(10000, .2, "internet-architecture.pdf", False)


    #Experiments


#   tester.run(1000, 0, "internet-architecture.pdf", False)
#   tester.run(2000, 0, "internet-architecture.pdf", False)
#   tester.run(5000, 0, "internet-architecture.pdf", False)
#   tester.run(10000, 0, "internet-architecture.pdf", False)
#    tester.run(15000, 0, "internet-architecture.pdf", False)
#    tester.run(20000, 0, "internet-architecture.pdf", False)









if __name__ == '__main__':
    main()
