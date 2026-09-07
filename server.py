import socket
from serialize import Serializer
from deserialize import Deserializer

HOST = "127.0.0.1"
PORT = 6379

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))

    server_socket.listen()
    print(f"Server is listening on port {HOST}:{PORT}...")

    while True:
        conn, addr = server_socket.accept()
        with conn:
            while True:
                print(f"Connected successfully by client at: {addr}")

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
                
                else:
                    response = Serializer("ERR unknown command").encode_error()

                conn.send(response.encode('utf-8'))

