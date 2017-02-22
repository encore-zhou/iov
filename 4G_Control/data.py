#!/usr/bin/python

import serial
import time
import sys


ser=serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=.1, rtscts=0)


while 1:
	response = ser.read(256)
	time.sleep(0.8)
	print response

