"""
Continuously read the serial port and process IO data received from a remote
XBee.
"""

from xbee import XBee
import serial

SERIALPORT = "/dev/tty.usbserial-AH02QMT3"
ser = serial.Serial(SERIALPORT, 9600)

xbee = XBee(ser)

# Continuously read and print packets
while True:
    try:
        response = xbee.wait_read_frame()
        print response
    except KeyboardInterrupt:
        break

ser.close()
