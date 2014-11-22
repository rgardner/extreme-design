import logging

import util
from .models import Coordinator


class Producer(object):
    """XBee Coordinator Server

    This class closely resembles the typical web server model, where the server
    lists for incoming connections and then creates new "worker" proccesses to
    handle the requests.

    """

    def __init__(self, frame_queue, nodes):
        self.logger = logging.getLogger('Producer')
        self.frame_queue = frame_queue
        self.nodes = nodes

        serial_port = util.open_serial_port()
        self.coordinator = Coordinator(serial_port)

    def start(self, discover_time, should_save_data):
        self.logger.info("Listening for packets...")
        while True:
            frame = self.coordinator.wait_read_frame()
            self.logger.debug("Received raw frame: %s", frame)
            self.frame_queue.put(frame)

    def shutdown(self):
        self.logger.info("Shutting down the producer...")
        self.coordinator.halt()
        self.logger.info("Producer shutdown complete.")
