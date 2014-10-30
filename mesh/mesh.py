#!/usr/bin/env python
"""
Continuously read the serial port and process IO data received from a remote
XBee.
"""

import serial
import time
from xbee import ZigBee  # Xbee Series 2

SERIALPORT = "/dev/tty.usbserial-A602N3AY"
# SERIALPORT = "/dev/tty.usbserial-AH02QMT3"


def print_data(data):
    """
    This method is called whenever data is received from the associated XBee
    device. Its first and only argument is the data contained within the frame.
    """
    print data

ser = serial.Serial(SERIALPORT, 9600)
xbee = ZigBee(ser, callback=print_data)

# Continuously read and print packets
while True:
    try:
        time.sleep(0.1)
    except KeyboardInterrupt:
        break

xbee.halt()
ser.close()
