import socket
import time
import os 
import random

class Server():
	def __init__(self,Adress=('',5000),MaxClient=1):
 		self.s = socket.socket()
		self.s.bind(Adress)
		self.s.listen(MaxClient)
 	def WaitForConnection(self):
		self.Client, self.Adr=(self.s.accept())
		print('Got a connection from: '+str(self.Client)+'.')


s = Server()
s.WaitForConnection()