#!/usr/bin/python

import serial
import time
import sys

serialport = sys.argv[1]
ser=serial.Serial(serialport, baudrate=115200, timeout=.1, rtscts=0)

while 1:
	response = ser.read(256)
	time.sleep(0.8)
	print response

