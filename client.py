# import socket
# import threading
# import os
# # def RecvMsgThread(sock):
# #     message = sock.recv(2048).decode('ascii')
# #     print(message)
# #     return 

# def Main():
#     ip = input('Enter IP -> ')
#     port = 5000
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.connect((ip, port))
#     # threading.Thread( target = RecvMsgThread, args = (s,)).start()
#     while True:
#         message = input('Send message to server -> ')
#         s.send(message.encode('ascii'))
#         msg = s.recv(2048).decode('ascii')
#         print(msg)
#     s.close()

# if __name__ == '__main__':
#     Main()

import socket
import sys
import os
import json
import pickle
import pprint
from functools import reduce

def intialize_socket(host,port):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        soc.connect((host, port))
    except:
        print("Connection error")
        sys.exit()
    return soc

# def get_directory_structure(rootdir):
#     """
#     Creates a nested dictionary that represents the folder structure of rootdir
#     """
#     dir = {}
#     rootdir = rootdir.rstrip(os.sep)
#     start = rootdir.rfind(os.sep) + 1
#     for path, dirs, files in os.walk(rootdir):
#         dirs[:] = [d for d in dirs if d not in ['_pycache_','.git']]
#         folders = path[start:].split(os.sep)
#         value = {'Type':'F', 'Version': 1}
#         subdir = dict.fromkeys(files, value)
#         parent = reduce(dict.get, folders[:-1], dir)
#         #print(parent)
#         parent[folders[-1]] = subdir
#     return dir


def main():
    host = input(" -> IP: ")
    port = int(input(" -> Port: "))

    soc = intialize_socket(host,port)

    # filess = {}
    # dictionary = {}

    # BASE_PATH = os.path.realpath(os.getcwd())
    # print(BASE_PATH)
    # filess = get_directory_structure(BASE_PATH)

    # host = 'localhost'
    # port = 30000
    # connections = {'30001' : {'ip':'127.0.0.0','port':30001}, '30002' : {'ip':'127.0.0.0','port':30002}}

    # thing = BASE_PATH+'/config.txt'
    # print(thing)
    # dictionary = {'host' : host, 'port' : port, 'connections':connections}

    # with open(thing, 'w') as fp:
    #     json.dump(dictionary, fp, indent=4)

    # with open(BASE_PATH+'/files.txt', 'w') as f:
    #     json.dump(filess, f, indent=4)


    # with open(thing, 'r') as fp:
    #     data = json.load(fp)
    #     print(str(data))

    # print(filess)
    # print(dictionary)
    path = "root"
    while True:
        message = input(" -> ")
        if message == 'exit':
            commands = []
            commands.append(message)
            data = pickle.dumps(commands)
            soc.sendall(data)
            print("Client Closed")
            soc.close()
            sys.exit()

        elif message == 'ls':
            commands = []
            commands.append(message)
            commands.append(path)
            data = pickle.dumps(commands)
            soc.sendall(data)
            recv_files_list = soc.recv(5120)
            decoded_input = pickle.loads(recv_files_list)
            for files in decoded_input:
                print(files)

        elif message[:5] == "mkdir":
            commands = []
            commands.append(message[:5])
            commands.append(message[6:])
            commands.append(path)
            data = pickle.dumps(commands)
            soc.sendall(data)
            recv_message = soc.recv(5120).decode("utf8")
            print(recv_message)
        
        elif message[:6] == "mkfile":
            commands = []
            commands.append(message[:6])
            commands.append(message[7:])
            commands.append(path)
            data = pickle.dumps(commands)
            soc.sendall(data)
            recv_message = soc.recv(5120).decode("utf8")
            print(recv_message)

        # elif message[:2] == 'cd':
        #     soc.sendall(message.encode("utf8"))
        #     recv_input = soc.recv(5120).decode("utf8")
        #     print(recv_input)

        # elif message[:8] == "download":
        #     filename = message[9:]
        #     soc.sendall(message.encode("utf8"))
        #     with open("new_"+filename, 'wb') as file_to_write:
        #         data = soc.recv(5120).decode("utf8")
        #         if not data:
        #             break
        #         file_to_write.write(data.encode())
        #         print("Download Complete")
        #         file_to_write.close()

        # elif message[:6] == "create":
        #     soc.sendall(message.encode("utf8"))
        #     recv_input = soc.recv(5120).decode("utf8")
        #     print(recv_input)
        
        # elif message[:4] == "read":
        #     soc.sendall(message.encode("utf8"))
        #     recv_input = soc.recv(5120).decode("utf8")
        #     print(recv_input)   

        # elif message[:6] == "update":
        #     soc.sendall(message.encode("utf8"))
        #     recv_input = soc.recv(5120).decode("utf8")
        #     print(recv_input)   

        #     data = input("-> Enter Data in the file: ")
        #     soc.sendall(data.encode("utf8"))
        #     recv_input1 = soc.recv(5120).decode("utf8")
        #     print(recv_input1)   

        else:
            commands = []
            commands.append(message[:])
            data = pickle.dumps(commands)
            soc.sendall(data)
            recv_input = soc.recv(5120).decode("utf8")
            print(recv_input)

if __name__ == "__main__":
    main()