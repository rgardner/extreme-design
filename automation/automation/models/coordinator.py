import logging
import time
import xbee

from .node import Node
from .packet import Packet


class Coordinator(xbee.ZigBee):
    """The XBee Series 2 wireless coordinator."""

    NAME = 'ms'

    def actuate(self, node):
        if node.relay_circuit_closed:
            self.remote_at(dest_addr_long=node.source_addr_long,
                           command=node.actuate_pin,
                           parameter=Node.RELAY_OPEN_PARAM)
        else:
            self.remote_at(dest_addr_long=node.source_addr_long,
                           command=node.actuate_pin,
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
            if ('command' not in response) or (response['command'] != 'ND'):
                # Not a node discovery response packet.
                logging.debug("non-nd response packet found: %s", response)
                continue

            logging.debug("nd response packet found: %s", response)
            source_addr_long = response['parameter']['source_addr_long']
            if source_addr_long not in nodes:
                name = response['parameter']['node_identifier']
                if name != self.NAME:
                    nodes[source_addr_long] = Node(source_addr_long, name)

        logging.debug("Coordinator discovered nodes: %s", nodes)
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
