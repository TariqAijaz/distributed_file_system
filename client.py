'''
Name : Muhammad Tariq Aijaz
Subject: Distributed Operating System
Instructor: Sir Shabbir Mukhi 

**CLIENT CODE**

'''
import socket
import sys
import os
import json
import sys
import dill
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

def main():
    host = input(" -> IP: ")
    port = int(input(" -> Port: "))
    soc = intialize_socket(host,port)
    path = "root"
    while True:
        message = input(" -> ")
        new_message = message+' '+path
        messageList = message.split(' ') 
        if messageList[0] == 'exit':
            soc.sendall(new_message.encode("utf8"))
            print("Client Closed")
            soc.close()
            sys.exit()

        elif messageList[0] == 'ls':
            print(new_message)

            soc.sendall(new_message.encode("utf8"))
            recv_files_list = soc.recv(5120)
            if recv_files_list == b'Invalid':
                print('Invalid')
            else:
                decoded_input = pickle.loads(recv_files_list)
                for files in decoded_input:
                    print(files)
            

        elif messageList[0] == "mkdir":
            if message[5:] == '':
                print('Invalid')
            else:
                soc.sendall(new_message.encode("utf8"))
                recv_message = soc.recv(5120).decode("utf8")
                print(recv_message)
        
        elif messageList[0] == "mkfile":
            if message[6:] == '':
                print('Invalid')
            else:
                soc.sendall(new_message.encode("utf8"))
                recv_message = soc.recv(5120).decode("utf8")
                print(recv_message)

        elif messageList[0] == 'cd':
            if message[2:] == '':
                print('Invalid')
            else:
                soc.sendall(new_message.encode("utf8"))
                recv_path = soc.recv(5120).decode("utf8")
                path = recv_path
                print(recv_path)
        
        elif messageList[0] == 'download':
            startpath = os.getcwd()
            root = startpath+'\\root'
            if message[8:] == '':
                print('Invalid')
            else:
                soc.sendall(new_message.encode("utf8"))
                recv_msg = soc.recv(10000).decode("utf8")
                if recv_msg == 'No File Found':
                    print('No File Found')
                else:
                    file_name = input('File Name: ')
                    if file_name is not None:
                        with open(root+'\\'+'Server_'+sys.argv[1]+'-Files'+'\\'+file_name+'.txt', 'w+') as f:
                            f.write(recv_msg)
                            f.close()
                    else:
                        print('Invalid')
        else:
            print('Invalid')
        

if __name__ == "__main__":
    main()