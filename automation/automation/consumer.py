import logging
import multiprocessing

from .models import Packet


class Consumer(multiprocessing.Process):
    """The meat and potatoes

    Handles the various types of packets.

    """

    def __init__(self, frame_queue, nodes):
        self.logger = logging.getLogger(self.name)
        self.frame_queue = frame_queue
        self.nodes = nodes

    def run(self):
        while True:
            frame = self.frame_queue.get()
            packet = Packet(frame)

            if packet.type == Packet.NODE_ID_INDICATOR:
                self.logger.debug("nd response packet found.")
                self.handle_node_id_packet(packet)

            elif packet.type == Packet.RX_IO_DATA_LONG_ADDR:
                self.logger.debug("rx io data packet found.")
                self.handle_rx_io_data_packet(packet)

            elif packet.type == Packet.TX_STATUS:
                self.logger.debug("tx status packet found.")
                self.handle_tx_status(packet)

            elif packet.type == Packet.UNDETERMINED:
                self.logger.debug("could not determine type of packet: %s",
                                  packet)
                self.handle_undetermined(packet)

            self.frame_queue.task_done()

    @classmethod
    def handle_node_id_packet(packet):
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
