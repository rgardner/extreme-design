import atexit
import glob
import logging
import serial
import sys

from models import Coordinator

LOG_FILE = "automation.log"


def close_connections(coordinator, serialport):
    """Always halt the xbee threads and close the serial connection."""

    logging.debug("halting coordinator threads.")
    coordinator.halt()
    logging.debug("closing serial port.")
    serialport.close()


def setup():
    """Setup logging, open serialport, initilize coordinator."""

    # Enable logging on stdout.
    logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)  # enable for stdout
    ch.setLevel(logging.DEBUG)
    root.addHandler(ch)

    # Platform specific serialports.
    if sys.platform == 'darwin':
        port = glob.glob('/dev/tty.usbserial*')[0]
    elif sys.platform == 'win32':
        port = 'COM9'
    else:  # Raspberry Pi
        port = glob.glob('/dev/ttyUSB*')[0]

    logging.debug("opening port: %s", port)
    serialport = serial.Serial(port)
    logging.debug("initializing the coordinator.")
    coordinator = Coordinator(serialport)

    # Halt ZigBee and close serialport at exit.
    atexit.register(close_connections, coordinator, serialport)
    return coordinator


def write_to_csv(filename, packets):
    """Append packets to given file."""

    logging.debug("writing packets to file")
    with open(filename, "a") as f:
        for packet in packets:
            f.write(packet.to_csv())
