import logging
import threading

from .models import Packet


class Consumer(threading.Thread):
    """The meat and potatoes

    Handles the various types of packets.

    """
    def __init__(self, packet_queue):
        self.packet_queue = packet_queue

    def run(self):
        while True:
            frame = self.packet_queue.get()
            packet = Packet(frame)

            if packet.type == Packet.NODE_ID_INDICATOR:
                logging.debug("nd response packet found.")
                self.handle_node_id_packet(packet)

            elif packet.type == Packet.RX_IO_DATA_LONG_ADDR:
                logging.debug("rx io data packet found.")
                self.handle_rx_io_data_packet(packet)

            elif packet.type == Packet.TX_STATUS:
                logging.debug("tx status packet found.")
                self.handle_tx_status(packet)

            elif packet.type == Packet.UNDETERMINED:
                logging.debug("could not determine type of packet: %s", packet)
                self.handle_undetermined(packet)

    @classmethod
    def handle_node_id_packet(packet):
        nodes_lock = threading.Lock()
        with nodes_lock:
            pass

    @classmethod
    def handle_rx_io_data_packet(cls, packet):
        pass

    @classmethod
    def handle_tx_status(cls, packet):
        pass

    @classmethod
    def handle_undetermined(cls, packet):
        pass
