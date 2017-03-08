import time
import os
import sys

if  __name__ == '__main__':
	path = os.path.abspath(os.curdir)
	while 1:
		ticks = time.strftime("%Y%m%d%H%M%S", time.localtime());
		filename = ticks+'.jpg'
		filename = os.path.join(path, 'pictures/'+filename)
		os.system('raspistill -o '+filename)
		# do something with the picture
		time.sleep(10)	
