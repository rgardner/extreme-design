"""Find X number of XBees on the same network."""

from glob import glob
import signal
import serial
import sys
from xbee import ZigBee

COORDINATOR = 'MASTER'
if sys.argv and len(sys.argv) > 1:
    NUM_TO_FIND = sys.argv[1]
else:
    NUM_TO_FIND = 2


def signal_shutdown(signum, frame):
    """Always halt the xbee threads and close the serial connection."""
    xbee.halt()
    ser.close()

signal.signal(signal.SIGINT, signal_shutdown)

SERIALPORT = glob('/dev/tty.usbserial*')[0]
ser = serial.Serial(SERIALPORT, 9600)
xbee = ZigBee(ser)

xbee.send('at', frame='A', command='NT', parameter='\xFF')
xbee.at(command='ND')

found = []
while len(found) < NUM_TO_FIND:
    response = xbee.wait_read_frame()
    if ('command' in response) and (response['command'] == 'ND'):
        name = response['parameter']['node_identifier']
        if name != COORDINATOR and name not in found:
            found.append(name)

for f in found:
    print f

signal_shutdown(0, None)
