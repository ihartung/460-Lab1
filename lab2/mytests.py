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

    file_size = os.path.getsize("internet-architecture.pdf")

    data = []
    time1 = tester.run(1000, 0, "internet-architecture.pdf", False)
    data.append((1000, file_size/time1))
    time2 = tester.run(2000, 0, "internet-architecture.pdf", False)
    data.append((2000, file_size/time2))
    time3 = tester.run(5000, 0, "internet-architecture.pdf", False)
    data.append((5000, file_size/time3))
    time4 = tester.run(10000, 0, "internet-architecture.pdf", False)
    data.append((10000, file_size/time4))
    time5 = tester.run(15000, 0, "internet-architecture.pdf", False)
    data.append((15000, file_size/time5))
    time6 = tester.run(20000, 0, "internet-architecture.pdf", False)
    data.append((20000, file_size/time6))

    segments = file_size / 1000
    data2 = []
    data2.append((1000, time1 - time6 / segments))
    data2.append((2000, time2 - time6 / segments))
    data2.append((5000, time3 - time6 / segments))
    data2.append((10000, time4 - time6 / segments))
    data2.append((15000, time5 - time6 / segments))
    data2.append((20000, time6 - time6 / segments))

    df = pd.DataFrame(data = data, columns=['Window Size', 'Throughput']).sort_values(by=['Window Size', 'Throughput'], ascending=[True, True])
    plt.figure()

    ax = df.plot(x="Window Size",y="Throughput", color="green", label="Experimental")

    ax.set_ylabel("Throughput")
    ax.set_xlabel("Window Size")
    fig = ax.get_figure()
    fig.savefig('window_size.png')

    df = pd.DataFrame(data = data, columns=['Window Size', 'Queueing Delay']).sort_values(by=['Window Size', 'Queueing Delay'], ascending=[True, True])
    plt.figure()

    ax = df.plot(x="Queueing Delay",y="Window Size", color="blue")

    ax.set_ylabel("Queueing Delay")
    ax.set_xlabel("Window Size")
    fig = ax.get_figure()
    fig.savefig('queueing_delay.png')








if __name__ == '__main__':
    main()
