from __future__ import print_function

import sys

sys.path.append('..')

from src.sim import Sim
from src.packet import Packet

from networks.network import Network

import random

class Generator(object):
    def __init__(self, node, destination, load, duration):
        self.node = node
        self.load = load
        self.destination = destination
        self.duration = duration
        self.start = 0
        self.ident = 1

    def handle(self, event):
        # quit if done
        now = Sim.scheduler.current_time()
        if (now - self.start) > self.duration:
            return

        # generate a packet
        self.ident += 1
        p = Packet(destination_address=self.destination, ident=self.ident, protocol='delay', length=1000)
        Sim.scheduler.add(delay=0, event=p, handler=self.node.send_packet)
        # schedule the next time we should generate a packet
        Sim.scheduler.add(delay=random.expovariate(self.load), event='generate', handler=self.handle)

class NormalHandler(object):
    @staticmethod
    def receive_packet(packet):
        print((Sim.scheduler.current_time(),
               packet.ident,
               packet.created,
               Sim.scheduler.current_time() - packet.created,
               packet.transmission_delay,
               packet.propagation_delay,
               packet.queueing_delay))

class LastHandler(object):
    @staticmethod
    def receive_packet(packet):
        if packet.ident == 1000:
            print((Sim.scheduler.current_time(),
                   packet.ident,
                   packet.created,
                   Sim.scheduler.current_time() - packet.created,
                   packet.transmission_delay,
                   packet.propagation_delay,
                   packet.queueing_delay))

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
    n = NormalHandler()
    net.nodes['n2'].add_protocol(protocol="delay", handler=n)

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
    n = NormalHandler()
    net.nodes['n2'].add_protocol(protocol="delay", handler=n)

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
    n = NormalHandler()
    net.nodes['n2'].add_protocol(protocol="delay", handler=n)

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
    b = LastHandler()
    net.nodes['n3'].add_protocol(protocol="delay", handler=b)

    # send 1MB

    for i in range(0, 8000000/8000):
        p = Packet(destination_address=n3.get_address('n2'), ident=i + 1, protocol='delay', length=1000)
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
    b = LastHandler()
    net.nodes['n3'].add_protocol(protocol="delay", handler=b)

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
    b = LastHandler()
    net.nodes['n3'].add_protocol(protocol="delay", handler=b)

    # send 1MB

    for i in range(0, 8000000//8000):
        p = Packet(destination_address=n3.get_address('n2'), ident=i + 1, protocol='delay', length=8000)
        transmissionDelay = 8000 // n1.links[0].bandwidth
        calculatedDelay = i * transmissionDelay
        Sim.scheduler.add(delay=calculatedDelay, event=p, handler=n1.send_packet)

    # Sim.set_debug("Node")

    # run the simulation
    Sim.scheduler.run()

    ####################
    print("QUEUEING DELAY")

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

    print("10% LOAD")
    # setup packet generator
    destination = n2.get_address('n1')
    max_rate = n1.links[0].bandwidth // (1000 * 8)
    load = 0.1 * max_rate
    g = Generator(node=n1, destination=destination, load=load, duration=10)
    Sim.scheduler.add(delay=0, event='generate', handler=g.handle)

    # run the simulation
    Sim.scheduler.run()

    print("20% LOAD")
    Sim.scheduler.reset()
    # setup packet generator
    destination = n2.get_address('n1')
    max_rate = n1.links[0].bandwidth // (1000 * 8)
    load = 0.2 * max_rate
    g = Generator(node=n1, destination=destination, load=load, duration=10)
    Sim.scheduler.add(delay=0, event='generate', handler=g.handle)

    # run the simulation
    Sim.scheduler.run()

    print("30% LOAD")
    Sim.scheduler.reset()
    # setup packet generator
    destination = n2.get_address('n1')
    max_rate = n1.links[0].bandwidth // (1000 * 8)
    load = 0.3 * max_rate
    g = Generator(node=n1, destination=destination, load=load, duration=10)
    Sim.scheduler.add(delay=0, event='generate', handler=g.handle)

    # run the simulation
    Sim.scheduler.run()

    print("40% LOAD")
    Sim.scheduler.reset()
    # setup packet generator
    destination = n2.get_address('n1')
    max_rate = n1.links[0].bandwidth // (1000 * 8)
    load = 0.4 * max_rate
    g = Generator(node=n1, destination=destination, load=load, duration=10)
    Sim.scheduler.add(delay=0, event='generate', handler=g.handle)

    # run the simulation
    Sim.scheduler.run()

    print("50% LOAD")
    Sim.scheduler.reset()
    # setup packet generator
    destination = n2.get_address('n1')
    max_rate = n1.links[0].bandwidth // (1000 * 8)
    load = 0.5 * max_rate
    g = Generator(node=n1, destination=destination, load=load, duration=10)
    Sim.scheduler.add(delay=0, event='generate', handler=g.handle)

    # run the simulation
    Sim.scheduler.run()

    print("60% LOAD")
    Sim.scheduler.reset()
    # setup packet generator
    destination = n2.get_address('n1')
    max_rate = n1.links[0].bandwidth // (1000 * 8)
    load = 0.6 * max_rate
    g = Generator(node=n1, destination=destination, load=load, duration=10)
    Sim.scheduler.add(delay=0, event='generate', handler=g.handle)

    # run the simulation
    Sim.scheduler.run()

    print("70% LOAD")
    Sim.scheduler.reset()
    # setup packet generator
    destination = n2.get_address('n1')
    max_rate = n1.links[0].bandwidth // (1000 * 8)
    load = 0.7 * max_rate
    g = Generator(node=n1, destination=destination, load=load, duration=10)
    Sim.scheduler.add(delay=0, event='generate', handler=g.handle)

    # run the simulation
    Sim.scheduler.run()

    print("80% LOAD")
    Sim.scheduler.reset()
    # setup packet generator
    destination = n2.get_address('n1')
    max_rate = n1.links[0].bandwidth // (1000 * 8)
    load = 0.8 * max_rate
    g = Generator(node=n1, destination=destination, load=load, duration=10)
    Sim.scheduler.add(delay=0, event='generate', handler=g.handle)

    # run the simulation
    Sim.scheduler.run()

    print("90% LOAD")
    Sim.scheduler.reset()
    # setup packet generator
    destination = n2.get_address('n1')
    max_rate = n1.links[0].bandwidth // (1000 * 8)
    load = 0.9 * max_rate
    g = Generator(node=n1, destination=destination, load=load, duration=10)
    Sim.scheduler.add(delay=0, event='generate', handler=g.handle)

    # run the simulation
    Sim.scheduler.run()

    print("95% LOAD")
    Sim.scheduler.reset()
    # setup packet generator
    destination = n2.get_address('n1')
    max_rate = n1.links[0].bandwidth // (1000 * 8)
    load = 0.95 * max_rate
    g = Generator(node=n1, destination=destination, load=load, duration=10)
    Sim.scheduler.add(delay=0, event='generate', handler=g.handle)

    # run the simulation
    Sim.scheduler.run()

    print("98% LOAD")
    Sim.scheduler.reset()
    # setup packet generator
    destination = n2.get_address('n1')
    max_rate = n1.links[0].bandwidth // (1000 * 8)
    load = 0.98 * max_rate
    g = Generator(node=n1, destination=destination, load=load, duration=10)
    Sim.scheduler.add(delay=0, event='generate', handler=g.handle)

    # run the simulation
    Sim.scheduler.run()

if __name__ == '__main__':
    main()
