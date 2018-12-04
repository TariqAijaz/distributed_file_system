'''
Name : Muhammad Tariq Aijaz
Subject: Distributed Operating System
Instructor: Sir Shabbir Mukhi 

**SERVER CODE**

'''
import socket
import sys
import traceback
import os
import pickle
import dill
import json
import uuid 
import time
from threading import Thread, ThreadError

server_socket = [None, None]

def main():
    start_server()

def read_connection_from_config_file():
    global server_socket
    f = open('config'+sys.argv[1]+'.json', 'r')
    dicte = json.load(f)
    connections = dicte['connections']
    while True:
        all_connected = True
        for server_sockets in server_socket:
            if server_sockets is None:
                all_connected = False
                break
        if all_connected == False:
            index = 0
            for server, connection in connections.items():
                    if server_socket[index] == None:
                        server_socket[index] = connect_to_servers(connection['ip'],connection['port'], index)
                    index = index + 1

def listen_on_socket(sockets, index):
    try:
        if sockets is not None:
            sockets.recv(10000)
    except:
        print('server has disconnected')
        server_socket[index] = None

def connect_to_servers(host, port, index):
    try:
        sockets = socket.create_connection((host,port))
        print("Connected To Server")
        Thread(target=listen_on_socket, args=(sockets, index, )).start()
        return sockets
    except:
        print("Connection error")
    
def start_server():
    host = "127.0.0.1"
    port = 30002
    try:
        Thread(target=read_connection_from_config_file).start()
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
        # sys.exit()


def client_thread(connection, ip, port, max_buffer_size = 10000):
    is_active = True
    path = "root"
    while is_active:
        try:
            data_input = receive_input(connection, max_buffer_size)
            if data_input is not None:
                client_input = data_input.split(' ')
                if "exit" in client_input[0]:
                    print("Client is requesting to disconnect")
                    connection.close()
                    print("Client Connection " + ip + ":" + port + " closed")
                    is_active = False
                    break
                
                elif "ls" in client_input[0]:
                    if client_input[1] != "":                    
                        files_list = list_directory(client_input[1])
                        data = pickle.dumps(files_list)
                        connection.sendall(data)
                    else:
                        message = 'Invalid'
                        connection.sendall(message.encode("utf8"))
                
                elif "mkdir" in client_input[0]:
                    if client_input[1] != "" and client_input[2] != "":
                        message = make_directory(client_input[1], client_input[2])
                        connection.sendall(message.encode("utf8"))
                    else:
                        message = 'Invalid'
                        connection.sendall(message.encode("utf8"))
                    if message == 'Directory Created':
                        message = 'Update_dir'
                        startpath = os.getcwd()
                        root = startpath+'\\root'
                        for socks in server_socket:
                            if socks is not None:
                                with open(root+'\\files'+sys.argv[1]+'.json', 'r') as f:
                                    bytesToSend = f.read(10000)
                                command = message+" "+bytesToSend
                                socks.sendall(command.encode("utf8"))

                elif "mkfile" in client_input[0]:
                    if client_input[1] != "" and client_input[2] != "":
                        path = client_input[2] 
                        message = make_file(client_input[1], client_input[2], 'Server_'+sys.argv[1])
                        connection.sendall(message[0].encode("utf8"))
                    else:
                        message = 'Invalid'
                        connection.sendall(message.encode("utf8"))
                    file_name = message[1]
                    if message[0] == 'File Created':
                        message = 'Update_file'
                        startpath = os.getcwd()
                        root = startpath+'\\root'
                        for socks in server_socket:
                            if socks is not None:
                                with open(root+'\\files'+sys.argv[1]+'.json', 'r') as f:
                                    bytesToSend = f.read(10000)
                                command = message+" "+bytesToSend
                                socks.sendall(command.encode("utf8"))
                        msg = 'Replicate_file'
                        for socks in server_socket:
                            if socks is not None:
                                command = msg+" "+path+" "+file_name
                                socks.sendall(command.encode("utf8"))

                elif "cd" in client_input[0]:
                    if client_input[1] != "" and client_input[2] != "":
                        message = change_directory(client_input[1], client_input[2])
                        connection.sendall(message.encode("utf8"))
                    else:
                        message = 'Invalid'
                        connection.sendall(message.encode("utf8"))
                
                elif "Update_dir" in client_input[0]:
                    startpath = os.getcwd()
                    root = startpath+'\\root'
                    with open(root+'\\files'+sys.argv[1]+'.json', 'w') as f:
                        f.write(data_input[11:])
                
                elif "Update_file" in client_input[0]:
                    startpath = os.getcwd()
                    root = startpath+'\\root'
                    with open(root+'\\files'+sys.argv[1]+'.json', 'w') as f:
                        f.write(data_input[12:])
                
                elif "Replicate_file" in client_input[0]:
                    startpath = os.getcwd()
                    root = startpath+'\\root'
                    path = client_input[1]
                    file_name = client_input[2]
                    len1 = len(client_input[0])
                    len2 = len(file_name)
                    len3 = len(path)
                    total_len = len1 + len2 + len3 + 3

                    with open(root+'\\files'+sys.argv[1]+'.json', 'r') as f:
                        prev_structure = json.load(f)
                    structure = prev_structure
                    id = uuid.uuid1()
                    unique_name = id.int
                    server_name = { 'Server_'+sys.argv[1]: {
                        'name': str(unique_name)
                        }
                    }
                    path_component = {}
                    for p in path:
                        path_component = path.split('\\')
                    for comp in path_component:
                        if comp in structure.keys():
                            structure = structure[comp]['children']
                    
                    for file_names in structure.keys():
                        if file_name in file_names:
                            structure = structure[file_name]['mappings']
                    structure.update(server_name)
                    msg = "updated rep"
                    print(msg)
                    with open(startpath+'\\'+'Server_'+sys.argv[1]+'\\'+str(unique_name)+'.txt', 'w+') as f:
                        f.write(data_input[total_len:])

                    for key in prev_structure:
                        if key in structure:         
                            prev_structure[key].update(structure[key])

                    with open(root+'\\files'+sys.argv[1]+'.json', 'w') as f:
                        json.dump(prev_structure, f, indent=4)

                    time.sleep(5)
                    message = 'add_entry'
                    for socks in server_socket:
                        if socks is not None:
                            send_command = message+" "+path+" "+file_name+" "+'Server_'+sys.argv[1]+" "+str(unique_name)
                            socks.sendall(send_command.encode('utf8'))
                
                elif "add_entry" in client_input[0]:
                    print(client_input)
                    startpath = os.getcwd()
                    root = startpath+'\\root'
                    
                    path = client_input[1]
                    file_name = client_input[2]
                    server = client_input[3]
                    unique_name = client_input[4]
                    
                    server_name = { server: {
                            'name': unique_name
                            }
                        }

                    with open(root+'\\files'+sys.argv[1]+'.json', 'r') as f:
                        prev_structure = json.load(f)
                    structure = prev_structure
                    path_component = {}
                    for p in path:
                        path_component = path.split('\\')
                    for comp in path_component:
                        if comp in structure.keys():
                            structure = structure[comp]['children']
                    for file_names in structure.keys():
                        if file_name in file_names:
                            structure = structure[file_name]['mappings']
                    structure.update(server_name)
                    msg = "updated add"
                    print(msg)
                    print(structure)
                    for key in prev_structure:
                        if key in structure:         
                            prev_structure[key].update(structure[key])
                    
                    with open(root+'\\files'+sys.argv[1]+'.json', 'w') as f:
                        json.dump(prev_structure, f, indent=4)

                elif "download" in client_input[0]:
                    file = True
                    if client_input[1] != "" and client_input[2] != "":
                        file_name = client_input[1] 
                        path = client_input[2] 
                        startpath = os.getcwd()
                        root = startpath+'\\root'
                        path_component = {}
                        for p in path:
                            path_component = path.split('\\')
                        with open(root+'\\files'+sys.argv[1]+'.json', 'r') as f:
                            prev_structure = json.load(f)
                        structure = prev_structure
                        for comp in path_component:
                            if comp in structure.keys():
                                structure = structure[comp]['children']
                        for file_names in structure.keys():
                            if file_name in file_names:
                                print(file_name)
                                structure = structure[file_name]['mappings']
                                for server, file in structure.items():
                                    print(file)
                                    if file['name'] is not None:
                                        if 'Server_'+sys.argv[1] == server:
                                            with open(startpath+'\\'+'Server_'+sys.argv[1]+'\\'+file['name']+'.txt', 'r') as f:
                                                file_read = f.read(4096)
                                            send_msg = 'file'+file_read
                                            connection.sendall(send_msg.encode("utf8"))  
                                            print('file send')
                                            break
                            else:
                                file = False
                        if file == False:
                            msg = 'No File Found'
                            connection.sendall(msg.encode("utf8"))
                    else:
                        message = 'No File Found'
                        connection.sendall(message.encode("utf8"))
                
                elif "upload" in client_input[0]:
                    upload = False
                    file_name = client_input[1] 
                    path = client_input[2]
                    startpath = os.getcwd()
                    root = startpath+'\\root'
                    if client_input[1] != "" and client_input[2] != "":
                        len1 = len(client_input[0])
                        len2 = len(file_name)
                        len3 = len(path)
                        total_len = len1 + len2 + len3 + 3
                        id = uuid.uuid1()
                        unique_name = id.int 
                        file_structure = {
                            file_name: {
                                'name': file_name,
                                'type':'file',
                                'mappings': {
                                    'Server_'+sys.argv[1]: {
                                        'name': str(unique_name)
                                    }
                                }
                            }
                        }
                        for p in path:
                            path_component = path.split('\\')
                        with open(root+'\\files'+sys.argv[1]+'.json', 'r') as f:
                            prev_structure = json.load(f)
                        structure = prev_structure
                        for comp in path_component:
                            if comp in structure.keys():
                                structure = structure[comp]['children']
                        if file_name in structure.keys():
                            msg = 'File Exists!'
                            connection.sendall(msg.encode("utf8"))
                        else:
                            structure.update(file_structure)
                            for key in prev_structure:
                                if key in structure:         
                                    prev_structure[key].update(structure[key])
                            with open(root+'\\files'+sys.argv[1]+'.json', 'w') as f:
                                json.dump(prev_structure, f, indent=4)
                            with open(startpath+'\\'+'Server_'+sys.argv[1]+'\\'+str(unique_name)+'.txt', 'w+') as f:
                                f.write(data_input[total_len:])
                            message = 'Uploaded'
                            upload = True
                            connection.sendall(message.encode("utf8"))

                        if upload == True:
                            message = 'Update_file'
                            startpath = os.getcwd()
                            root = startpath+'\\root'
                            for socks in server_socket:
                                if socks is not None:
                                    with open(root+'\\files'+sys.argv[1]+'.json', 'r') as f:
                                        bytesToSend = f.read(10000)
                                    command = message+" "+bytesToSend
                                    socks.sendall(command.encode("utf8"))
                            msg = 'Replicate_file'
                            for socks in server_socket:
                                if socks is not None:
                                    command = msg+" "+path+" "+file_name+" "+data_input[total_len:]
                                    socks.sendall(command.encode("utf8"))

                    else:
                        message = 'Invalid'
                        connection.sendall(message.encode("utf8"))
                        
                else:
                    message = "Invalid Request"
                    connection.sendall(message.encode("utf8"))
            else:
                message = "Invalid Request"
                connection.sendall(message.encode("utf8"))
        except (ThreadError, socket.error) as e:
            print('Client Thread Error: {}'.format(e))
            connection.close()
            return

def receive_input(connection, max_buffer_size):
    try:
        client_input = connection.recv(max_buffer_size)
        client_input_size = sys.getsizeof(client_input)
        if client_input_size > max_buffer_size:
            print("The input size is greater than expected {}".format(client_input_size))
        decoded_input = client_input.decode("utf8")
        return decoded_input
    except Exception as e:
        print('Receive Input Error: {}'.format(e))

def list_directory(path):
    startpath = os.getcwd()
    root = startpath+'\\root'
    values = []
    path_component = {}
    for p in path:
        path_component = path.split('\\')
    f = open(root+'\\files'+sys.argv[1]+'.json', 'r')
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
    with open(root+'\\files'+sys.argv[1]+'.json', 'r') as f:
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
        with open(root+'\\files'+sys.argv[1]+'.json', 'w') as f:
            json.dump(prev_structure, f, indent=4)
    return message

def make_file(file_name, path, server):
    id = uuid.uuid1()
    unique_name = id.int
    startpath = os.getcwd()
    name = file_name
    root = startpath+'\\root'
    file_structure = {
        file_name: {
            'name': file_name,
            'type':'file',
            'mappings': {
                server : {
                    'name': str(unique_name)
                }
            }
        }
    }
    path_component = {}
    for p in path:
        path_component = path.split('\\')
    with open(root+'\\files'+sys.argv[1]+'.json', 'r') as f:
        prev_structure = json.load(f)
    structure = prev_structure
    for comp in path_component:
        if comp in structure.keys():
            structure = structure[comp]['children']
    message = []
    if file_name in structure.keys():
        msg = 'File Exists!'
        message.append(msg)
    else:
        structure.update(file_structure)
        msg = "File Created"
        message.append(msg)
        for key in prev_structure:
            if key in structure:         
                prev_structure[key].update(structure[key])
        with open(root+'\\files'+sys.argv[1]+'.json', 'w') as f:
            json.dump(prev_structure, f, indent=4)
        f = open(startpath+'\\'+server+'\\'+str(unique_name)+'.txt', 'w+')
    message.append(name)
    return message

def change_directory(directory_name, path):
    directory = list_directory(path)
    if directory_name in directory:
        new_path = path+'\\'+directory_name
        return new_path 
    else:
        message = 'Directory not found'
        return message

if __name__ == "__main__":
    main()