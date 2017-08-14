import string, socket
			
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
	s.send("JOIN #" + "imaqtpie" + "\r\n")
	return s
	
def sendMessage(s, message):
	messageTemp = "PRIVMSG #" + "imaqtpie" + " :" + message
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

while True:
		readbuffer = readbuffer + s.recv(1024)
		temp = string.split(readbuffer, "\n")
		readbuffer = temp.pop()
		
		for line in temp:
			print(line)
			if "PING" in line:
				s.send(line.replace("PING", "PONG"))
				break
			user = getUser(line)
			message = getMessage(line)
			print user + " typed :" + message
			if "You Suck" in message:
				sendMessage(s, "No, you suck!")
				break