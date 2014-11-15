"""The starting point for the automation system

1. Discover nodes on network.
2. Calibrate sensing nodes.
3. Collect data from each node.
4. Save data to csv file.

"""
import glob
import signal
import serial
import sys
import time
import xbee

from .models import Node

COORDINATOR_NAME = 'ms'
DISCOVER_TIME = 10  # seconds
RECEIVE_TIME = 10  # seconds
coordinator = None
serialport = None


def signal_shutdown(signum, frame):
    """Always halt the xbee threads and close the serial connection."""
    global coordinator
    global serialport
    coordinator.halt()
    serialport.close()


def setup():
    """Attach signal handler and initialize coordinator and serialport."""
    global coordinator
    global serialport
    signal.signal(signal.SIGINT, signal_shutdown)

    # Platform specific serialports.
    if sys.platform == 'darwin':
        port = glob.glob('/dev/tty.usbserial*')[0]
    elif sys.platform == 'win32':
        port = 'COM9'
    else:  # Raspberry Pi
        port = glob.glob('/dev/ttyUSB*')

    serialport = serial.Serial(port)
    coordinator = xbee.ZigBee(serialport)


def discover_nodes(discover_time):
    """Discover nodes on network for `time` secs."""
    global coordinator

    # Set node discover time to FF; send node discover from coordinator.
    coordinator.send('at', frame='A', command='NT', parameter='\xFF')
    coordinator.at(command='ND')

    nodes = {}  # source_addr_long: node object, includes coordinator.
    future = time.time() + discover_time
    while time.time() < future:
        response = coordinator.wait_read_frame()
        if ('command' not in response) or (response['command'] != 'ND'):
            continue

        source_addr_long = response['source_addr_long']
        if source_addr_long not in nodes:
            name = response['parameter']['node_identifier']
            if name == COORDINATOR_NAME:
                nodes[source_addr_long] = coordinator
            else:
                nodes[source_addr_long] = Node(source_addr_long, name)

    return nodes


def receive_sensor_data(receive_time, nodes):
    """Recieve sensor data."""
    global coordinator

    responses = []
    future = time.time() + receive_time
    while time.time() < future:
        responses.append(coordinator.wait_read_frame())
    return responses


def main():
    # Initialize coordinator and serialport.
    setup()

    # Discover nodes with same PANID.
    nodes = discover_nodes(DISCOVER_TIME)

    while True:
        # Receive sensor data from discovered nodes.
        receive_sensor_data(RECEIVE_TIME)

        # Actuate nodes.
        for node in nodes:
            if node.type == Node.node_types['ac']:
                node.actuate(coordinator)

    # Halt XBee threads and close serialport.
    signal_shutdown(0, None)

if __name__ == '__main__':
    main()
