import socket
from threading import Thread

BYTES_TO_READ = 4096
HOST = "127.0.0.1"
PORT = 8080

def handle_connection(conn, addr):
	with conn:
		print(f"connected by: {addr}")
		while True:
			data=conn.recv(BYTES_TO_READ)
			if not data:
				break
			print(data)
			conn.send(data)
	return

def start_server():
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((HOST,PORT))
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # reuse address
		s.listen()
		conn, addr = s.accept()
		handle_connection(conn, addr)
	return

def start_threaded_server():
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((HOST,PORT))
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.listen(2)
	
		while True:
			conn, addr = s.accept()
			thread = Thread(target=handle_connection, args=(conn, addr))
			thread.run()
	
start_threaded_server()