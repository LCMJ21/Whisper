from whisper_spln.listener import ASK_QUEUE_STATUS, PORT
import socket
import pickle
import subprocess
import sys


def runWhisper(input_file, dest_folder, inputLang, outputLang):
    dict = {
        "filename": input_file,
        "outputLang": outputLang,
    }
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', PORT)
        client_socket.connect(server_address)

        send_request = pickle.dumps(dict)
        client_socket.sendall(send_request)
        response = client_socket.recv(1024)
        print('Received:', response.decode())
        client_socket.close()
    except ConnectionRefusedError:
        subprocess.Popen(
            ["python3", "whisper_spln/startThreads.py", " ".join(sys.argv[1:])], stdout=open("output.log", "w"), stderr=open("error.log", "w"))


def getQueue():
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
