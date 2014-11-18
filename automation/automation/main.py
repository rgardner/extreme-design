"""The starting point for the automation system

1. Discover nodes on network.
2. Calibrate sensing nodes.
3. Collect data from each node.
4. Save data to csv file.

"""
import logging

from models import Node
import util

SHOULD_SAVE_DATA = True  # write to CSV files?
DATA_FILE = "data.csv"

DISCOVER_TIME = 30  # seconds
RECEIVE_TIME = 10   # seconds


def main():
    # Initialize coordinator and serialport.
    coordinator = util.setup()

    # Discover nodes with same PANID.
    logging.info("Discovering for %d seconds.", DISCOVER_TIME)
    nodes = coordinator.discover_nodes(DISCOVER_TIME)

    while True:
        # Receive sensor data from discovered nodes.
        logging.info("Receiving packets for %d seconds", DISCOVER_TIME)
        responses = coordinator.receive_sensor_data(RECEIVE_TIME)

        # Actuate nodes.
        logging.info("Actuating nodes.")
        for source_addr_long, node in nodes.iteritems():
            if node.type == Node.node_types['ac']:
                coordinator.actuate(node)

        if SHOULD_SAVE_DATA:
            util.write_to_csv(DATA_FILE, responses)


if __name__ == '__main__':
    main()
