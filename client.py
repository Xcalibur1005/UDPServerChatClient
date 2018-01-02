#!/usr/bin/python

import socket, sys, threading, pickle, re

shutdown_event = threading.Event()

def ClientThread(ip, port):
	clientchatrecv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	clientchatrecv.bind((ip, port))
	print "\033[1;32m[+] Client listening on " + str(port) + "\033[1;m"
	while True:
		data, conn = clientchatrecv.recvfrom(4096)
		sender_name, message = data.split(":")
		print "\033[1;34m<- <From " + str(conn[0]) + ":" + str(conn[1]) + ":" + str(sender_name) + ">: \033[1;32m" + "\033[1;33m" + str(message) + "\033[1;m"
		inputprompt()


def usage():
	print "\033[1;32m[!] Usage: python chatclient.py -u username -sip server_ip -sp server_port\033[1;m"
	print "\033[1;32m[!] Example: python chatclient.py -u Alice -sip 192.168.203.199 -sp 9000\033[1;m"
	sys.exit("Arguments not specified. See the usage above")

def inputprompt():
	sys.stdout.write("+> ")
	sys.stdout.flush()

def main():
	if (len(sys.argv) != 7):
		usage()

	client_ip = '127.0.0.1'
	client_username = str(sys.argv[2])
	client_port = 7777
	client_info = "SIGN-IN: " + str(client_username) + " " + str(client_port)
	server_ip = str(sys.argv[4])
	server_port = int(sys.argv[6])
	client_info_dict = {}

	try:
		server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	except socket.error:
		print "\033[1;31m[+] Error creating socket connection\033[1;m"
		sys.exit()

	try:
		try:
			server.sendto(client_info,(server_ip,server_port))
			server.settimeout(5)
			data, conn = server.recvfrom(4096)
		except socket.timeout:
			print "\033[1;31m[!] Server not available. Exiting client.\033[1;m"
			sys.exit()
		t = threading.Thread(target=ClientThread, args=(client_ip, client_port))
                t.daemon = True
                t.start()
		print "\033[1;32m[+] Socket connection initiated\033[1;m"
		if data.find('Username already exists') != -1:
			print data
			sys.exit()
		else:
			while True:
				inputprompt()
				input = sys.stdin.readline()
				if input.find('logout') != -1:
					logout_data = "logout " + client_username
					server.sendto(logout_data,(server_ip,server_port))
					sys.exit()

				elif input.find('list') != -1:
					try:
						server.sendto(input,(server_ip,server_port))
						server.settimeout(2)
						data, conn = server.recvfrom(4096)
					except socket.timeout:
                                                print "\033[1;31m[!] Server not available. Exiting Client.\033[1;m"
                                                sys.exit()
					print "\033[1;34m<- Signed In Users: " + str(pickle.loads(data)) + "\033[1;m"

				elif (input.find('send') != -1):
					try:
						server.sendto(input,(server_ip,server_port))
						server.settimeout(2)
					except socket.timeout:
						print "\033[1;31m[!] Server not available. Exiting client.\033[1;m"
                                                sys.exit()

					command, peer, message = input.split(" ", 2)
					text = client_username + ":" + message
					data, conn = server.recvfrom(4096)
					client_info_dict[peer] = data
					ip = re.findall('(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})', data)
					port = re.findall('\d{4}', data)
					clientchatsend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
					clientchatsend.sendto(text,(str(ip[0]), int(port[0])))
				else:
					print "\033[1;31m[!] Invalid Command\033[1;m"
	except KeyboardInterrupt:
		print "\033[1;31m[-] Keyboard Interrupt Received. Exiting Program\033[1;m"
		t.join()
		sys.exit()

main()
