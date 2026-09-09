import socket
import threading
import time
import json
from serialize import Serializer
from deserialize import Deserializer

HOST = "127.0.0.1"
PORT = 6379
FILENAME = "dump.json"

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

            elif command == "exists":
                key = parsed[1]
                if key in storage:
                    response = Serializer(1).encode_integer()
                else:
                    response = Serializer(0).encode_integer()

            elif command == "del":
                count = 0
                for i in range(1, len(parsed)):
                    if parsed[i] in storage:
                        del storage[parsed[i]]
                        count += 1
                        if parsed[i] in expires:
                            del expires[parsed[i]]
                response = Serializer(count).encode_integer()

            elif command == "incr" or command == "decr":
                counter = parsed[1]
                if command == "incr":
                    step = +1

                elif command == "decr":
                    step = -1

                if counter in storage:
                    currentval = storage[counter]
                    try:
                        conversion = int(currentval)
                        conversion += step
                        storage[counter] = str(conversion)
                        response = Serializer(storage[counter]).encode_integer()
                    except:
                        response = Serializer("Invalid: current value is not a digit").encode_error()

                else:
                    count = 0
                    count += step
                    storage[counter] = str(count)
                    response = Serializer(storage[counter]).encode_integer()

            elif command == "rpush" or command == "lpush":
                collection = parsed[1]
                flag = True
                if collection not in storage:
                    currentlist = []
                elif not isinstance(storage[collection], list):
                    response = Serializer("WRONGTYPE Operation against a key holding the wrong kind of value").encode_error()
                    flag = False
                else:
                    currentlist = storage[collection]

                if flag:
                    for i in range(2, len(parsed)):
                        if command == 'rpush':
                            currentlist.append(parsed[i])
                        elif command == 'lpush':
                            currentlist.insert(0, parsed[i]) 
                
                    storage[collection] = currentlist

                    response = Serializer(len(storage[collection])).encode_integer() 

            elif command == "save":
                try:
                    with open(FILENAME, 'w') as f:
                        json.dump(storage, f) 
                        response = Serializer("OK").encode_str() 
                except Exception as e:
                    response = Serializer("Error saving to file").encode_error()
            else:
                response = Serializer("ERR unknown command").encode_error()

            conn.send(response.encode('utf-8'))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))

    server_socket.listen()
    print(f"Server is listening on port {HOST}:{PORT}...")

    storage = {}
    expires = {}

    try:
        with open(FILENAME, 'r') as f:
            data = json.load(f)
            storage.update(data)
    except FileNotFoundError:
        pass


    while True:
        conn, addr = server_socket.accept()
        print(f"Connected successfully by client at: {addr}")
        
        # Create new thread
        new_thread = threading.Thread(target=resp, args=(conn, addr, storage, expires))
        new_thread.start()


