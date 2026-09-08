import socket
import threading
import time
from serialize import Serializer
from deserialize import Deserializer

HOST = "127.0.0.1"
PORT = 6379

def resp(conn, addr, storage, expires):
    with conn:
        while True:
            # read data from connection
            data = conn.recv(1024) 
            if not data:
                break
            data_str = data.decode('utf-8')
            parsed = Deserializer(data_str).decoder_dispatch()

            command = parsed[0].lower()
            if command == "ping":
                response = Serializer("PONG").encode_str()
            elif command == "echo":
                message = parsed[1]
                response = Serializer(message).encode_bulk_string()

            elif command == "set":
                key = parsed[1]
                value = parsed[2]
                storage[key] = value

                if len(parsed) == 5:
                    time_value = int(parsed[4])
                    time_seconds = time.time() + time_value
                    expires[key] = time_seconds

                response = Serializer("OK").encode_str()

            elif command == "get":
                key = parsed[1]
                if key in expires:
                    time_seconds = expires[key]
                    if time.time() > time_seconds:
                        del expires[key]
                        del storage[key]
                        response = Serializer(None).encode_bulk_string()
                        
                if key in storage:
                    message = storage[key]
                    response = Serializer(message).encode_bulk_string()
                else:
                    response = Serializer(None).encode_bulk_string()
            else:
                response = Serializer("ERR unknown command").encode_error()

            conn.send(response.encode('utf-8'))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))

    server_socket.listen()
    print(f"Server is listening on port {HOST}:{PORT}...")

    storage = {}
    expires = {}

    while True:
        conn, addr = server_socket.accept()
        print(f"Connected successfully by client at: {addr}")
        
        # Create new thread
        new_thread = threading.Thread(target=resp, args=(conn, addr, storage, expires))
        new_thread.start()


