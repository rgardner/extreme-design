"""
Simple Xbee Series 2 Wireless Sensing

This receives the raw packet data and outputs it to stdout.
"""
from glob import glob
import serial
import signal
from xbee import ZigBee


def signal_shutdown(signum, frame):
    """Always halt the xbee threads and close the serial connection."""
    xbee.halt()
    ser.close()

signal.signal(signal.SIGINT, signal_shutdown)

SERIALPORT = glob('/dev/tty.usbserial*')[0]
ser = serial.Serial(SERIALPORT, 9600)
xbee = ZigBee(ser)
counter = 0

while True:
    data = xbee.wait_read_frame()
    print data
    counter += 1

signal_shutdown(0, None)
