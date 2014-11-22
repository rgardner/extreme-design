import logging
import multiprocessing

from automation import models


def handle(frame, pid, should_save_data):
    packet = models.Packet(frame)
    logging.getLogger("process-")
    print packet


class Server(object):
    """XBee Coordinator Server

    This class closely resembles the typical web server model, where the server
    lists for incoming connections and then creates new "worker" proccesses to
    handle the requests.

    """

    def __init__(self, coordinator):
        self.coordinator = coordinator
        self.logger = logging.getLogger('server')

    def start(self, discover_time, should_save_data):
        # Discover nodes with same PANID.
        self.logger.info("Discovering nodes for %d seconds.", discover_time)
        nodes = self.coordinator.discover_nodes(discover_time)

        self.logger.info("Listening for packets...")
        while True:
            # Receive sensor data from discovered nodes.
            frame = self.coordinator.wait_read_frame()
            process = multiprocessing.Process(target=handle,
                                              args=(frame, nodes,
                                                    should_save_data))
            process.daemon = True
            process.start()
            self.logger.debug("Started process %r", process)
