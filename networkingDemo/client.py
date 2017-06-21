import socket

s = socket.socket()
host = "localhost"
port = 9078
s.connect((host, port))
print s.recv(1024)
while True:
	data = raw_input("")
	s.sendto(data,(host,port))

