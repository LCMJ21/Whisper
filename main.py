from threading import Event
from worker import Worker
from listener import ASK_QUEUE_STATUS, PORT, Listener
import socket
from lockedQueue import lockedQueue
import argparse

def main(input_file, queue_progress, dest_folder, inputLang, outputLang):
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
            # TODO run this procees in background
    

class QueueAction(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        return super().__init__(option_strings, dest, nargs=0, default=argparse.SUPPRESS, **kwargs)
    
    def __call__(self, parser, namespace, values, option_string, **kwargs):
        main(None, True, None, None, None)
        parser.exit()

# Create an ArgumentParser object
parser = argparse.ArgumentParser(
    prog= 'AudioToText',
    description= 'Converts an audio file to text file.',
    epilog= 'Made for SPLN 2022/2023'
)

# Add arguments
parser.add_argument('input_file', type=str, help='Path to the file with the audio')
parser.add_argument('-d', '--dest', type=str, default='', help='Path for the output file')
parser.add_argument('-il', '--inputLang', type=str, default='pt', help='Language of the input file')
parser.add_argument('-ol', '--outputLang', type=str, default='pt', help='Language of the output text')
parser.add_argument('-q', '--queue', action=QueueAction, help='Show the audio conversion queue')

# Parse the command-line arguments
args = parser.parse_args()

# Access the values of the arguments
input_file = args.input_file
dest_folder = args.dest
inputLang = args.inputLang
outputLang = args.outputLang

main(input_file, False, dest_folder, inputLang, outputLang)
