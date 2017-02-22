#!/usr/bin/env python
import pika
import socket
import thread
import struct
import hashlib
import ssl
import pprint
import time
import dlib

BUFFER_SIZE = 1024
HEAD_STRUCT = '!128sIq32s'   # Structure of file head
hostip = '10.42.0.1'

credential = pika.PlainCredentials('encore' , 'encore')

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=hostip , credentials=credential))

channel = connection.channel()

channel.queue_declare(queue='upload_queue')

def upload_file(s):
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="/home/encore/Documents/iov/iov/openssl/server.crt", keyfile="/home/encore/Documents/iov/iov/openssl/server.key" , password="iovpro")
    context.load_verify_locations("/home/encore/Documents/iov/iov/openssl/ca.crt")
    context.verify_mode = ssl.CERT_REQUIRED
    
    client_socket, client_address = s.accept()
    
    try:
        connstream = context.wrap_socket(client_socket, server_side=True) 
    except BaseException:
        print "fail to verify client!"
        return
        # continue

    print 'connection address:', client_address
    # print "Socket %s:%d has connect" % client_address

    try:  
        pprint.pprint(connstream.getpeercert())  

    # Receive file info
        info_struct = struct.calcsize(HEAD_STRUCT)
        file_info = connstream.recv(info_struct)
        file_name2, filename_size, file_size, md5_recv = struct.unpack(HEAD_STRUCT, file_info)
        file_name = file_name2[:filename_size]
        print "file info:"
        print "file name:",file_name
        print "file size:",file_size
        fw = open(file_name, 'wb')
    
        recv_size = 0
        print "Receiving data..."
        while (recv_size < file_size):
            if(file_size - recv_size < BUFFER_SIZE):
                file_data = connstream.recv(file_size - recv_size)
                # recv_size = file_size
            else:
                file_data = connstream.recv(BUFFER_SIZE)
                # recv_size += BUFFER_SIZE
            recv_size += len(file_data)
            fw.write(file_data)
        fw.close()
        print "Accept success!"
        print "Calculating MD5..."
        
        fw = open(file_name, 'rb')
        md5_cal = hashlib.md5()
        md5_cal.update(fw.read())
        print "  Recevie MD5 : %s" %md5_recv
        print "Calculate MD5 : %s" % md5_cal.hexdigest()
        fw.close()

    finally:  
        connstream.shutdown(socket.SHUT_RDWR)  
        connstream.close()  
        s.close()

def getFile(n):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    s.bind(("",0))  
    s.listen(1)  
    port = s.getsockname()[1]

    try:
        thread.start_new_thread( upload_file, ( s, ) )
    except:
        print "Error: unable to start thread"
    # s.close()
    return port

def on_request(ch, method, props, body):
    n = int(body)

    print(" [.] upload request(%s)" % n)
    response = getFile(n)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='upload_queue')

print(" [x] Awaiting RPC requests")
channel.start_consuming()