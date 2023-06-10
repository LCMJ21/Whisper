from whisper_spln.listener import ASK_QUEUE_STATUS, PORT
import socket
import pickle
import subprocess
import sys
import os


def runWhisper(input_file, dest_folder, inputLang, outputLang):
    dict = {
        "filename": input_file,
        "output_lang": outputLang,
        "dest_folder": dest_folder,
        "input_lang": inputLang
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
        script_dir = os.path.dirname(os.path.abspath(__file__))
        error_log_path = os.path.join(script_dir, 'conf/error.log')
        output_log_path = os.path.join(script_dir, 'conf/output.log')
        subprocess.Popen(
            ["python3", "whisper_spln/startThreads.py"] + sys.argv[1:], stdout=open(output_log_path, "w"), stderr=open(error_log_path, "w"))


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


def getLogs():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    error_log_path = os.path.join(script_dir, 'conf/error.log')
    output_log_path = os.path.join(script_dir, 'conf/output.log')

    with open(error_log_path, 'r') as file:
        error_text = file.read()
    with open(output_log_path, 'r') as file:
        output_text = file.read()

    print('App Logs\n\nOUTPUT:')
    print(output_text)
    print('\nERROR:')
    print(error_text)


def clearLogs():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    error_log_path = os.path.join(script_dir, 'conf/error.log')
    output_log_path = os.path.join(script_dir, 'conf/output.log')

    with open(error_log_path, 'w') as file:
        file.close()
    with open(output_log_path, 'w') as file:
        file.close()

    print('The application logs were cleared!')
