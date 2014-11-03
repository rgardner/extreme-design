"""
Simple Xbee Series 2 Wireless Sensing

This receives the raw packet data and outputs it to stdout
"""
import serial
from xbee import ZigBee

SERIALPORT = '/dev/tty.usbserial-AH02QMT3'
ser = serial.Serial(SERIALPORT, 9600)
xbee = ZigBee(ser)
counter = 0

while True:
    try:
        data = xbee.wait_read_frame()
        print "%d: %s" % (counter, data['samples'])
        counter += 1
    except KeyboardInterrupt:
        break

ser.close()
