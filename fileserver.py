# import socket 
# import threading

# def HandleClient(sock):
#     msg = sock.recv(2048).decode('ascii')
#     print('From Client: ', msg)
#     sock.send('from server: OK'.encode('ascii'))
#     return 

# def Main():
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     ip = '127.0.0.1'
#     port = 5000
#     s.bind((ip, port))
#     s.listen()
#     print('Server Started')
#     print('IP Address of the Server::%s'%ip)
#     # threading.Thread( target = HandleClient, args = (s,)).start()

#     while True:
#         client, address = s.accept()
#         print('%s connected to the server:'%str(address))
#         msg = client.recv(2048).decode('ascii')
#         print('From Client: ', msg)
#         client.send('from server: OK'.encode('ascii'))
#     client.close()

# if __name__ == '__main__':
#     Main()
import socket
import sys
import traceback
import os
import pickle
import json
from threading import Thread, ThreadError

# config_file = {
#                   "Server_A": {
#                   "ip": "localhost",
#                   "port": 30000
#                   },
#                   "Server_B":  {
#                   "ip": "localhost",
#                   "port": 30001
#                   },
#                   "Server_C": {
#                   "ip": "localhost",
#                   "port": 30002
#                   }
#             }
def main():
    start_server()

def read_connection_from_config_file():
    f = open('configA.txt', 'r')
    dicte = json.load(f)
    connections = dicte['connections']
    sock = []
    for server, connection in connections.items():
        sock.append(connect_to_servers(connection['ip'],connection['port']))
    return sock

def connect_to_servers(host, port):
    try:
        sockets = socket.create_connection((host,port))
        print("Connected To Server")
        return sockets
    except:
        print("Connection error")
    

def start_server():
    host = "127.0.0.1"
    port = 30000
    try:
        sock = read_connection_from_config_file()
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.bind((host, port))
        print("Socket created")
        print("Socket now listening")
        print('listening on port:', soc.getsockname()[1])
        soc.listen(5)  
        while True:
            connection, address = soc.accept()
            ip, port = str(address[0]), str(address[1])
            print("Connected with " + ip + ":" + port)
            Thread(target=client_thread, args=(connection, ip, port)).start()
        # soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire
        
    except (socket.error, ThreadError) as e:
        print("Socket Error: " + str(e))
        sys.exit()

    # infinite loop- do not reset for every requests

def client_thread(connection, ip, port, max_buffer_size = 5120):
    is_active = True
    path = "root"
    while is_active:
        try:
            client_input = receive_input(connection, max_buffer_size)

            if "exit" in client_input[0]:
                print("Client is requesting to disconnect")
                connection.close()
                print("Connection " + ip + ":" + port + " closed")
                is_active = False
                break

            elif "ls" in client_input[0]:
                files_list = list_directory(path)
                data = pickle.dumps(files_list)
                connection.sendall(data)
            
            elif "mkdir" in client_input[0]:
                message = make_directory(client_input[1], client_input[2])
                connection.sendall(message.encode("utf8"))
            
            elif "mkfile" in client_input[0]:
                message = make_file(client_input[1], client_input[2])
                connection.sendall(message.encode("utf8"))

            # elif "cd" in client_input[0]:
            #     message = make_file(client_input[1], client_input[2])
            #     connection.sendall(message.encode("utf8"))
            
            # elif "cd" in client_input:
            #     directory = client_input[3:]
            #     directory_name = os.path.realpath(directory)
            #     change_directory = os.chdir(directory_name)
            #     data = 'Directory Changed'
            #     connection.sendall(data.encode("utf8"))

            # elif client_input[:8] == "download":
            #     filename = client_input[9:]
            #     if os.path.isfile(filename):
            #         with open(filename, 'rb') as file_to_send:
            #             bytesToSend = file_to_send.read(5120)
            #             connection.sendall(bytesToSend)
            #             while bytesToSend != "":
            #                 if bytesToSend != "":
            #                     break
            #                 bytesToSend = file_to_send.read(5120)
            #                 connection.sendall(bytesToSend)
            
            # elif client_input[:6] == "create":
            #     filename = client_input[7:]
            #     open(filename, 'w+')
            #     msg = 'File Created' 
            #     connection.sendall(msg.encode("utf8"))

            # elif client_input[:4] == "read":
            #     filename = client_input[5:]
            #     f = open(filename, 'rb')
            #     if f.mode == 'rb':
            #         data = f.read()
            #         connection.sendall(data)

            # elif client_input[:4] == "read":
            #     filename = client_input[5:]
            #     f = open(filename, 'rb')
            #     if f.mode == 'rb':
            #         data = f.read()
            #         connection.sendall(data)
            
            # elif client_input[:6] == "update":
            #     filename = client_input[5:]
            #     f = open(filename, 'a')
            #     msg = "File Opened!"
            #     connection.sendall(msg.encode("utf8"))
            #     data = f.write(client_input)
            #     msg1 = 'File Updated'
            #     # if f.mode == 'rb':
            #     #     data = f.read()
            #     connection.sendall(msg1.encode("utf8"))

            else:
                message = "Invalid Request"
                connection.sendall(message.encode("utf8"))
        except (ThreadError, socket.error) as e:
            print('Thread Error: {}'.format(e))
            connection.close()
            return

def receive_input(connection, max_buffer_size):
    client_input = connection.recv(max_buffer_size)
    client_input_size = sys.getsizeof(client_input)
    if client_input_size > max_buffer_size:
        print("The input size is greater than expected {}".format(client_input_size))

    decoded_input = pickle.loads(client_input)
    # decoded_input = client_input.decode("utf8").rstrip()  # decode and strip end of line
    return decoded_input


def list_directory(path):
    startpath = os.getcwd()
    root = startpath+'\\root'
    values = []
    path_component = {}
    for p in path:
        path_component = path.split('\\')
    f = open(root+'\\files.json', 'r')
    structure = json.load(f)
    dicte = {}
    for comp in path_component:
        if comp in structure.keys():
                structure = structure[comp]['children']
    for value in structure.keys():
        values.append(value)
    return values

def make_directory(folder_name, path):
    startpath = os.getcwd()
    root = startpath+'\\root'
    directory_structure = { folder_name: {
        'name':folder_name,
        'type':'directory',
        'children':{}
        }
    }
    path_component = {}
    for p in path:
        path_component = path.split('\\')
    with open(root+'\\files.json', 'r') as f:
        prev_structure = json.load(f)
    structure = prev_structure
    for comp in path_component:
        if comp in structure.keys():
                structure = structure[comp]['children']

    if folder_name in structure.keys():
        message = 'Folder Exists!'
    else:
        structure.update(directory_structure)
        message = "Directory Created"

    for key in prev_structure:
        if key in structure:         
            prev_structure[key].update(structure[key])

    with open(root+'\\files.json', 'w') as f:
        json.dump(prev_structure, f, indent=4)
    
    return message

def make_file(file_name, path):
    startpath = os.getcwd()
    root = startpath+'\\root'
    file_name = { file_name: {
        'name': file_name,
        'type':'file',
        }
    }
    
    path_component = {}
    for p in path:
        path_component = path.split('\\')
    with open(root+'\\files.json', 'r') as f:
        prev_structure = json.load(f)
    structure = prev_structure
    for comp in path_component:
        if comp in structure.keys():
                structure = structure[comp]['children']
    
    if file_name in structure.values():
        message = 'File Exists!'
    else:
        structure.update(file_name)
        message = "File Created"

    for key in prev_structure:
        if key in structure:         
            prev_structure[key].update(structure[key])

    with open(root+'\\files.json', 'w') as f:
        json.dump(prev_structure, f, indent=4)

    return message

if __name__ == "__main__":
    main()