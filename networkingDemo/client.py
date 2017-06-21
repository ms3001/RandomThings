import socket

class Client():
   def __init__(self,Adress=("server script IP",5000)):
      self.s = socket.socket()
      self.s.connect(Adress)

c = Client()