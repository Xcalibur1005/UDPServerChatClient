# UDPServerChatClient

Server Chat Application Based on UDP Socket based on python 2.7.12

Server Usage:
	python server.py -sp port

	server$ python ChatServer.py -sp 9090 (runs the server on port 9090)
	Server Initialized... 

Client Usage:
	python client.py -u username -sip server_ip -sp server_portnumber
	
	user$ python ChatClient.py -u Alice -sip server-ip -sp 9090
	+> Prompt message from user
	+> list 
	<– Signed In Users: Bob, Carole
	+> send Carole Hello this is Alice.
	<– <From IP:PORT:Carole>: Hi Alice! How are you
	+>
