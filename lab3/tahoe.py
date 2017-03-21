
from __future__ import print_function

import sys

sys.path.append('..')

from src.sim import Sim
from src.transport import Transport
from src.tcp_tahoe import TCP

from networks.network import Network

import optparse
import os
import subprocess


class AppHandler(object):
    def __init__(self, filename):
        self.filename = filename
        self.directory = 'received'
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        self.f = open(os.path.join(self.directory, self.filename), 'wb')

    def receive_data(self, data):
        Sim.trace('AppHandler', "application got %d bytes" % (len(data)))
        self.f.write(data)
        self.f.flush()


class Trans(object):
    def __init__(self):
        self.directory = 'received'

    def diff(self):
        args = ['diff', '-u', self.filename, os.path.join(self.directory, self.filename)]
        result = subprocess.Popen(args, stdout=subprocess.PIPE).communicate()[0]
        print()
        if not result:
            print("File transfer correct!")
        else:
            print("File transfer failed. Here is the diff:")
            print()
            print(result)

    def run(self, fila, drop):

        self.filename = fila
        fast = True
        Sim.trace('Trans', "It is %s that I am using drop transmit." % (fast))

        # parameters
        Sim.scheduler.reset()
        Sim.set_debug('AppHandler')
        Sim.set_debug('TCP')
        Sim.set_debug('Trans')

        # setup network
        net = Network('./network.txt')


        # setup routes
        n1 = net.get_node('n1')
        n2 = net.get_node('n2')
        net.set_queue(n1.links[0], "100")
        net.set_queue(n2.links[0], "100")

        n1.add_forwarding_entry(address=n2.get_address('n1'), link=n1.links[0])
        n2.add_forwarding_entry(address=n1.get_address('n2'), link=n2.links[0])

        # setup transport
        t1 = Transport(n1)
        t2 = Transport(n2)

        # setup application
        a = AppHandler(self.filename)

        # setup connection
        c1 = TCP(t1, n1.get_address('n2'), 1, n2.get_address('n1'), 1, a, drop)
        c2 = TCP(t2, n2.get_address('n1'), 1, n1.get_address('n2'), 1, a, drop)

        # send a file
        with open(self.filename, 'rb') as f:
            while True:
                data = f.read(1000)
                if not data:
                    break
                Sim.scheduler.add(delay=0, event=data, handler=c1.send)

        # run the simulation
        Sim.scheduler.run()

        self.diff()

        self.filename = None

        return Sim.scheduler.current_time()


if __name__ == '__main__':
    m = Main()
