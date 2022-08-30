import pickle
import socket
import uuid


BUFFER_SIZE = 2048
HOST = '127.0.0.1'
PORT_1 = 8000
PORT_2 = 8001


try:
    client_id = str(uuid.uuid1())
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT_1))
    print(f"Connected successfully to the port {PORT_1}")

    client_socket.send(str.encode(str(client_id)))
    client_code = client_socket.recv(BUFFER_SIZE).decode('utf-8')

    client_socket.detach()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT_2))
    print(f"Connected successfully to the port {PORT_2}")

    message = input('Your message: ')
    to_send = pickle.dumps([client_id, client_code, message])
    client_socket.send(to_send)
    # response = client_socket.recv(BUFFER_SIZE).decode('utf-8')
    print("The message was logged.")

    client_socket.close()
except socket.error as e:
    print(str(e))



































# import pickle
# import socket
# import uuid
#
#
# BUFFER_SIZE = 2048
# HOST = '127.0.0.1'
# PORT_1 = 8000
# PORT_2 = 8001
#
#
#
# client_id = str(uuid.uuid1())
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# try:
#     client_socket.connect((HOST, PORT_1))
#     print(f"Connected successfully to the port {PORT_1}")
#
#     client_socket.send(str.encode(str(client_id)))
#     client_code = client_socket.recv(BUFFER_SIZE).decode('utf-8')
# except socket.error as e:
#     print(str(e))
#
#     client_socket.detach()
#
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client_socket.connect((HOST, PORT_2))
#     print(f"Connected successfully to the port {PORT_2}")
#
# message = input('Your message: ')
# to_send = pickle.dumps([client_id, client_code, message])
#
# try:
#     client_socket.send(to_send)
# except socket.error as e:
#     print(str(e))
#     # response = client_socket.recv(BUFFER_SIZE).decode('utf-8')
# else:
#     print("The message was logged.")
# finally:
#     client_socket.close()
