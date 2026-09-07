import socket

HOST = "127.0.0.1"
PORT = 6379

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))

    server_socket.listen()
    print(f"Server is listening on port {HOST}:{PORT}...")

    conn, addr = server_socket.accept()

    with conn:
        print(f"Connected successfully by client at: {addr}")

        # read data from connection
        data = conn.recv(1024) 

        if not data:
            print("Client disconnected without sending data")
        else:
            print(f"Received data from client: {data.decode('utf-8')}")

