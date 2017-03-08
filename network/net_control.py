#!/usr/bin/python

import serial
import time
import sys
import argparse
import os

class networkControl(object):
	"""docstring for networkControl"""
	def __init__(self, serialport, baudrate=115200, timeout=0.1, rtscts=0):
		super(networkControl, self).__init__()
		self.serialport = serialport
		self.baudrate = baudrate
		self.timeout = timeout
		self.rtscts = rtscts

	def checkNetConnect(self):
		connected = False
		checktime = 3
		while (not connected and checktime > 0):
			connected = os.system('ping 8.8.8.8 -qc 3')
			checktime -=1
		if connected:
			print 'ping fail'
		else:
			print 'ping ok'
		return not connected

	def connect4G(self):
		print "serialport:",self.serialport
		print "baudrate:",self.baudrate
		print "timeout:",self.timeout
		print "rtscts:",self.rtscts
		ser = serial.Serial(self.serialport, baudrate=self.baudrate, timeout=self.timeout, rtscts=self.rtscts)

		ser.write(b'ATE1\r')
		response = ser.read(256)
		print response
		
		ser.write(b'AT^SYSINFO\r')
		response = ser.read(256)
		print response
		
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
		return self.checkNetConnect()

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='check network status and control network')
	parser.add_argument('-s', dest='serialport', help='serialport to the network device' , required=True)
	parser.add_argument('-b', dest='baudrate',default=115200,type=int, help='set baudrate to serialport')
	parser.add_argument('-t', dest='timeout',default=.1,type=float, help='set timeout to serialport connection')
	parser.add_argument('-r', dest='rtscts',default=0,type=int, help='set rtscts to serialport')
	parser.add_argument('-i', dest='interval', default=60, type=int, help='time interval to check the network status')
	args = parser.parse_args()

	nc = networkControl(args.serialport, args.baudrate, args.timeout, args.rtscts)
	while 1:
		print " [x]check network connection"
		connected = nc.checkNetConnect()
		if connected:
			print " [.]network is connected"
		else:
			print " [x]cannot connect to network, try 4G connection..."
			if nc.connect4G():
				print " [.]connected to 4G network"
			else:
				print " [x]failed to connection"
		time.sleep(args.interval)
