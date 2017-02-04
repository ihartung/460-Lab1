from __future__ import print_function

import sys

sys.path.append('..')

from src.sim import Sim
from src.packet import Packet

from networks.network import Network

import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = []

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

class DelayHandler(object):
    @staticmethod
    def receive_packet(packet):
        global data
        data.append((Sim.scheduler.current_time(),
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
    global data
    data = []
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
    df = pd.DataFrame(data = data, columns=['Simulator Time', 'Packet Ident', 'Packet Create', 'Packet Time to Creation', 'Packet Transmission Delay', 'Packet Propagation Delay', 'Packet Queueing Delay'])
    df.to_csv('results/two_nodes_1.csv', index=True, header=True)
    ## Part 2

    print("PART 2")

    # parameters
    data = []
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
    df = pd.DataFrame(data = data, columns=['Simulator Time', 'Packet Ident', 'Packet Create', 'Packet Time to Creation', 'Packet Transmission Delay', 'Packet Propagation Delay', 'Packet Queueing Delay'])
    df.to_csv('results/two_nodes_2_0.csv', index=True, header=True)

    ## Part 3

    print("PART 3")

    # parameters
    data = []
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
    df = pd.DataFrame(data = data, columns=['Simulator Time', 'Packet Ident', 'Packet Create', 'Packet Time to Creation', 'Packet Transmission Delay', 'Packet Propagation Delay', 'Packet Queueing Delay'])
    df.to_csv('results/two_nodes_3_0.csv', index=True, header=True)

    ####################
    print("THREE NODES")

    ## Part 1

    print("PART 1")

    # parameters
    data = []
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
    net.nodes['n3'].add_protocol(protocol="delay", handler=d)

    # send 1MB

    for i in range(0, 8000000/8000):
        p = Packet(destination_address=n3.get_address('n2'), ident=i + 1, protocol='delay', length=1000)
        transmissionDelay = 8000 / n1.links[0].bandwidth
        calculatedDelay = i * transmissionDelay
        Sim.scheduler.add(delay=calculatedDelay, event=p, handler=n1.send_packet)

    # Sim.set_debug("Node")

    # run the simulation
    Sim.scheduler.run()
    df = pd.DataFrame(data = data, columns=['Simulator Time', 'Packet Ident', 'Packet Create', 'Packet Time to Creation', 'Packet Transmission Delay', 'Packet Propagation Delay', 'Packet Queueing Delay'])
    df.to_csv('results/three_nodes_1.csv', index=True, header=True)

    ## Part 2

    print("PART 2")

    # parameters
    data = []
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
    df = pd.DataFrame(data = data, columns=['Simulator Time', 'Packet Ident', 'Packet Create', 'Packet Time to Creation', 'Packet Transmission Delay', 'Packet Propagation Delay', 'Packet Queueing Delay'])
    df.to_csv('results/two_nodes_2.csv', index=True, header=True)

    ## Part 3

    print("PART 3")

    # parameters
    data = []
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
    net.nodes['n3'].add_protocol(protocol="delay", handler=d)

    # send 1MB

    for i in range(0, 8000000//8000):
        p = Packet(destination_address=n3.get_address('n2'), ident=i + 1, protocol='delay', length=8000)
        transmissionDelay = 8000 // n1.links[0].bandwidth
        calculatedDelay = i * transmissionDelay
        Sim.scheduler.add(delay=calculatedDelay, event=p, handler=n1.send_packet)

    # Sim.set_debug("Node")

    # run the simulation
    Sim.scheduler.run()
    df = pd.DataFrame(data = data, columns=['Simulator Time', 'Packet Ident', 'Packet Create', 'Packet Time to Creation', 'Packet Transmission Delay', 'Packet Propagation Delay', 'Packet Queueing Delay'])
    df.to_csv('results/two_nodes_3.csv', index=True, header=True)

    ####################
    print("QUEUEING DELAY")

    # parameters
    data = []
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
    df = pd.DataFrame(data = data, columns=['Simulator Time', 'Packet Ident', 'Packet Create', 'Packet Time to Creation', 'Packet Transmission Delay', 'Packet Propagation Delay', 'Packet Queueing Delay'])
    df.to_csv('results/10.csv', index=True, header=True)

    print("20% LOAD")
    data = []
    Sim.scheduler.reset()
    # setup packet generator
    destination = n2.get_address('n1')
    max_rate = n1.links[0].bandwidth // (1000 * 8)
    load = 0.2 * max_rate
    g = Generator(node=n1, destination=destination, load=load, duration=10)
    Sim.scheduler.add(delay=0, event='generate', handler=g.handle)

    # run the simulation
    Sim.scheduler.run()
    df = pd.DataFrame(data = data, columns=['Simulator Time', 'Packet Ident', 'Packet Create', 'Packet Time to Creation', 'Packet Transmission Delay', 'Packet Propagation Delay', 'Packet Queueing Delay'])
    df.to_csv('results/20.csv', index=True, header=True)

    print("30% LOAD")
    data = []
    Sim.scheduler.reset()
    # setup packet generator
    destination = n2.get_address('n1')
    max_rate = n1.links[0].bandwidth // (1000 * 8)
    load = 0.3 * max_rate
    g = Generator(node=n1, destination=destination, load=load, duration=10)
    Sim.scheduler.add(delay=0, event='generate', handler=g.handle)

    # run the simulation
    Sim.scheduler.run()
    df = pd.DataFrame(data = data, columns=['Simulator Time', 'Packet Ident', 'Packet Create', 'Packet Time to Creation', 'Packet Transmission Delay', 'Packet Propagation Delay', 'Packet Queueing Delay'])
    df.to_csv('results/30.csv', index=True, header=True)

    print("40% LOAD")
    data = []
    Sim.scheduler.reset()
    # setup packet generator
    destination = n2.get_address('n1')
    max_rate = n1.links[0].bandwidth // (1000 * 8)
    load = 0.4 * max_rate
    g = Generator(node=n1, destination=destination, load=load, duration=10)
    Sim.scheduler.add(delay=0, event='generate', handler=g.handle)

    # run the simulation
    Sim.scheduler.run()
    df = pd.DataFrame(data = data, columns=['Simulator Time', 'Packet Ident', 'Packet Create', 'Packet Time to Creation', 'Packet Transmission Delay', 'Packet Propagation Delay', 'Packet Queueing Delay'])
    df.to_csv('results/40.csv', index=True, header=True)

    print("50% LOAD")
    data = []
    Sim.scheduler.reset()
    # setup packet generator
    destination = n2.get_address('n1')
    max_rate = n1.links[0].bandwidth // (1000 * 8)
    load = 0.5 * max_rate
    g = Generator(node=n1, destination=destination, load=load, duration=10)
    Sim.scheduler.add(delay=0, event='generate', handler=g.handle)

    # run the simulation
    Sim.scheduler.run()
    df = pd.DataFrame(data = data, columns=['Simulator Time', 'Packet Ident', 'Packet Create', 'Packet Time to Creation', 'Packet Transmission Delay', 'Packet Propagation Delay', 'Packet Queueing Delay'])
    df.to_csv('results/50.csv', index=True, header=True)

    print("60% LOAD")
    data = []
    Sim.scheduler.reset()
    # setup packet generator
    destination = n2.get_address('n1')
    max_rate = n1.links[0].bandwidth // (1000 * 8)
    load = 0.6 * max_rate
    g = Generator(node=n1, destination=destination, load=load, duration=10)
    Sim.scheduler.add(delay=0, event='generate', handler=g.handle)

    # run the simulation
    Sim.scheduler.run()
    df = pd.DataFrame(data = data, columns=['Simulator Time', 'Packet Ident', 'Packet Create', 'Packet Time to Creation', 'Packet Transmission Delay', 'Packet Propagation Delay', 'Packet Queueing Delay'])
    df.to_csv('results/60.csv', index=True, header=True)

    print("70% LOAD")
    data = []
    Sim.scheduler.reset()
    # setup packet generator
    destination = n2.get_address('n1')
    max_rate = n1.links[0].bandwidth // (1000 * 8)
    load = 0.7 * max_rate
    g = Generator(node=n1, destination=destination, load=load, duration=10)
    Sim.scheduler.add(delay=0, event='generate', handler=g.handle)

    # run the simulation
    Sim.scheduler.run()
    df = pd.DataFrame(data = data, columns=['Simulator Time', 'Packet Ident', 'Packet Create', 'Packet Time to Creation', 'Packet Transmission Delay', 'Packet Propagation Delay', 'Packet Queueing Delay'])
    df.to_csv('results/70.csv', index=True, header=True)

    print("80% LOAD")
    data = []
    Sim.scheduler.reset()
    # setup packet generator
    destination = n2.get_address('n1')
    max_rate = n1.links[0].bandwidth // (1000 * 8)
    load = 0.8 * max_rate
    g = Generator(node=n1, destination=destination, load=load, duration=10)
    Sim.scheduler.add(delay=0, event='generate', handler=g.handle)

    # run the simulation
    Sim.scheduler.run()
    df = pd.DataFrame(data = data, columns=['Simulator Time', 'Packet Ident', 'Packet Create', 'Packet Time to Creation', 'Packet Transmission Delay', 'Packet Propagation Delay', 'Packet Queueing Delay'])
    df.to_csv('results/80.csv', index=True, header=True)

    print("90% LOAD")
    data = []
    Sim.scheduler.reset()
    # setup packet generator
    destination = n2.get_address('n1')
    max_rate = n1.links[0].bandwidth // (1000 * 8)
    load = 0.9 * max_rate
    g = Generator(node=n1, destination=destination, load=load, duration=10)
    Sim.scheduler.add(delay=0, event='generate', handler=g.handle)

    # run the simulation
    Sim.scheduler.run()
    df = pd.DataFrame(data = data, columns=['Simulator Time', 'Packet Ident', 'Packet Create', 'Packet Time to Creation', 'Packet Transmission Delay', 'Packet Propagation Delay', 'Packet Queueing Delay'])
    df.to_csv('results/90.csv', index=True, header=True)

    print("95% LOAD")
    data = []
    Sim.scheduler.reset()
    # setup packet generator
    destination = n2.get_address('n1')
    max_rate = n1.links[0].bandwidth // (1000 * 8)
    load = 0.95 * max_rate
    g = Generator(node=n1, destination=destination, load=load, duration=10)
    Sim.scheduler.add(delay=0, event='generate', handler=g.handle)

    # run the simulation
    Sim.scheduler.run()
    df = pd.DataFrame(data = data, columns=['Simulator Time', 'Packet Ident', 'Packet Create', 'Packet Time to Creation', 'Packet Transmission Delay', 'Packet Propagation Delay', 'Packet Queueing Delay'])
    df.to_csv('results/95.csv', index=True, header=True)

    print("98% LOAD")
    data = []
    Sim.scheduler.reset()
    # setup packet generator
    destination = n2.get_address('n1')
    max_rate = n1.links[0].bandwidth // (1000 * 8)
    load = 0.98 * max_rate
    g = Generator(node=n1, destination=destination, load=load, duration=10)
    Sim.scheduler.add(delay=0, event='generate', handler=g.handle)

    # run the simulation
    Sim.scheduler.run()
    df = pd.DataFrame(data = data, columns=['Simulator Time', 'Packet Ident', 'Packet Create', 'Packet Time to Creation', 'Packet Transmission Delay', 'Packet Propagation Delay', 'Packet Queueing Delay'])
    df.to_csv('results/98.csv', index=True, header=True)

    queueing_delay = []
    df = pd.read_csv('results/10.csv')
    queueing_delay.append((.10, df["Packet Queueing Delay"].mean()))
    df = pd.read_csv('results/20.csv')
    queueing_delay.append((.20, df["Packet Queueing Delay"].mean()))
    df = pd.read_csv('results/30.csv')
    queueing_delay.append((.30, df["Packet Queueing Delay"].mean()))
    df = pd.read_csv('results/40.csv')
    queueing_delay.append((.40, df["Packet Queueing Delay"].mean()))
    df = pd.read_csv('results/50.csv')
    queueing_delay.append((.50, df["Packet Queueing Delay"].mean()))
    df = pd.read_csv('results/60.csv')
    queueing_delay.append((.60, df["Packet Queueing Delay"].mean()))
    df = pd.read_csv('results/70.csv')
    queueing_delay.append((.70, df["Packet Queueing Delay"].mean()))
    df = pd.read_csv('results/80.csv')
    queueing_delay.append((.80, df["Packet Queueing Delay"].mean()))
    df = pd.read_csv('results/90.csv')
    queueing_delay.append((.90, df["Packet Queueing Delay"].mean()))
    df = pd.read_csv('results/95.csv')
    queueing_delay.append((.95, df["Packet Queueing Delay"].mean()))
    df = pd.read_csv('results/98.csv')
    queueing_delay.append((.98, df["Packet Queueing Delay"].mean()))

    df = pd.DataFrame(data = queueing_delay, columns=['Utilization', 'Avg Packet Queueing Delay'])
    df.to_csv('results/average_queueing_delay.csv', index=True, header=True)

    service = (1000.0*8)/1000000
    mu = 1.0/service
    rho = np.arange(0,1,1.0/100)
    values = (1/(2*mu))*(rho/(1-rho))
    plt.figure()

    df = pd.DataFrame(data = zip(rho, values), columns=['Utilization', 'Theoretical Queueing Delay'])
    ax = df.plot(x="Utilization",y="Theoretical Queueing Delay", color="green")

    df = pd.read_csv('results/average_queueing_delay.csv')
    df.plot(x="Utilization",y="Avg Packet Queueing Delay", ax=ax)

    ax.set_xlabel("Utilization")
    ax.set_ylabel("Queueing Delay")
    fig = ax.get_figure()
    fig.savefig('results/queueing_delay.png')

if __name__ == '__main__':
    main()
