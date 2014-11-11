from glob import glob
import serial
import signal
from xbee import ZigBee
import time


def signal_shutdown(signum, frame):
    xbee.halt()
    ser.close()

# Halt XBee and closer serial upon SIGINT (Ctrl-C)
signal.signal(signal.SIGINT, signal_shutdown)

SERIALPORT = glob('/dev/tty.usbserial*')[0]
ser = serial.Serial(SERIALPORT, 9600)
xbee = ZigBee(ser)

# replace with your router's address.
# myRouter = '\x00\x13\xa2\x00\x40\xbf\x05\x76'
myRouter = '\x00\x13\xa2\x00\x40\xb9\x6D\x77'

while True:
    xbee.remote_at(dest_addr_long=myRouter, command='D4', parameter='\x05')
    time.sleep(1)

    xbee.remote_at(dest_addr_long=myRouter, command='D4', parameter='\x04')
    time.sleep(1)

signal_shutdown(0, None)
