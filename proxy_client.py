import socket

HOST = "www.google.com"
PORT = 80
BYTES_TO_READ = 4096

def get(host, port):
    # create request
	request_data = b'GET /  HTTP/1.1\nHost: www.google.com\n\n'
	
	# create socket
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((host,port))
		s.send(request_data)
		s.shutdown(socket.SHUT_WR)
		print("waiting for response")
		chunk = s.recv(BYTES_TO_READ)
		result = b'' + chunk
		while(len(chunk) > 0):
			chunk = s.recv(BYTES_TO_READ)
			result+=chunk
		s.close()
		return result
		
print(get(HOST,PORT))

