#!/usr/bin/env python
"""The starting point for the automation system

1. Discover nodes on network.
2. Calibrate sensing nodes.
3. Collect data from each node.
4. Save data to csv file.

"""
import atexit
import logging

from automation import util
from automation import Server

SHOULD_SAVE_DATA = True  # write to CSV files?
DATA_FILE = "data.csv"

NUM_WORKERS = 4


def shutdown(server):
    logging.info("Shutdown initiated...")
    server.shutdown()
    logging.info("Shutdown complete.")


def main():
    # Initialize logging.
    util.init_logger()

    # Initialize server to manage resources, the producer, and the consumers.
    server = Server(NUM_WORKERS)

    # Shutdown server at exit.
    atexit.register(shutdown, server)

    server.start()

if __name__ == '__main__':
    main()
