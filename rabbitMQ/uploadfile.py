#!/usr/bin/env python
import socket
import struct
import os
import hashlib
import sys
import ssl
import pprint
from rpc_client import rpc_client
from argparse import ArgumentParser

BUFFER_SIZE = 1024
FILE_NAME = sys.argv[1]   # Change to your file
FILE_SIZE = os.path.getsize(FILE_NAME)
HEAD_STRUCT = '!128sIq32s'  # Structure of file head
hostip = "118.89.234.177"
CERTPATH='/home/pi/iov/openssl/'
#CERTPATH='/home/encore/Documents/iov/iov/openssl/'

class uploadfile(rpc_client):
    def __init__(self, username, passwd, hostip, queuename):
        super(uploadfile, self).__init__(username, passwd, hostip, queuename)

    def do_something(self, response):
        response = int(response)
        #Calculate MD5
        print "Calculating MD5..."
        fr = open(FILE_NAME, 'rb')
        md5_code = hashlib.md5()
        md5_code.update(fr.read())
        fr.close()
        print "Calculating success"
        
        # Need open again
        fr = open(FILE_NAME, 'rb')
        fn = os.path.split(FILE_NAME)[1]
        # Pack file info(file name and file size)
        print "file info:"
        print "file name:",fn
        print "file size:",FILE_SIZE
        file_head = struct.pack(HEAD_STRUCT, fn, len(fn), FILE_SIZE, md5_code.hexdigest())
        
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
            while(send_size < FILE_SIZE):
                if(FILE_SIZE - send_size < BUFFER_SIZE):
                    file_data = fr.read(FILE_SIZE - send_size)
                    send_size = FILE_SIZE
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
    args = parser.argparse()
    
    hostip = args.hostip;
    rpc = uploadfile("iov" , "iovpro" , hostip , "upload_queue")
    
    print(" [x] Requesting upload file")
    result = rpc.start("this is the message!")
    print(" [x] Upload file success")
    # print(" [.] Got server port:%r" % response)

