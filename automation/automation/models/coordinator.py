import logging
import time
import xbee

from .node import Node
from .packet import Packet


class Coordinator(xbee.ZigBee):
    """The XBee Series 2 wireless coordinator."""

    NAME = 'ms'

    def actuate(self, node):
        if node.type != Node.node_types['ac']:
            # Don't do anything if this is not an actuation node.
            logging.warning("noop, %s, not an actuation node", node)
            return

        if node.relay_circuit_closed:
            self.remote_at(node.source_addr_long, command=node.actuate_pin,
                           parameter=Node.RELAY_OPEN_PARAM)
        else:
            self.remote_at(node.source_addr_long, command=node.actuate_pin,
                           parameter=Node.RELAY_CLOSED_PARAM)

    def discover_nodes(self, discover_time):
        """Discover nodes on network for `time` secs."""
        # Set node discover time to FF; send node discover from self.
        self.send('at', frame='A', command='NT', parameter='\xFF')
        self.at(command='ND')

        nodes = {}  # source_addr_long: node object, includes self.
        future = time.time() + discover_time
        while time.time() < future:
            response = self.wait_read_frame()
            logging.debug(response)
            if ('command' not in response) or (response['command'] != 'ND'):
                continue

            source_addr_long = response['parameter']['source_addr_long']
            if source_addr_long not in nodes:
                name = response['parameter']['node_identifier']
                if name == self.NAME:
                    nodes[source_addr_long] = self
                else:
                    nodes[source_addr_long] = Node(source_addr_long, name)

        logging.debug(nodes)
        return nodes

    def receive_sensor_data(self, receive_time):
        """Recieve sensor data."""
        responses = []
        future = time.time() + receive_time
        while time.time() < future:
            packet = Packet(self.wait_read_frame())
            logging.debug(packet)
            responses.append(packet)
        return responses
