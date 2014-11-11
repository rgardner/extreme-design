"""Find first XBee on network and print its reponse and Node Identifier."""

import glob
import signal
import serial
from xbee import ZigBee


def signal_shutdown(signum, frame):
    xbee.halt()
    ser.close()

# Halt XBee and closer serial upon SIGINT (Ctrl-C)
signal.signal(signal.SIGINT, signal_shutdown)

SERIALPORT = glob.glob('/dev/tty.usbserial*')[0]
ser = serial.Serial(SERIALPORT, 9600)
xbee = ZigBee(ser)

# Set `Node Discovery Timeout` to X * 100ms
xbee.send('at', frame='A', command='NT', parameter='\xFF')
xbee.at(command='ND')

while True:
    response = xbee.wait_read_frame()
    if ('command' in response) and (response['command'] == 'ND'):
        print response
        print response['parameter']['node_identifier']
        break


signal_shutdown(0, None)
