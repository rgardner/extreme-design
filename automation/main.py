"""The starting point for the automation system

1. Discover nodes on network.
2. Calibrate sensing nodes.
3. Collect data from each node.
4. Save data to csv file.

"""
import glob
import signal
import xbee

COORDINATOR_NAME = 'ms'
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


def main():
    setup()

if __name__ == '__main__':
    main()
