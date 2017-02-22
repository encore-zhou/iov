#!/usr/bin/env python
import pika
import uuid
import socket
import struct
import os
import hashlib
import sys
import ssl
import pprint

BUFFER_SIZE = 1024
FILE_NAME = sys.argv[1]   # Change to your file
FILE_SIZE = os.path.getsize(FILE_NAME)
HEAD_STRUCT = '!128sIq32s'  # Structure of file head
hostip = "192.168.5.135"
CERTPATH='/home/pi/iov/openssl/'
#
class FibonacciRpcClient(object):
    def __init__(self):
        credential = pika.PlainCredentials('encore' , 'encore')

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=hostip , credentials=credential))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='upload_queue',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)

fibonacci_rpc = FibonacciRpcClient()

print(" [x] Requesting upload file")
response = fibonacci_rpc.call(30)
# print(" [.] Got server port:%r" % response)

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
    #sock.connect((hostip, response))
    ssl_sock = context.wrap_socket(sock , server_hostname="iov-server")
    ssl_sock.connect((hostip, response))  
    #print "Connecting to %s port %s" % hostip , response
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
