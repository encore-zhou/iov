#!/usr/bin/python

import serial
import time
import sys


ser=serial.Serial('/dev/ttyUSB1', baudrate=115200, timeout=.1, rtscts=0)

ser.write(b'ATE1\r')
response = ser.read(256)
print response

ser.write(b'AT^SYSINFO\r')
response = ser.read(256)
print response

#ser.write(b'AT^ZGACT=0,1\r')
#response = ser.read(256)
#print response
flag=1
while(flag):
	ser.write(b'AT+CGACT=1,1\r')
#	time.sleep(0.5)
	response = ser.read(256)
	print response
	if response.find("ERROR") == -1:
		flag = 0

flag=1
while(flag):
	ser.write(b'AT+ZGACT=0,1\r')
	response = ser.read(256)
	print response
	ser.write(b'AT+ZGACT=1,1\r')
#	time.sleep(0.5)
	response = ser.read(256)
	print response
	if response.find("+ZCONSTAT: 1,1") != -1:
		flag = 0
