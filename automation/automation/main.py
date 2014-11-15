"""The starting point for the automation system

1. Discover nodes on network.
2. Calibrate sensing nodes.
3. Collect data from each node.
4. Save data to csv file.

"""
import glob
from .models import Node
import signal
import sys
import time
import xbee

COORDINATOR_NAME = 'ms'
DISCOVER_TIME = 10  # seconds
coordinator = None
serialport = None


def signal_shutdown(signum, frame):
    """Always halt the xbee threads and close the serial connection."""
    global coordinator
    global serialport
    coordinator.halt()
    serialport.close()


def setup():
    global coordinator
    global serialport
    signal.signal(signal.SIGINT, signal_shutdown)

    # Platform specific serialports.
    if sys.platform == 'darwin':
        serialport = glob.glob('/dev/tty.usbserial*')[0]
    elif sys.platform == 'win32':
        serialport = 'COM9'
    else:  # Raspberry Pi
        serialport = glob.glob('/dev/ttyUSB*')

    coordinator = xbee.ZigBee(serialport)


def discover_nodes(discover_time):
    """Discover nodes on network for `time` secs."""
    global coordinator

    coordinator.send('at', frame='A', command='NT', parameter='\xFF')
    coordinator.at(command='ND')
    now = time.time()
    future = now + discover_time
    nodes = {COORDINATOR_NAME: coordinator}
    while time.time() < future:
        response = coordinator.wait_read_frame()
        if ('command' not in response) or (response['command'] != 'ND'):
            continue

        source_addr_long = response['source_addr_long']
        if source_addr_long not in nodes:
            name = response['parameter']['node_identifier']
            nodes[source_addr_long] = Node(source_addr_long, name)

    return nodes


def main():
    setup()
    nodes = discover_nodes(DISCOVER_TIME)
    signal_shutdown(0, None)

if __name__ == '__main__':
    main()
