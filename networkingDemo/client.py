import socket

class Client():
   def __init__(self,Address=("174.205.12.99",5000)):
      self.s = socket.socket()
      self.s.connect(Address)

c = Client()