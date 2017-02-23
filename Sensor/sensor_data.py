#!/usr/bin/python

import serial
import time
import sys

serialport = sys.argv[1]
ser=serial.Serial(serialport, baudrate=115200, timeout=.1, rtscts=0)

while 1:
	rawdata = ser.read(256)
	if rawdata[0] == 's' && rawdata[-1] == 'e':
		print rawdata
	else
		print "broken data!"	
	time.sleep(0.8)

