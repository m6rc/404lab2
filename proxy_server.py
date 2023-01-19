import socket
from threading import Thread

BYTES_TO_READ = 4096

PROXY_SERVER_HOST = "localhost"
PROXY_SERVER_PORT = 8080

def send_request(host, port, request_data):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
		client_socket.connect((host,port))
		client_socket.send(request_data)
		client_socket.shutdown(socket.SHUT_WR)
		
		# Assemble response, be careful here, recall that recv(bytes) blocks until it recieves data!
		data = client_socket.recv(BYTES_TO_READ)
		result = b'' + data
		while len(data)>0:
			data = client_socket.recv(BYTES_TO_READ)
			result += data
		return result

def handle_conn(conn, addr):
	with conn:
		print(f"Connected by {addr}")

		request = b''
		while True:
			data=conn.recv(BYTES_TO_READ)
			if not data: # If the socket has been closed to further writes, break.
				break
			print(data) # Otherwise, print the data to the screen
			request += data
		response = send_request("www.google.com", 80, request) # and send it as a request to www.google.com
		conn.sendall(response) #return the response from www.google.com back to the client
			
def start_server():
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
		server_socket.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))
		server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server_socket.listen(2) #Allow queuing of up to 2 connections

		# Wait for an incomming connection, and when one arrives, accept it and 
        # create a new socket called 'conn' to interact with it.
		conn, addr = server_socket.accept()
		handle_conn(conn, addr)

def start_threaded_server():
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
		server_socket.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))
		server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server_socket.listen(2)
	
		while True:
			conn, addr = server_socket.accept()
			thread = Thread(target=handle_conn, args=(conn, addr))
			thread.run()
				
start_threaded_server()

# See active ports: lsof -nP | grep LISTEN
