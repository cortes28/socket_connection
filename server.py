
# *****************************************************
# server side, has to be run first before the client.
# *****************************************************

import socket
import sys
import os

try:
	listenPort = int(sys.argv[1])

except:
	# The port on which to listen
	print("Default port will be chosen...")
	listenPort = 9999

print("Server port: ", str(listenPort))
# Create a welcome socket. 
welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
welcomeSock.bind(('', listenPort))

# Start listening on the socket
welcomeSock.listen(1)

# ************************************************
# Receives the specified number of bytes
# from the specified socket
# @param sock - the socket from which to receive
# @param numBytes - the number of bytes to receive
# @return - the bytes received
# *************************************************
def recvAll(sock, numBytes):

	# The buffer
	recvBuff = ""
	
	# The temporary buffer
	tmpBuff = ""
	
	# Keep receiving till all is received
	while len(recvBuff) < numBytes:
		
		# Attempt to receive bytes
		tmpBuff =  sock.recv(numBytes).decode()
		
		# The other side has closed the socket
		if not tmpBuff:
			break
		
		# Add the received bytes to the buffer
		recvBuff += tmpBuff
	
	return recvBuff

# ftp> get <file name> (downloads file <file name> from the server)
def get(socket, fileData):

	file = open(fileData, "r")
	fileInfo = file.read()

	# if no EOF
	if fileInfo:

		dataSizeStr = str(len(fileInfo))

		while len(dataSizeStr) < 10:
			dataSizeStr = "0" + dataSizeStr

		fileInfo =  dataSizeStr + fileInfo

		numSent = 0

		while len(fileInfo) > numSent:
			numSent += socket.send(fileInfo[numSent:].encode())


# for some reason len was not working created this as a way to mediate it
def fun_length(x):
	return len(x)


def ls(socket):


	list = []
	for line in os.popen('ls'):
		#print(line)
		list.append(line.strip('\n'))


	# converting list of what is in server to string
	data = str(list)

	length = str(fun_length(data))

	while fun_length(length) < 10:
		length = "0" + length

	data = length + data

	numSent = 0

	# sending data here
	while fun_length(data) > numSent:
		numSent += socket.send(data[numSent:].encode())




print ("Waiting for connections...")
	
# Accept connections
clientSock, addr = welcomeSock.accept()

print ("Accepted connection from client: ", addr)
print ("\n")

# Accept connections forever
while True:
	
	
	# The buffer to all data received from the
	# the client.
	fileData = ""
	
	# The temporary buffer to store the received
	# data.
	recvBuff = ""
	
	# The size of the incoming file
	fileSize = 0	
	
	# The buffer containing the file size
	fileSizeBuff = ""

	# reads the particular command that the user requested [get, put, ls]
	# ---------------------------------- original command to read
	# command =  clientSock.recv(30).decode()

	buffsize = 0

	fileSizeBuff = recvAll(clientSock, 10)
	fileSize = int(fileSizeBuff)
	string = recvAll(clientSock, fileSize)

	print("command that was given to the server: ", string)

	commands = string.split()
	command = commands[0]


	print("\nCommand: ", command, '\n')

	# gives to the client the desired file
	if command == "get":
		print(commands[1])
		get(clientSock, commands[1])
		print("SUCCESS\n")


	# reads from the client...
	elif command == "put":
		print("from: ", str(commands[1]))
		#put(clientSock, commands[1])
		print(commands[2:])
		print("Received ", str(fileSize), " bytes")
		print("SUCCESS\n")

	# prints what is there...
	elif command == "ls":
		ls(clientSock)
		print("SUCCESS\n")

	# prints that there was an invalid requet
	else:
		print("invalid request...")
		print("FAILURE")
	

clientSock.close()
	
