import time
import os
import sys
import argparse

if  __name__ == '__main__':
	parser = argparse.ArgumentParser(description='capture picture with camera')
	parser.add_argument('-t' , dest='timeinterval', default=10, type=int, help='time interval to capture a picture')
	parser.add_argument('dir', help='directory to save the pictures', required=True)
	args = parser.parse_args()

	# path = os.path.abspath(os.curdir)
	path = args.dir;
	while 1:
		ticks = time.strftime("%Y%m%d%H%M%S", time.localtime());
		filename = ticks+'.jpg'
		filename = os.path.join(path, filename)
		os.system('raspistill -o '+filename)
		# do something with the picture
		time.sleep(args.timeinterval)	
