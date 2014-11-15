"""The starting point for the automation system

1. Discover nodes on network.
2. Calibrate sensing nodes.
3. Collect data from each node.
4. Save data to csv file.

"""
import glob
import signal
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
    serialport = glob.glob('/dev/tty.usbserial*')[0]
    coordinator = xbee.ZigBee(serialport)


def discover_nodes(discover_time):
    """Discover nodes on network for `time` secs."""
    coordinator.send('at', frame='A', command='NT', parameter='\xFF')
    coordinator.at(command='ND')
    now = time.time()
    future = now + discover_time
    nodes = {COORDINATOR_NAME: coordinator}
    while time.time() < future:
        response = coordinator.wait_read_frame()
        if ('command' not in response) or (response['command'] != 'ND'):
            continue

        name = response['parameter']['node_identifier']
        if name not in nodes:
            pass


def main():
    setup()
    discover_nodes(DISCOVER_TIME)

if __name__ == '__main__':
    main()
