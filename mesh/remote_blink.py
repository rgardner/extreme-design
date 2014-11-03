import serial
from xbee import ZigBee
import time

SERIALPORT = '/dev/tty.usbserial-AH02QMT3'
ser = serial.Serial(SERIALPORT, 9600)
xbee = ZigBee(ser)

# replace with your router's address
myRouter = '\x00\x13\xa2\x00\x40\xbf\x05\x76'

while True:
    try:
        xbee.remote_at(dest_addr_long=myRouter, command='D4', parameter='\x05')
        time.sleep(1)

        xbee.remote_at(dest_addr_long=myRouter, command='D4', parameter='\x04')
        time.sleep(1)

    except KeyboardInterrupt:  # Ctrl-c
        break

xbee.halt()
ser.close()
