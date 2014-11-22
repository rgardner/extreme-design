import logging


class Server(object):
    """XBee Coordinator Server

    This class closely resembles the typical web server model, where the server
    lists for incoming connections and then creates new "worker" proccesses to
    handle the requests.

    """

    def __init__(self, coordinator, packet_queue):
        self.coordinator = coordinator
        self.logger = logging.getLogger('server')
        self.packet_queue = packet_queue

    def start(self, discover_time, should_save_data):
        self.logger.info("Listening for packets...")
        while True:
            frame = self.coordinator.wait_read_frame()
            self.packet_queue.put(frame)
