"""Boilerplate Python code for every XBee Series 2 operation."""
from glob import glob
import signal
import serial
from xbee import ZigBee


def signal_shutdown(signum, frame):
    """Always halt the xbee threads and close the serial connection."""
    xbee.halt()
    ser.close()

signal.signal(signal.SIGINT, signal_shutdown)

SERIALPORT = glob('/dev/tty.usbserial*')[0]
ser = serial.Serial(SERIALPORT, 9600)
xbee = ZigBee(ser)

# TODO: insert code here.

signal_shutdown()
