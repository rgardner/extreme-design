#!/usr/bin/env python
"""The starting point for the automation system

1. Discover nodes on network.
2. Calibrate sensing nodes.
3. Collect data from each node.
4. Save data to csv file.

"""
import atexit
import logging
import multiprocessing

from automation import util
from automation import Server

SHOULD_SAVE_DATA = True  # write to CSV files?
DATA_FILE = "data.csv"

DISCOVER_TIME = 20  # seconds
RECEIVE_TIME = 10   # seconds


def shutdown_threads():
    logging.info("Shutting down")
    for process in multiprocessing.active_children():
        logging.info("Shutting down process: %r", process)
        process.terminate()
        process.join()
    logging.info("All done :)")


def main():
    # Initialize coordinator and serialport.
    coordinator = util.setup()
    atexit.register(shutdown_threads)

    # Discover nodes with same PANID.
    logging.info("Discovering for %d seconds.", DISCOVER_TIME)
    nodes = coordinator.discover_nodes(DISCOVER_TIME)

    server = Server(coordinator)
    logging.info("Listening for XBee packets")
    server.start()


if __name__ == '__main__':
    main()
