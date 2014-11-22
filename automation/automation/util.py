import atexit
import glob
import logging
import serial
import sys

LOG_FILE = "automation.log"


def init_logger():
    """Setup logging for file and stdout."""
    logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)  # enable for stdout
    ch.setLevel(logging.DEBUG)
    root.addHandler(ch)


def open_serial_port():
    # Platform specific serial ports.
    if sys.platform == 'darwin':  # mac osx
        port = glob.glob('/dev/tty.usbserial*')[0]
    elif sys.platform == 'win32':  # windows
        port = 'COM9'
    else:  # Raspberry Pi
        port = glob.glob('/dev/ttyUSB*')[0]

    logging.debug("opening port: %s", port)
    serial_port = serial.Serial(port)

    atexit(_close_serial_port, serial_port)
    return serial_port


def write_to_csv(filename, packets):
    """Append packets to given file."""

    logging.debug("writing packets to file")
    with open(filename, "a") as f:
        for packet in packets:
            f.write(packet.to_csv() + "\n")


def _close_serial_port(serial_port):
    logging.debug("closing serial port: %s", serial_port)
    serial_port.close()
