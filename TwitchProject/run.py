import string, socket, time, datetime, numpy as np, requests, json
			
# Function used to parse twitch PRVMSG to return user name
def getUser(line):
	separate = line.split(":", 2)
	user = separate[1].split("!", 1)[0]
	return user

# Function used to parse twitch PRVMSG to return message
def getMessage(line):
	separate = line.split(":", 2)
	message = separate[2]
	return message

# Function used to create socket connection with twitch stream
def openSocket(stream):
	s = socket.socket()
	s.connect(("irc.chat.twitch.tv", 6667))
	s.send("PASS " + "oauth:ncxzgp9pb7t68lwkayagai7h13gsjk" + "\r\n")
	s.send("NICK " + "msthreezero" + "\r\n")
	s.send("JOIN #" + stream + "\r\n")
	return s

# Function used to send message to twitch stream using given socket	
def sendMessage(s, message, stream):
	messageTemp = "PRIVMSG #" + stream + " :" + message
	s.send(messageTemp + "\r\n")
	print("Sent: " + messageTemp)

# Function used to join given twitch stream with given socket
def joinRoom(s, stream):
	readbuffer = ""
	Loading = True
	while Loading:
		readbuffer = readbuffer + s.recv(1024)
		temp = string.split(readbuffer, "\n")
		readbuffer = temp.pop()
		
		for line in temp:
			print(line)
			Loading = loadingComplete(line)
	sendMessage(s, "Successfully joined chat", stream)

def loadingComplete(line):
	if("End of /NAMES list" in line):
		return False
	else:
		return True

# Function used to find when given stream was started
def getStreamData(stream):
	payload = {'Client-ID': 'kty4svj7yncksdfls55emyj9btqufe'}
	print('Requesting stream data')
	r = requests.get('https://api.twitch.tv/kraken/streams/' + stream, headers=payload)
	raw_time = (r.json()['stream']['created_at'])
	stream_start_time = time.mktime(datetime.datetime.strptime(raw_time, "%Y-%m-%dT%H:%M:%SZ").timetuple())
	print('Stream started at: ' + str(stream_start_time))
	# Weird numbers being added are for EST to UTC conversion
	print('Stream has been live for: ' + str(time.time()+4*60*60-stream_start_time))
	return time.time()+4*60*60-stream_start_time # stream_live_time

stream = 'shroud'
s = openSocket(stream)
joinRoom(s, stream)
stream_live_time = getStreamData(stream)
start_time = time.time()
readbuffer = ""
count = 0
list_of_times = []

while True:
		readbuffer = readbuffer + s.recv(1024)
		temp = string.split(readbuffer, "\n")
		readbuffer = temp.pop()
		if len(temp) == 0: # We sometimes get kicked out of room.
			s = openSocket(stream)
			joinRoom(s, stream)
			print('Rejoined room')
			

		for line in temp:
			#print(line)
			if "PING" in line: # Need to respond to twitch PONG messages
				s.send(line.replace("PING", "PONG"))
				print("Sent PONG message")
				break
			user = getUser(line)
			message = getMessage(line)
			#print user + " typed :" + message

			list_of_times.append(time.time() - start_time + stream_live_time)
			print time.time() - start_time + stream_live_time

			if (len(list_of_times) == 1000):
			 	out = np.asarray(list_of_times)
			 	list_of_times = []
			 	np.savetxt("chatoutput" + str(count) + ".txt", out, fmt="%.2f", delimiter="\t")
			 	count = count + 1
			 	break




			