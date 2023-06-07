from threading import Event
from worker import Worker
from listener import ASK_QUEUE_STATUS, PORT, Listener
import socket
from lockedQueue import lockedQueue

input_file = 'audio.mp3'

queue_progress = True

if queue_progress:
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', PORT)
        client_socket.connect(server_address)
        client_socket.sendall(ASK_QUEUE_STATUS.encode())
        response = client_socket.recv(1024)
        print('Received:', response.decode())
        client_socket.close()
    except ConnectionRefusedError:
        print("No server found, no jobs in queue")
else:
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', PORT)
        client_socket.connect(server_address)
        client_socket.sendall(input_file.encode())
        response = client_socket.recv(1024)
        print('Received:', response.decode())
        client_socket.close()
    except ConnectionRefusedError:
        event_shutdown = Event()
        shared_queue = lockedQueue()
        shared_queue.put(input_file)
        listener = Listener(shared_queue, event_shutdown)
        worker = Worker(shared_queue, event_shutdown)
        listener.start()
        worker.start()
    