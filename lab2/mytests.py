from __future__ import print_function

import sys

sys.path.append('..')

from trans import Trans

import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import os


def main():
    
    
    tester = Trans()
    
    #Basic Tests
    
    tester.run(3000, 0, "test.txt", False)
    tester.run(3000, .1, "test.txt", False)
    tester.run(3000, .2, "test.txt", False)
    tester.run(3000, .5, "test.txt", False)
    
    
    tester.run(10000, 0, "internet-architecture.pdf", False)
    tester.run(10000, .1, "internet-architecture.pdf", False)

    #Fast Retransmit

    tester.run(10000, 0, "internet-architecture.pdf", True)
    tester.run(10000, .2, "internet-architecture.pdf", True)
    tester.run(10000, .2, "internet-architecture.pdf", False)


    #Experiments

    data = []
    time = tester.run(1000, 0, "internet-architecture.pdf", False)
    data.append((1000, time))
    time = tester.run(2000, 0, "internet-architecture.pdf", False)
    data.append((2000, time))
    time = tester.run(5000, 0, "internet-architecture.pdf", False)
    data.append((5000, time))
    time = tester.run(10000, 0, "internet-architecture.pdf", False)
    data.append((10000, time))
    time = tester.run(15000, 0, "internet-architecture.pdf", False)
    data.append((15000, time))
    time = tester.run(20000, 0, "internet-architecture.pdf", False)
    data.append((20000, time))



    df = pd.DataFrame(data = data, columns=['Window Size', 'Time']).sort_values(by=['Window Size', 'Time'], ascending=[True, True])
    plt.figure()

    ax = df.plot(x="Window Size",y="Time", color="green", label="Experimental")

    ax.set_ylabel("Time (s)")
    ax.set_xlabel("Window Size")
    fig = ax.get_figure()
    fig.savefig('window_size.png')









if __name__ == '__main__':
    main()
