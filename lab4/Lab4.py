from __future__ import print_function

import sys

sys.path.append('..')

from src.sim import Sim
from src.packet import Packet
from lab4.dvrouting import DvroutingApp
from lab4.broadcast import BroadcastApp

from networks.network import Network


class BroadcastApp(object):
    def __init__(self, node):
        self.node = node

    def receive_packet(self, packet):
        print(Sim.scheduler.current_time(), self.node.hostname, packet.ident)

def p_setup(nodey):
    b = BroadcastApp(nodey)
    dv = DvroutingApp(nodey)
    nodey.add_protocol(protocol="broadcast", handler=b)
    nodey.add_protocol(protocol="dvrouting", handler=dv)



def exp1():
    # parameters
    Sim.scheduler.reset()
    Sim.set_debug(True)

    # setup network
    net = Network('../networks/l4e1.txt')

    # get nodes
    n1 = net.get_node('n1')
    n2 = net.get_node('n2')
    n3 = net.get_node('n3')
    n4 = net.get_node('n4')
    n5 = net.get_node('n5')

    # setup broadcast application
    p_setup(n1)
    p_setup(n2)
    p_setup(n3)
    p_setup(n4)
    p_setup(n5)


    # send a broadcast packet from 1 with TTL 2, so everyone should get it
    p = Packet(
        source_address=n1.get_address('n2'),
        destination_address=0,
        ident=1, ttl=2, protocol='broadcast', length=100)
    Sim.scheduler.add(delay=0, event=p, handler=n1.send_packet)

    # send a broadcast packet from 1 with TTL 1, so just nodes 2 and 3
    # should get it
    p = Packet(
        source_address=n1.get_address('n2'),
        destination_address=0,
        ident=2, ttl=1, protocol='broadcast', length=100)
    Sim.scheduler.add(delay=1, event=p, handler=n1.send_packet)

    # send a broadcast packet from 3 with TTL 1, so just nodes 1, 4, and 5
    # should get it
    p = Packet(
        source_address=n3.get_address('n1'),
        destination_address=0,
        ident=3, ttl=1, protocol='broadcast', length=100)
    Sim.scheduler.add(delay=2, event=p, handler=n3.send_packet)

    # run the simulation
    Sim.scheduler.run()

    def exp2():
    # parameters
    Sim.scheduler.reset()
    Sim.set_debug(True)

    # setup network
    net = Network('../networks/l4e2.txt')

    # get nodes
    n1 = net.get_node('n1')
    n2 = net.get_node('n2')
    n3 = net.get_node('n3')
    n4 = net.get_node('n4')
    n5 = net.get_node('n5')

    # setup broadcast application
    p_setup(n1)
    p_setup(n2)
    p_setup(n3)
    p_setup(n4)
    p_setup(n5)


    # send a broadcast packet from 1 with TTL 2, so everyone should get it
    p = Packet(
        source_address=n1.get_address('n2'),
        destination_address=0,
        ident=1, ttl=2, protocol='broadcast', length=100)
    Sim.scheduler.add(delay=0, event=p, handler=n1.send_packet)

    # send a broadcast packet from 1 with TTL 1, so just nodes 2 and 3
    # should get it
    p = Packet(
        source_address=n1.get_address('n2'),
        destination_address=0,
        ident=2, ttl=1, protocol='broadcast', length=100)
    Sim.scheduler.add(delay=1, event=p, handler=n1.send_packet)

    # send a broadcast packet from 3 with TTL 1, so just nodes 1, 4, and 5
    # should get it
    p = Packet(
        source_address=n3.get_address('n1'),
        destination_address=0,
        ident=3, ttl=1, protocol='broadcast', length=100)
    Sim.scheduler.add(delay=2, event=p, handler=n3.send_packet)

    # run the simulation
    Sim.scheduler.run()

    def exp3():
    # parameters
    Sim.scheduler.reset()
    Sim.set_debug(True)

    # setup network
    net = Network('../networks/l4e3.txt')

    # get nodes
    n1 = net.get_node('n1')
    n2 = net.get_node('n2')
    n3 = net.get_node('n3')
    n4 = net.get_node('n4')
    n5 = net.get_node('n5')
    n6 = net.get_node('n6')
    n7 = net.get_node('n7')
    n8 = net.get_node('n8')
    n9 = net.get_node('n9')
    n10 = net.get_node('n10')
    n11 = net.get_node('n11')
    n12 = net.get_node('n12')
    n13 = net.get_node('n13')
    n14 = net.get_node('n14')
    n15 = net.get_node('n15')

    # setup broadcast application
    p_setup(n1)
    p_setup(n2)
    p_setup(n3)
    p_setup(n4)
    p_setup(n5)
    p_setup(n6)
    p_setup(n7)
    p_setup(n8)
    p_setup(n9)
    p_setup(n10)
    p_setup(n11)
    p_setup(n12)
    p_setup(n13)
    p_setup(n14)
    p_setup(n15)


    # send a broadcast packet from 1 with TTL 2, so everyone should get it
    p = Packet(
        source_address=n1.get_address('n2'),
        destination_address=0,
        ident=1, ttl=2, protocol='broadcast', length=100)
    Sim.scheduler.add(delay=0, event=p, handler=n1.send_packet)

    # send a broadcast packet from 1 with TTL 1, so just nodes 2 and 3
    # should get it
    p = Packet(
        source_address=n1.get_address('n2'),
        destination_address=0,
        ident=2, ttl=1, protocol='broadcast', length=100)
    Sim.scheduler.add(delay=1, event=p, handler=n1.send_packet)

    # send a broadcast packet from 3 with TTL 1, so just nodes 1, 4, and 5
    # should get it
    p = Packet(
        source_address=n3.get_address('n1'),
        destination_address=0,
        ident=3, ttl=1, protocol='broadcast', length=100)
    Sim.scheduler.add(delay=2, event=p, handler=n3.send_packet)

    # run the simulation
    Sim.scheduler.run()

    def main():
        exp1()
        exp2()
        exp3()

if __name__ == '__main__':
    main()
