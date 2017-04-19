

class DvroutingApp(object):
    def __init__(self, node):
        self.node = node
        self.dv   = {}

    def receive_packet(self, packet):
        print(Sim.scheduler.current_time(), self.node.hostname, packet.ident)


