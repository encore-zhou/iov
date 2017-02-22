import socket, ssl, pprint,time  

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.load_cert_chain(certfile="/home/pi/iov/openssl/raspi.crt", keyfile="/home/pi/iov/openssl/raspi.key" , password="iovpro")
context.load_verify_locations("/home/pi/iov/openssl/ca.crt")
context.verify_mode = ssl.CERT_REQUIRED

#print context.get_ca_certs()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
print( "socket create success" )  
# require a certificate from the server  

ssl_sock = context.wrap_socket(s , server_hostname="iov-server")
ssl_sock.connect(('10.42.0.1', 10023))  
print( "socket connect success" )  
  
pprint.pprint(ssl_sock.getpeercert())  
# note that closing the SSLSocket will also close the underlying socket  
ssl_sock.send("hello world!") 
#ssl_sock.send(b'')  
ssl_sock.close()  
