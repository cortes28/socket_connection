
# *******************************************************************
#.The client side that connects to the already established server. 
# *******************************************************************

import socket
import sys

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


# Command line checks 

# Server address
serverAddr = "localhost"

try:
	serverPort = int(sys.argv[2])
	serverAddr = str(sys.argv[1])
except:
	# The port on which to listen
	print("Default port will be chosen...")
	serverPort = 9999
# # The name of the file
# fileName = sys.argv[1]

# # Open the file
# fileObj = open(fileName, "r")
print("Client port: ", str(serverPort))
# Create a TCP socket
connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
connSock.connect((serverAddr, serverPort))

# The number of bytes sent
num_sent = 0

# number received

numReceived = 0

# The file data
fileData = None

# can use this to see if its within the list, if it ain't on the list then we close or ask again for a different input
dict = {"get": 1, "put": 1, "ls": 1, "quit": 0}

connect = True
# Keep sending until all is sent
while connect:

	print("****************************************************************")
	command = input("ftp> ")

	if command:
		list = command.split()

		if list[0] in dict:

			# 
			# sending the 'get' meaning we would recieve data from the file desired in the server
			#
			if list[0] == "get":
				# ls = connSock.recv(100)
				# print(ls)
				commandData = command

				connSizeStr = str(len(commandData))

				while len(connSizeStr) < 10:
					connSizeStr = "0" + connSizeStr

				
				commandData = connSizeStr + commandData

				numSent = 0

				while len(commandData) > numSent:
					numSent += connSock.send(commandData[numSent:].encode())

				#-----------------------------------------------------------
				# now to receive from the get command
				buffsize = 0
				filesize = 0

				buffsize = recvAll(connSock, 10)

				filesize = int(buffsize)

				data = recvAll(connSock, filesize)

				print("The file: ", str(list[1]), " was")
				print(data.split())
				print("\n Received ", str(filesize), " bytes")
				numReceived += filesize


			#
			# recieve what is currently is in the server by the 'ls' command
			#
			elif list[0] == "ls":

				commandData = command

				connSizeStr = str(len(commandData))

				while len(connSizeStr) < 10:
					connSizeStr = "0" + connSizeStr

				
				commandData = connSizeStr + commandData

				numSent = 0

				while len(commandData) > numSent:
					numSent += connSock.send(commandData[numSent:].encode())

				#--------------------------------------
				buffsize = 0
				filesize = 0

				buffsize = recvAll(connSock, 10)

				filesize = int(buffsize)

				data = recvAll(connSock, filesize)

				print(data)
				print("\n Received ", str(filesize), " bytes")
				numReceived += filesize

			#
			#
			#
			elif list[0] == "put":
				# TODO send data from the file.txt or other from here to the server... like the commented code here perhaps
				commandData = command
				#--------------------------------------	
					# # Open the file
				try:
					fileObj = open(list[1], "r")
				except:
					print("no valid file...")
					break

				fileData = fileObj.read()

				print("read file...")
				# to make sure we didn't hit eof
				if fileData:

					# conc. the command and the contents
					fileData = commandData + " " + fileData

					dataSizeStr = str(len(fileData))

					while len(dataSizeStr) < 10:
						dataSizeStr = "0" + dataSizeStr

					numSent = 0

					fileData = dataSizeStr + fileData

					while len(fileData) > numSent:
						numSent += connSock.send(fileData[numSent:].encode())

						# file has been sent...

				print("data sent...")
				print("Total data sent: ", str(numSent))
				num_sent += numSent

			else:
				connect = False
				print("Disconnecting...")


		elif connect is True:
			print("Invalid command...")


		elif connect is False:
			break



print("\n Data sent: ", str(num_sent))
print("Data received: ", str(numReceived))

# Close the socket and the file
connSock.close()
# fileObj.close()
	


