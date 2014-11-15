import xbee


class Node(xbee.ZigBee):
    """Class that represents an XBee series 2 wireless node."""

    node_types = {'ms': 'coordinator',
                  'es': 'environmental sensor',
                  'ls': 'light switch',
                  'pl': 'plug level sensor'}

    def __init__(self, source_addr_long, name):
        self.name = name
        self.source_addr_long = source_addr_long

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
