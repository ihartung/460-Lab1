from .sim import Sim

class DvroutingApp(object):
    def __init__(self, node):
        self.node = node
        self.dv   = {}
        self.dv[self.node.get_address(self.node.hostname)] = 0
        Sim.scheduler.add(delay=1, event=p, handler=self.gossip)

    def update(self, key, value):
    	self.dv[key] = value
    	self.node.delete_forwarding_entry(key)
    	self.node.add_forwarding_entry(key, self.node.get_link(key))

    def receive_packet(self, packet):
        print(Sim.scheduler.current_time(), self.node.hostname, packet.ident)
        link = self.node.
        neighbor_dv = packet.body
        for key in neighbor_dv
        	n = (neighbor_dv[key] + 1)
        	if key in self.dv.keys():
        		if n < self.dv[key]:
        			update(key, n)
    		else:
    			update(key, n)



    def gossip():
    	#make packet with dv in it.
    	p = Packet(
        source_address=n1.get_address('n2'),
        destination_address=0,
        ident=0, ttl=1, protocol='dvrouting', body=dv)
    	Sim.scheduler.add(delay=1, event=p, handler=self.node.send_packet)



