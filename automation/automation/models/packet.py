import logging
import time


class Packet(dict):
    """Dictionary wrapper for packet dictionary."""

    # Packet types.
    NODE_ID_INDICATOR = 'node_id_indicator'
    RX_IO_DATA_LONG_ADDR = 'rx_io_data_long_addr'
    TX_STATUS = 'tx_status'
    UNDETERMINED = 'undetermined'

    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)
        self['created_at'] = time.time()
        self.type = self.init_type()

    def init_type(self):
        """Determine the XBee packet type."""
        if self._is_node_id_indicator(self):
            return self.NODE_ID_INDICATOR

        if self._is_rx_io_data_long_addr(self):
            return self.RX_IO_DATA_LONG_ADDR

        if self._is_tx_status(self):
            return self.TX_STATUS

        logging.debug("Could not determine type of packet.")
        return self.UNDETERMINED

    def to_csv(self):
        """created_at,name,adc...,dio...,din"""
        created_at = self['created_at']
        name = self['source_addr_long'].__repr__()  # escape hex in string
        data = [0] * 12

        # Iterate over adc samples. (0 - 3)
        for i in range(3):
            key = "adc-{0}".format(i)
            if key in self['samples'][0]:
                data[i] = self['samples'][0][key]

        # Iterate over dio (1 - 7)
        for i in range(7):
            key = "dio-{0}".format(i)
            if key in self['samples'][0]:
                data[i] = self['samples'][0][key]

        # Add din
        if 'din' in self['samples'][0]:
            data[11] = self['samples'][0]['din']

        return "{0}, {1}, {2}".format(created_at, name, str(data).strip('[]'))

    @classmethod
    def _is_node_id_indicator(cls, packet):
        if ('command' in packet) and (packet['command'] == 'ND'):
            return True
        return False

    @classmethod
    def _is_rx_io_data_long_addr(packet):
        if ('id' in packet) and (packet['id'] == 'rx_io_data_long_addr'):
            return True
        return False

    @classmethod
    def _is_tx_status(packet):
        if ('id' in packet) and (packet['id'] == 'tx_status'):
            return True
        return False
