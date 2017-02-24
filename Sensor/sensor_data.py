#!/usr/bin/env python

import serial
import time
import sys
import json
from rpc_client import rpc_client
serialport = sys.argv[1]

class sensor_data(rpc_client):
	"""docstring for sensor_data"""
	def __init__(self, username, passwd, hostip, queuename, serialport):
		super(sensor_data, self).__init__(username, passwd, hostip, queuename)
		self.serialport = serialport

	# def do_something(self, response):
	# 	return True
	
	def processing_data():
		ser=serial.Serial(self.serialport, baudrate=115200, timeout=.1, rtscts=0)
		while 1:
			rawdata = ser.read(256)
			if len(rawdata) == 0:
				continue
			if (rawdata[0] != 's' or rawdata[-3] != 'e'):
				print "broken data!"
				continue
			nums = rawdata.split(" ")[1:-1]
			if len(nums) != 16:
				continue
			ticks = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
			for i in range(0,16):
				nums[i] = float(nums[i])
			jsonFormat = {'acx': nums[0],'acy':nums[1] ,'acz':nums[2] ,'grx':nums[3] ,'gry':nums[4] ,'grz':nums[5] ,'agx':nums[6] ,'agy':nums[7] ,'agz':nums[8] ,'mag':nums[9] ,'pap':nums[10] ,'php':nums[11] ,'lng':nums[12] ,'lat':nums[13] ,'gph':nums[14] ,'gpv':nums[15] ,'t':ticks}
			print jsonFormat
			self.start(jsonFormat)
			time.sleep(0.8)
		return

factory = sensor_data("iov", "iovpro", "118.89.234.177", "sensor_data", serialport)
factory.processing_data()
