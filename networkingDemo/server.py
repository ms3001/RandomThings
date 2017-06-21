import socket

s = socket.socket()
host = ''
port = 9078
s.bind((host,port))
s.listen(5)

while True:
    c, addr = s.accept()
    print("Connection accepted from " + repr(addr[1]))
    c.send("You have been heard, what do you want to say?")
    print c.recv(1024)
    c.close()