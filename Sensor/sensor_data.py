#!/usr/bin/python

import serial
import time
import sys
import json

serialport = sys.argv[1]
ser=serial.Serial(serialport, baudrate=115200, timeout=.1, rtscts=0)

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
	#print json.dumps(jsonFormat)
	time.sleep(0.8)

