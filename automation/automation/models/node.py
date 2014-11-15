from itertools import count
import logging


class Node(object):
    """Class that represents an XBee series 2 wireless node."""

    ACTUATE_PIN = 'D4'
    _ids = count(0)

    node_types = {'ms': 'coordinator',
                  'ac': 'actuator',
                  'es': 'environmental sensor',
                  'ls': 'light switch',
                  'pl': 'plug level sensor'}

    def __init__(self, source_addr_long, name):
        self.id = self._ids.next()
        self.name = name
        self.source_addr_long = source_addr_long
        if self.type == self.node_types['ac']:
            self.actuate_pin = self.ACTUATE_PIN

    def __str__(self):
        return "%s: %s, %s, %s, %s" % (self.name, self.type, self.building,
                                       self.floor, self.room)

    def __repr__(self):
        return self.__str__()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        """Parse name and set all attrs to the appropriate info."""
        if not name:
            return

        self._name = name
        node = self.parse_name(name)
        for key in node:
            setattr(self, key, node[key])

    def actuate(self, coordinator):
        """Toggle the device connected to this node."""
        if self.type != self.node_types['ac']:
            # Don't do anything if this is not an actuation node.
            logging.warning("noop, %s, not an actuation node", self)
            return

        coordinator.remote_at(self.source_addr_long, command=self.actuate_pin,
                              parameter='\x05')

    @classmethod
    def parse_name(cls, name):
        """Parse node names according to API contract.

        This script parses node names and returns the type of sensor and the
        location data (building, floor, room). The API contract exists here:
        https://github.com/rgardner/extreme-design/wiki/Naming-Protocol

        """
        node = {}
        if name[0:2] not in cls.node_types:
            raise ValueError('Invalid name: unrecognized node type')

        node['type'] = cls.node_types[name[0:2]]  # first two chars
        node['building'] = name[2:6]              # next four chars
        node['floor'] = name[6:8]                 # next two chars
        node['room'] = name[8:]                   # the rest of the string

        return node
