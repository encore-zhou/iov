import socket, ssl, time ,pprint 
  
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="/home/encore/Documents/iov/openssl/server.crt", keyfile="/home/encore/Documents/iov/openssl/server.key" , password="iovpro")
context.load_verify_locations("/home/encore/Documents/iov/openssl/ca.crt")
context.verify_mode = ssl.CERT_REQUIRED  
bindsocket = socket.socket()  
print( "socket create success" )  
bindsocket.bind(('10.42.0.1', 10023))  
print( "socket bind success" )  
bindsocket.listen(5)  
print( "socket listen success" )  
  
def do_something(connstream, data):  
    print("data length:",len(data))  
    print data
    return True  
  
def deal_with_client(connstream):
    data = connstream.recv(1024)
    # empty data means the client is finished with us
    while data:
        if not do_something(connstream, data):
            # we'll assume do_something returns False
            # when we're finished with client
            break
        data = connstream.recv(1024)
    # finished with client
  
while True:  
    newsocket, fromaddr = bindsocket.accept()  
    print( "socket accept one client" )  
    
    try:
        connstream = context.wrap_socket(newsocket, server_side=True) 
    except BaseException:
    	print "fail to verify client!"
    	continue

    try:  
        pprint.pprint(connstream.getpeercert())  
        deal_with_client(connstream)  
    finally:  
        connstream.shutdown(socket.SHUT_RDWR)  
        connstream.close()  