'''
Name : Muhammad Tariq Aijaz
ERP: 09827
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
import subprocess
from functools import reduce

# initialize socket and gets connected to server
def intialize_socket(host,port):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        soc.connect((host, port))
    except:
        print("Connection error")
        sys.exit()
    return soc

# main function
def main():
    # take IP as input.
    host = input(" -> IP: ")

    # take port as input.
    port = int(input(" -> Port: "))
    
    soc = intialize_socket(host,port)
    path = "root"
    while True:
        message = input(" -> ")
        new_message = message+' '+path
        messageList = message.split(' ') 

        # client closed.
        if messageList[0] == 'exit':
            soc.sendall(new_message.encode("utf8"))
            print("Client Closed")
            soc.close()
            sys.exit()

        # list down all the files and send it to client.
        elif messageList[0] == 'ls':
            soc.sendall(new_message.encode("utf8"))
            recv_files_list = soc.recv(5120)
            if recv_files_list == b'Invalid':
                print('Invalid')
            else:
                decoded_input = pickle.loads(recv_files_list)
                for files in decoded_input:
                    print(files)
            
        # makes new directory, updates directory structure and send the response to the client.    
        elif messageList[0] == "mkdir":
            if message[5:] == '':
                print('Invalid')
            else:
                soc.sendall(new_message.encode("utf8"))
                recv_message = soc.recv(5120).decode("utf8")
                print(recv_message)
        
        # makes new file, updates directory structure and send the response to the client.
        elif messageList[0] == "mkfile":
            if message[6:] == '':
                print('Invalid')
            else:
                soc.sendall(new_message.encode("utf8"))
                recv_message = soc.recv(5120).decode("utf8")
                print(recv_message)

        # change directory.
        elif messageList[0] == 'cd':
            if message[2:] == '':
                print('Invalid')
            else:
                soc.sendall(new_message.encode("utf8"))
                recv_path = soc.recv(5120).decode("utf8")
                path = recv_path
                print(recv_path)
        
        # downloads the file from server and send it to client.
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
                            f.write(recv_msg[4:])
                            f.close()
                    else:
                        print('Invalid')

        # uploads the file on server.
        elif messageList[0] == 'upload':
            startpath = os.getcwd()
            root = startpath+'\\root'
            if message[7:] == '':
                print('Invalid')
            else:
                try:
                    with open(root+'\\'+'Server_'+sys.argv[1]+'-Files'+'\\'+messageList[1], 'r') as f:
                        read_bytes = f.read(10000)
                    message = new_message+' '+read_bytes
                    soc.sendall(message.encode("utf8"))
                    recv_msg = soc.recv(10000).decode("utf8")
                    if recv_msg == 'Invalid':
                        print('Invalid')
                    elif recv_msg == 'File Exists!':
                        print('File Exists!')
                    else:
                        print(recv_msg)
                except:
                    print('No File Found')
        
        # opens the download file from the server in a seperated process.
        elif messageList[0] == 'open':
            if message[4:] == '':
                print('Invalid')
            else:
                startpath = os.getcwd()
                root = startpath+'\\root'
                try:
                    if messageList[1] != '':
                        subprocess.call(["notepad.exe", root+'\\'+'Server_'+sys.argv[1]+'-Files\\'+messageList[1]])
                    else:
                        print('No File Found')
                except:
                    print("No File Found!")
        
        # checks if input is invalid
        else:
            print('Invalid')
        
# main
if __name__ == "__main__":
    main()