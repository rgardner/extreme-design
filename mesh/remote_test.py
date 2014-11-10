"""Find X number of XBees on the same network."""

from glob import glob
import signal
import serial
from xbee import ZigBee

COORDINATOR = 'MASTER'
NUM_TO_FIND = 2  # the number of xbee nodes to find.


def signal_shutdown(signum, frame):
    """Always halt the xbee threads and close the serial connection."""
    xbee.halt()
    ser.close()

signal.signal(signal.SIGINT, signal_shutdown)

SERIALPORT = glob('/dev/tty.usbserial*')[0]
ser = serial.Serial(SERIALPORT, 9600)
xbee = ZigBee(ser)

xbee.send('at', frame='A', command='NT', parameter='FF')
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
