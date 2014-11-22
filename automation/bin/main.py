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
from automation import Server, Consumer

SHOULD_SAVE_DATA = True  # write to CSV files?
DATA_FILE = "data.csv"

DISCOVER_TIME = 20  # seconds
NUM_WORKERS = 4


def shutdown_threads(frame_queue):
    logging.info("Blocking until all tasks are done.")
    frame_queue.join()
    logging.info("All done :)")


def main():
    # Initialize coordinator and serialport.
    coordinator = util.setup()

    # Queue for XBee packets.
    frame_queue = multiprocessing.JoinableQueue()
    atexit.register(shutdown_threads, frame_queue)

    # Spawn threads.
    for i in range(NUM_WORKERS):
        p = Consumer(args=(i, frame_queue))
        p.setName("Consumer {0}".format(i))
        p.daemon = True  # run as background process
        p.start()

    server = Server(coordinator, frame_queue)

    logging.info("Starting server...")
    server.start()


if __name__ == '__main__':
    main()
