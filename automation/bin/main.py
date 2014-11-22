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
import threading

from automation import util
from automation import Server, Consumer

SHOULD_SAVE_DATA = True  # write to CSV files?
DATA_FILE = "data.csv"

DISCOVER_TIME = 20  # seconds
NUM_THREADS = 4


def shutdown_threads(queue):
    logging.info("Blocking until all tasks are done.")
    queue.join()
    logging.info("All done :)")


def main():
    # Initialize coordinator and serialport.
    coordinator = util.setup()

    # Queue for XBee packets.
    queue = multiprocessing.Queue()
    atexit.register(shutdown_threads, queue)

    # Spawn threads.
    for i in range(NUM_THREADS):
        t = Consumer(queue)
        t.setName("Consumer {0}".format(i))
        t.daemon = True
        t.start()

    server = Server(coordinator, queue)

    logging.info("Starting server...")
    server.start()


if __name__ == '__main__':
    main()
