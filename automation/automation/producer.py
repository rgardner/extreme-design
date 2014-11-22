import logging


class Server(object):
    """XBee Coordinator Server

    This class closely resembles the typical web server model, where the server
    lists for incoming connections and then creates new "worker" proccesses to
    handle the requests.

    """

    def __init__(self, coordinator, frame_queue):
        self.coordinator = coordinator
        self.frame_queue = frame_queue
        self.logger = logging.getLogger('server')

    def start(self, discover_time, should_save_data):
        self.logger.info("Listening for packets...")
        while True:
            frame = self.coordinator.wait_read_frame()
            self.logger.debug("Received raw frame: %s", frame)
            self.frame_queue.put(frame)
