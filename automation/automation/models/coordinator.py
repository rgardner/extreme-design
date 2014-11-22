import xbee

from .node import Node


class Coordinator(xbee.ZigBee):
    """The XBee Series 2 wireless coordinator."""

    NAME = 'ms'

    def __init__(self, serial_port):
        super(Coordinator, self).__init__(serial_port)
        self.name = self.NAME

    def discover_nodes(self):
        """Send node discover command."""
        # Set node discover time to FF; send node discover from self.
        self.send('at', frame='A', command='NT', parameter='\xFF')
        self.at(command='ND')

    def toggle_node_relay(self, node):
        """Toggle the relay attached to the given node."""
        if node.relay_circuit_closed:
            self.remote_at(dest_addr_long=node.source_addr_long,
                           command=node.actuate_pin,
                           parameter=Node.RELAY_OPEN_PARAM)
        else:
            self.remote_at(dest_addr_long=node.source_addr_long,
                           command=node.actuate_pin,
                           parameter=Node.RELAY_CLOSED_PARAM)
