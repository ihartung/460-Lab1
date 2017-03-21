from .buffer import SendBuffer, ReceiveBuffer
from .connection import Connection
from .sim import Sim
from .tcppacket import TCPPacket
class TCP(Connection):
    """ A TCP connection between two hosts."""

    def __init__(self, transport, source_address, source_port,
                 destination_address, destination_port, app=None, drop=[]):
        Connection.__init__(self, transport, source_address, source_port, destination_address, destination_port, app)

        # -- Sender functionality

        # maximum segment size, in bytes
        self.mss = 1000
        # send window; represents the total number of bytes that may
        # be outstanding at one time
        self.window = self.mss
        # send buffer
        self.send_buffer = SendBuffer()
        # largest sequence number that has been ACKed so far; represents
        # the next sequence number the client expects to receive
        self.sequence = 0
        # plot sequence numbers
        self.plot_sequence_header()
        # packets to drop
        self.drop = drop
        self.dropped = []
        self.timer = None
        # retransmission timer
        # timeout duration in seconds
        self.timeout = 1
        self.threshold = 100000
        self.additiveIncrease = False
        self.increment = 0

        # -- Receiver functionality

        # receive buffer
        self.receive_buffer = ReceiveBuffer()
        # ack number to send; represents the largest in-order sequence
        # number not yet received
        self.ack = 0

    def trace(self, message):
        """ Print debugging messages. """
        Sim.trace("TCP", message)

    def plot_sequence_header(self):
        if self.node.hostname =='n1':
            Sim.plot('sequence.csv','Time,Sequence Number,Event\n')

    def plot_sequence(self,sequence,event):
        if self.node.hostname =='n1':
            Sim.plot('sequence.csv','%s,%s,%s\n' % (Sim.scheduler.current_time(),sequence,event))

    def plot_congestion_window_header(self):
        if self.node.hostname =='n1':
            Sim.plot('congestion-window.csv','Time,Size\n')

    def plot_congestion_window(self,size):
        if self.node.hostname =='n1':
            Sim.plot('congestion-window.csv','%s,%s\n' % (Sim.scheduler.current_time(),size))

    def receive_packet(self, packet):
        """ Receive a packet from the network layer. """
        if packet.ack_number > 0:
            # handle ACK
            self.handle_ack(packet)
        if packet.length > 0:
            # handle data
            self.handle_data(packet)

    ''' Sender '''

    def send(self, data):

        self.send_buffer.put(data)

        if not self.timer:
        # set a timer
            self.timer = Sim.scheduler.add(delay=self.timeout, event='retransmit', handler=self.retransmit)

        while (self.send_buffer.outstanding() < self.window):
            size = self.mss
            d, s = self.send_buffer.get(size);
            self.send_packet(d, s)
            if not self.send_buffer.available():
                return

    def send_packet(self, data, sequence):
        packet = TCPPacket(source_address=self.source_address,
                           source_port=self.source_port,
                           destination_address=self.destination_address,
                           destination_port=self.destination_port,
                           body=data,
                           sequence=sequence, ack_number=self.ack)
        if sequence in self.drop and not sequence in self.dropped:
            self.dropped.append(sequence)
            self.plot_sequence(sequence,'drop')
            self.trace("%s (%d) dropping TCP segment to %d for %d" % (
                self.node.hostname, self.source_address, self.destination_address, packet.sequence))
            return

        # send the packet
        self.plot_sequence(sequence,'send')
        self.trace("%s (%d) sending TCP segment to %d for %d" % (
            self.node.hostname, self.source_address, self.destination_address, packet.sequence))
        self.transport.send_packet(packet)

        # set a timer
        if not self.timer:
            self.timer = Sim.scheduler.add(delay=self.timeout, event='retransmit', handler=self.retransmit)

    def handle_ack(self, packet):
        """ Handle an incoming ACK. """
        self.plot_sequence(packet.ack_number - 1000,'ack')
        self.trace("%s (%d) received ACK from %d for %d" % (
            self.node.hostname, packet.destination_address, packet.source_address, packet.ack_number))
        self.cancel_timer()
        if self.sequence >= packet.ack_number:
            return

        # Fast Restransmit
        if packet.ack_number == self.sequence:
            self.repeat = self.repeat + 1
        else:
            self.repeat   = 1
            self.sequence = packet.ack_number
            bytesReceived = packet.ack_number - self.sequence
            if self.additiveIncrease:
                # Once cwnd is larger than the threshold, use additive increase. Every time the sender receives an ACK for new data, increment cwnd by MSS*b/cwnd, where MSS is the maximum segment size (1000 bytes) and b is the number of new bytes acknowledged.
                self.increment += (self.mss * bytesReceived / self.window)
                if self.increment > self.mss:
                    self.window += self.increment/self.mss * self.mss
                    self.increment -= self.increment/self.mss * self.mss
	    else:
                # Every time the sender receives an ACK for new data, increment cwnd by the number of new bytes of data acknowledged.Never increment cwnd by more than one MSS.
                #self.window += min(bytesReceived, self.mss)
		self.window += bytesReceived
                if self.window > self.threshold:
                    # Stop slow start when cwnd exceeds or equals the threshold
                    self.additiveIncrease = True


            self.send_buffer.slide(packet.ack_number)

        if self.repeat == 4:
            # A loss event is detected when there are three duplicate ACKs (meaning the fourth ACK in a row for the same sequence number), and TCP immediately retransmits instead of waiting for the retransmission timer.
            self.trace("fast_restransmit.  seq = %d" % (self.sequence))
            self.retransmit()
	    return

        # self.sequence = packet.ack_number
        # self.send_buffer.slide(packet.ack_number)
        self.timer = Sim.scheduler.add(delay=self.timeout, event='retransmit', handler=self.retransmit)
        while (self.send_buffer.outstanding() < self.window):
            size = self.mss
            d, s = self.send_buffer.get(size);
            self.send_packet(d, s)
            if not self.send_buffer.available():
                return
        if self.send_buffer.outstanding() == 0 and self.send_buffer.available() == 0:
            return
        size = self.mss
    def retransmit(self, event):
        # When a loss event is detected (a timeout or 3 duplicate ACKs), then set the threshold to max(cwnd/2,MSS) and set cwnd to 1 MSS.
        halfCWND = self.window/2
        halfCWND = (halfCWND-(halfCWND % self.mss))
        self.threshold = max(halfCWND, self.mss)
        self.window = self.mss
        self.increment = 0
	self.additiveIncrease = False

        d, s = self.send_buffer.resend(size)
        self.send_packet(d, s)
        self.timer = Sim.scheduler.add(delay=self.timeout, event='retransmit', handler=self.retransmit)
    def cancel_timer(self):
        """ Cancel the timer. """
        if not self.timer:
            return
        Sim.scheduler.cancel(self.timer)
        self.timer = None
    ''' Receiver '''

    def handle_data(self, packet):
        """ Handle incoming data. This code currently gives all data to
            the application, regardless of whether it is in order, and sends
        self.trace("%s (%d) received TCP segment from %d for %d" % (
            an ACK."""
        self.trace("%s (%d) received TCP segment from %d for %d" % (self.node.hostname, packet.destination_address, packet.source_address, packet.sequence))
        d, s = self.receive_buffer.get()
        self.app.receive_data(d)
        self.ack = len(d) + s
        self.trace("Sending this ack from handle data: %d" % (self.ack))
        self.send_ack()
    def send_ack(self):
        """ Send an ack. """
        packet = TCPPacket(source_address=self.source_address,
                           source_port=self.source_port,
                           destination_address=self.destination_address,
                           destination_port=self.destination_port,
                           sequence=self.sequence, ack_number=self.ack)
        # send the packet
        self.trace("%s (%d) sending TCP ACK to %d for %d" % (
            self.node.hostname, self.source_address, self.destination_address, packet.ack_number))
        self.transport.send_packet(packet)
