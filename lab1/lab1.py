from __future__ import print_function

import sys

sys.path.append('..')

from src.sim import Sim
from src.packet import Packet

from networks.network import Network


class DelayHandler(object):
    @staticmethod
    def receive_packet(packet):
        print((Sim.scheduler.current_time(),
               packet.ident,
               packet.created,
               Sim.scheduler.current_time() - packet.created,
               packet.transmission_delay,
               packet.propagation_delay,
               packet.queueing_delay))


def main():

    ####################
    print("TWO NODES")

    ## Part 1

    print("PART 1")

    # parameters
    Sim.scheduler.reset()

    # setup network
    net = Network('networks/two_nodes_1.txt')

    # setup routes
    n1 = net.get_node('n1')
    n2 = net.get_node('n2')
    n1.add_forwarding_entry(address=n2.get_address('n1'), link=n1.links[0])
    n2.add_forwarding_entry(address=n1.get_address('n2'), link=n2.links[0])

    # setup app
    d = DelayHandler()
    net.nodes['n2'].add_protocol(protocol="delay", handler=d)

    # send one packet
    p = Packet(destination_address=n2.get_address('n1'), ident=1, protocol='delay', length=1000)
    Sim.scheduler.add(delay=0, event=p, handler=n1.send_packet)

    # run the simulation
    Sim.scheduler.run()

    ## Part 2

    print("PART 2")

    # parameters
    Sim.scheduler.reset()

    # setup network
    net = Network('networks/two_nodes_2.txt')

    # setup routes
    n1 = net.get_node('n1')
    n2 = net.get_node('n2')
    n1.add_forwarding_entry(address=n2.get_address('n1'), link=n1.links[0])
    n2.add_forwarding_entry(address=n1.get_address('n2'), link=n2.links[0])

    # setup app
    d = DelayHandler()
    net.nodes['n2'].add_protocol(protocol="delay", handler=d)

    # send one packet
    p = Packet(destination_address=n2.get_address('n1'), ident=1, protocol='delay', length=1000)
    Sim.scheduler.add(delay=0, event=p, handler=n1.send_packet)

    # run the simulation
    Sim.scheduler.run()

    ## Part 3

    print("PART 3")

    # parameters
    Sim.scheduler.reset()

    # setup network
    net = Network('networks/two_nodes_3.txt')

    # setup routes
    n1 = net.get_node('n1')
    n2 = net.get_node('n2')
    n1.add_forwarding_entry(address=n2.get_address('n1'), link=n1.links[0])
    n2.add_forwarding_entry(address=n1.get_address('n2'), link=n2.links[0])

    # setup app
    d = DelayHandler()
    net.nodes['n2'].add_protocol(protocol="delay", handler=d)

    # send one packet
    p = Packet(destination_address=n2.get_address('n1'), ident=1, protocol='delay', length=1000)
    Sim.scheduler.add(delay=0, event=p, handler=n1.send_packet)
    p = Packet(destination_address=n2.get_address('n1'), ident=2, protocol='delay', length=1000)
    Sim.scheduler.add(delay=0, event=p, handler=n1.send_packet)
    p = Packet(destination_address=n2.get_address('n1'), ident=3, protocol='delay', length=1000)
    Sim.scheduler.add(delay=0, event=p, handler=n1.send_packet)

    p = Packet(destination_address=n2.get_address('n1'), ident=4, protocol='delay', length=1000)
    Sim.scheduler.add(delay=2, event=p, handler=n1.send_packet)

    # run the simulation
    Sim.scheduler.run()

    ####################
    print("THREE NODES")

    ## Part 1

    print("PART 1")

    # parameters
    Sim.scheduler.reset()

    # setup network
    net = Network('networks/three_nodes_1.txt')

    # setup routes
    n1 = net.get_node('n1')
    n2 = net.get_node('n2')
    n3 = net.get_node('n3')
    n1.add_forwarding_entry(address=n2.get_address('n1'), link=n1.links[0])
    n1.add_forwarding_entry(address=n3.get_address('n2'), link=n1.links[0])
    n2.add_forwarding_entry(address=n1.get_address('n2'), link=n2.links[0])
    n2.add_forwarding_entry(address=n3.get_address('n2'), link=n2.links[1])
    n3.add_forwarding_entry(address=n2.get_address('n3'), link=n3.links[0])


    # setup app
    d = DelayHandler()
    # net.nodes['n2'].add_protocol(protocol="delay", handler=d)
    net.nodes['n3'].add_protocol(protocol="delay", handler=d)

    # send 1MB

    for i in range(0, 8000000/8000):
        p = Packet(destination_address=n3.get_address('n2'), ident=i + 1, protocol='delay', length=8000)
        transmissionDelay = 8000 / n1.links[0].bandwidth
        calculatedDelay = i * transmissionDelay
        Sim.scheduler.add(delay=calculatedDelay, event=p, handler=n1.send_packet)

    # Sim.set_debug("Node")

    # run the simulation
    Sim.scheduler.run()

    ## Part 2

    print("PART 2")

    # parameters
    Sim.scheduler.reset()

    # setup network
    net = Network('networks/three_nodes_2.txt')

    # setup routes
    n1 = net.get_node('n1')
    n2 = net.get_node('n2')
    n3 = net.get_node('n3')
    n1.add_forwarding_entry(address=n2.get_address('n1'), link=n1.links[0])
    n1.add_forwarding_entry(address=n3.get_address('n2'), link=n1.links[0])
    n2.add_forwarding_entry(address=n1.get_address('n2'), link=n2.links[0])
    n2.add_forwarding_entry(address=n3.get_address('n2'), link=n2.links[1])
    n3.add_forwarding_entry(address=n2.get_address('n3'), link=n3.links[0])


    # setup app
    d = DelayHandler()
    # net.nodes['n2'].add_protocol(protocol="delay", handler=d)
    net.nodes['n3'].add_protocol(protocol="delay", handler=d)

    # send 1MB

    for i in range(0, 8000000/8000):
        p = Packet(destination_address=n3.get_address('n2'), ident=i + 1, protocol='delay', length=8000)
        transmissionDelay = 8000 / n1.links[0].bandwidth
        calculatedDelay = i * transmissionDelay
        Sim.scheduler.add(delay=calculatedDelay, event=p, handler=n1.send_packet)

    # Sim.set_debug("Node")

    # run the simulation
    Sim.scheduler.run()

    ## Part 3

    print("PART 3")

    # parameters
    Sim.scheduler.reset()

    # setup network
    net = Network('networks/three_nodes_3.txt')

    # setup routes
    n1 = net.get_node('n1')
    n2 = net.get_node('n2')
    n3 = net.get_node('n3')
    n1.add_forwarding_entry(address=n2.get_address('n1'), link=n1.links[0])
    n1.add_forwarding_entry(address=n3.get_address('n2'), link=n1.links[0])
    n2.add_forwarding_entry(address=n1.get_address('n2'), link=n2.links[0])
    n2.add_forwarding_entry(address=n3.get_address('n2'), link=n2.links[1])
    n3.add_forwarding_entry(address=n2.get_address('n3'), link=n3.links[0])


    # setup app
    d = DelayHandler()
    # net.nodes['n2'].add_protocol(protocol="delay", handler=d)
    net.nodes['n3'].add_protocol(protocol="delay", handler=d)

    # send 1MB

    for i in range(0, 8000000/8000):
        p = Packet(destination_address=n3.get_address('n2'), ident=i + 1, protocol='delay', length=8000)
        transmissionDelay = 8000 / n1.links[0].bandwidth
        calculatedDelay = i * transmissionDelay
        Sim.scheduler.add(delay=calculatedDelay, event=p, handler=n1.send_packet)

    # Sim.set_debug("Node")

    # run the simulation
    Sim.scheduler.run()

if __name__ == '__main__':
    main()
