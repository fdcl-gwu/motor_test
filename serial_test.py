#! /usr/bin/python

import serial
import sys, time

from pylibftdi import Driver


def get_ftdi_device_list():
    """
    return a list of lines, each a colon-separated
    vendor:product:serial summary of detected devices
    """
    dev_list = []
    for device in Driver().list_devices():
        # list_devices returns bytes rather than strings
        dev_info = map(lambda x: x.decode('latin1'), device)
        # device must always be this triple
        vendor, product, serial = dev_info
        dev_list.append("%s:%s:%s" % (vendor, product, serial))
    return dev_list

if __name__ == '__main__':
    for device in get_ftdi_device_list():
        print(device)

sys.exit()


port=serial.Serial(
    port='/dev/ttyUSB0',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)

i=0
tmp = 0
# while True:
#
#     tmp=raw_input('send: ')
#
#     port.write(tmp)
#     port.flushOutput()
#
#     print port.read(1)
#     port.flushInput()
while True:
  tmp=raw_input('send: ')

  port.write(tmp)
  port.flushOutput()

  print port.read(port.inWaiting())
  port.flushInput()
