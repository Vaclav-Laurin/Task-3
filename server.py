import logging
import os
import pickle
import socket
import _thread
import uuid


BUFFER_SIZE = 2048
HOST = "127.0.0.1"
LOG_PATH = os.path.join(os.path.dirname(__file__), "logs\sockets.log")
PORTS = [8000, 8001]

codes = []
threads = []
thread_counter = 0


# Creates a unique code for further client authentication
def generate_code(client_id):
    client_code = str(uuid.uuid1())
    codes.append(
        {
            "Client ID": client_id,
            "Client Code": client_code
        }
    )

    return client_code


def client_handler(client_socket):
    port = client_socket.getsockname()[1]
    response = client_socket.recv(BUFFER_SIZE)

    if port == PORTS[0]:
        client_id = response.decode('utf-8')
        client_socket.sendall(str.encode(str(generate_code(client_id))))
    elif port == PORTS[1]:
        data = pickle.loads(response)
        client_id, client_code, message = data
        address = client_socket.getpeername()
        log_message = f"Client address: {address[0]}:{address[1]} || Message: {message}"

        for item in codes:
            if client_id == item["Client ID"] and client_code == item["Client Code"]:
                logger.info(log_message)
                break
        else:
            raise socket.error(f"Client ID {client_id} does not match client code {client_code}.")

    client_socket.close()


def accept_connection(server_socket):
    global thread_counter
    thread_counter += 1
    client, address = server_socket.accept()

    print('Connected to: ' + address[0] + ':' + str(address[1]))
    print(f"Thread #{thread_counter}")
    _thread.start_new_thread(client_handler, (client, ))


def start_server():
    server_socket_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket_1.bind((HOST, PORTS[0]))
        server_socket_2.bind((HOST, PORTS[1]))
    except socket.error as e:
        print(str(e))
    print(f'Server is listing on the port {PORTS[0]}...')
    print(f'Server is listing on the port {PORTS[1]}...')
    server_socket_1.listen()
    server_socket_2.listen()

    while True:
        accept_connection(server_socket_1)
        accept_connection(server_socket_2)


# Check if directory exists. If not, create it
if not os.path.exists(os.path.dirname(LOG_PATH)):
    os.mkdir(os.path.dirname(LOG_PATH))

# Logger setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s || %(message)s")
file_handler = logging.FileHandler(filename=LOG_PATH, mode='a', encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

start_server()
