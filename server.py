#!/usr/bin/python

import socket, sys, json, pickle

def usage():
	print "\033[1;32m[!] Usage: python chatserver.py -sp port\033[1;m"
	print "\033[1;32m[!] Exmaple: python chatserver.py -sp 9000\033[1;m"
	sys.exit("Arguments not specified. See the usage above")

if __name__ == '__main__':
	#Checking if arguments are supplied
	if (len(sys.argv) != 3):
		usage()

	#Defining variables
	server_port = int(sys.argv[2])

	#Creating dictionary to store 
	client_list = []
	client_info_dict = {}

	#Creating socket for client connection
	try:
		client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		client.bind(('127.0.0.1',server_port))
		print "\033[1;33m[+] Server Initialized...\033[1;m"
	except socket.error:
		print "\033[1;32m[-] Error creating socket connection\033[1;m"
		sys.exit()

	try:
		while True:
			#Receiving connections from client
			data, conn = client.recvfrom(4096)
			if data.find('SIGN-IN') != -1:
				command,client_name,client_port = data.split(" ")
				print command, client_name,client_port
				if (client_info_dict.has_key(client_name) == False):
					client_list.append(client_name)
					client_info_dict[client_name] = conn[0],client_port
					client.sendto("User virefied",(conn))
				else:
					client.sendto("Username already exists",(conn))

			elif (data.find('list') != -1):
				client.sendto(pickle.dumps(client_list),(conn))
			elif (data.find('send') != -1):
				command, requested_user, message = data.split(" ", 2)
				if requested_user not in client_list:
					client.sendto("Client not active",(conn))
				else:
					client.sendto(pickle.dumps(client_info_dict[requested_user]),(conn))
			elif (data.find('logout') != -1):
				command, client_username = data.split(" ")
				client_list.remove(client_username)
				client_info_dict.pop(client_username,0)
			else:
				sys.exit()
	except KeyboardInterrupt:
                print "\033[1;31m[-] Server exiting...\033[1;m"
		sys.exit(0)
