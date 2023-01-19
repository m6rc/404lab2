import socket

HOST = 'www.google.com'
PORT = 80
BYTES_TO_READ = 4096

def get(host, port):
	# create request
	request_data = b'GET /  HTTP/1.1\nHost:'+host.encode('utf-8') + b'\n\n'

	# create socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# send data on socket
	s.connect((host,port))
	s.send(request_data)
	s.shutdown(socket.SHUT_WR)

	# listen for response
	response = s.recv(BYTES_TO_READ)
	while(len(response) > 0):
		print(response)
		response = s.recv(BYTES_TO_READ)
	s.close()

get(HOST,PORT)
