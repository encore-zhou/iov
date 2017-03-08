#!/usr/bin/env python
import socket
import struct
import os
import hashlib
import sys
import ssl
import pprint
from rpc_client import rpc_client
import argparse

BUFFER_SIZE = 1024
HEAD_STRUCT = '!128sIq32s'  # Structure of file head
hostip = "118.89.234.177"
CERTPATH='/home/pi/iov/openssl/'
#CERTPATH='/home/encore/Documents/iov/iov/openssl/'

class uploadfile(rpc_client):
    def __init__(self, username, passwd, hostip, queuename, filename):
        super(uploadfile, self).__init__(username, passwd, hostip, queuename)
        self.FILE_NAME = filename
        self.FILE_SIZE = os.path.getsize(filename)

    def do_something(self, response):
        response = int(response)
        #Calculate MD5
        print "Calculating MD5..."
        fr = open(self.FILE_NAME, 'rb')
        md5_code = hashlib.md5()
        md5_code.update(fr.read())
        fr.close()
        print "Calculating success"
        
        # Need open again
        fr = open(self.FILE_NAME, 'rb')
        fn = os.path.split(self.FILE_NAME)[1]
        # Pack file info(file name and file size)
        print "file info:"
        print "file name:",fn
        print "file size:",self.FILE_SIZE
        file_head = struct.pack(HEAD_STRUCT, fn, len(fn), self.FILE_SIZE, md5_code.hexdigest())
        
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.load_cert_chain(certfile=os.path.join(CERTPATH,'client.crt'), keyfile=os.path.join(CERTPATH , 'client.key'), password="iovpro")
        context.load_verify_locations(os.path.join(CERTPATH , 'ca.crt'))
        context.verify_mode = ssl.CERT_REQUIRED
        
        try:
            sock = socket.socket()
            # print("Connecting to %s port %d" % (hostip , response))
            #sock.connect((hostip, response))
            ssl_sock = context.wrap_socket(sock , server_hostname="iov-server")
            ssl_sock.connect((hostip, response))  

            # pprint.pprint(ssl_sock.getpeercert())  
            
            # Send file info
            ssl_sock.send(file_head)
            send_size = 0
            print "Sending data..."
            while(send_size < self.FILE_SIZE):
                if(self.FILE_SIZE - send_size < BUFFER_SIZE):
                    file_data = fr.read(self.FILE_SIZE - send_size)
                    send_size = self.FILE_SIZE
                else:
                    file_data = fr.read(BUFFER_SIZE)
                    send_size += BUFFER_SIZE
                ssl_sock.send(file_data)
            print "Send success!"
            print "MD5 : %s" % md5_code.hexdigest()
        
            fr.close()
            ssl_sock.close()
        
        except socket.errno, e:
            print "Socket error: %s" % str(e)
        except Exception, e:
            print "Other exception : %s" % str(e)
        finally:
            print "Closing connect"

        return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='upload file to the server')
    parser.add_argument('-host', dest='hostip', default='118.89.234.177',help='host ip of the server')
    parser.add_argument('-f', dest='FILE_NAME', required=True, help='select a file to upload')
    args = parser.parse_args()
    
    hostip = args.hostip;
    rpc = uploadfile("iov" , "iovpro" , hostip , "upload_queue", args.FILE_NAME)
    
    print(" [x] Requesting upload file")
    result = rpc.start("this is the message!")
    print(" [x] Upload file success")
    # print(" [.] Got server port:%r" % response)

