from threading import Thread, Event
import socket

from whisper_spln.lockedQueue import lockedQueue

PORT = 9999
ASK_QUEUE_STATUS = "ASK_QUEUE_STATUS"


class Listener(Thread):
    def __init__(self, shared_queue : lockedQueue, event_shutdown : Event):
        Thread.__init__(self)
        self.shared_queue = shared_queue
        self.event_shutdown = event_shutdown
    
    def run(self):
        self.listen()

    def listen(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', PORT)
        server_socket.bind(server_address)
        server_socket.listen(1)
        server_socket.settimeout(10)
        while not self.event_shutdown.is_set():
            try:
                client_socket, client_address = server_socket.accept()
                print('Connected by', client_address)
                request = client_socket.recv(1024).decode()
                response = self.handle_request(request)
                client_socket.sendall(response.encode())
                client_socket.close()
            except socket.timeout:
                pass

        # Close the connection
        server_socket.close()

    def handle_request(self, request):
        if request == ASK_QUEUE_STATUS:
            return f"{self.shared_queue.all_items()}"
        else:
            self.shared_queue.put(request)
            return 'Response from server ...'
