import string, socket, time, numpy as np
			
def getUser(line):
	separate = line.split(":", 2)
	user = separate[1].split("!", 1)[0]
	return user

def getMessage(line):
	separate = line.split(":", 2)
	message = separate[2]
	return message

def openSocket():
	s = socket.socket()
	s.connect(("irc.chat.twitch.tv", 6667))
	s.send("PASS " + "oauth:ncxzgp9pb7t68lwkayagai7h13gsjk" + "\r\n")
	s.send("NICK " + "msthreezero" + "\r\n")
	s.send("JOIN #" + "shroud" + "\r\n")
	return s
	
def sendMessage(s, message):
	messageTemp = "PRIVMSG #" + "shroud" + " :" + message
	s.send(messageTemp + "\r\n")
	print("Sent: " + messageTemp)

def joinRoom(s):
	readbuffer = ""
	Loading = True
	while Loading:
		readbuffer = readbuffer + s.recv(1024)
		temp = string.split(readbuffer, "\n")
		readbuffer = temp.pop()
		
		for line in temp:
			print(line)
			Loading = loadingComplete(line)
	sendMessage(s, "Successfully joined chat")
	
def loadingComplete(line):
	if("End of /NAMES list" in line):
		return False
	else:
		return True

s = openSocket()
joinRoom(s)
readbuffer = ""
start_time = time.time()
count = 0
list_of_times = []

while True:
		readbuffer = readbuffer + s.recv(512)
		temp = string.split(readbuffer, "\n")
		readbuffer = temp.pop()
		print('blah---xxx')
		if len(temp) == 0: # We sometimes get kicked out of room.
			s = openSocket()
			joinRoom(s)
			print('Rejoined room')
			

		for line in temp:
			#print(line)
			if "PING" in line:
				s.send(line.replace("PING", "PONG"))
				print(line)
				break
			user = getUser(line)
			message = getMessage(line)
			print user + " typed :" + message
			print time.time() - start_time
			list_of_times.append(time.time() - start_time)
			
			if (len(list_of_times) == 1000):
			 	out = np.asarray(list_of_times)
			 	list_of_times = []
			 	np.savetxt("chatoutput" + str(count) + ".txt", out, fmt="%.2f", delimiter="\t")
			 	count = count + 1
			 	break




			