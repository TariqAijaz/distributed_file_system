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
    # downloadDir = "E:/IBA-CS FALL 2018 (CS-8)/Distributed Operating System/final_project"

    soc = intialize_socket(host,port)

    while True:
        message = input(" -> ")
        if message == 'exit':
            soc.sendall(message.encode("utf8"))
            print("Client Closed")
            soc.close()
            sys.exit()

        elif message == 'dir':
            soc.sendall(message.encode("utf8"))
            recv_input = soc.recv(5120).decode("utf8")
            print(recv_input)
        
        elif message[:2] == 'cd':
            soc.sendall(message.encode("utf8"))
            recv_input = soc.recv(5120).decode("utf8")
            print(recv_input)

        elif message[:8] == "download":
            filename = message[9:]
            soc.sendall(message.encode("utf8"))
            with open("new_"+filename, 'wb') as file_to_write:
                data = soc.recv(5120).decode("utf8")
                if not data:
                    break
                file_to_write.write(data.encode())
                print("Download Complete")
                file_to_write.close()

        elif message[:6] == "create":
            soc.sendall(message.encode("utf8"))
            recv_input = soc.recv(5120).decode("utf8")
            print(recv_input)
        
        elif message[:4] == "read":
            soc.sendall(message.encode("utf8"))
            recv_input = soc.recv(5120).decode("utf8")
            print(recv_input)   

        elif message[:6] == "update":
            soc.sendall(message.encode("utf8"))
            recv_input = soc.recv(5120).decode("utf8")
            print(recv_input)   

            data = input("-> Enter Data in the file: ")
            soc.sendall(data.encode("utf8"))
            recv_input1 = soc.recv(5120).decode("utf8")
            print(recv_input1)   

        else:
            soc.sendall(message.encode("utf8"))
            recv_input = soc.recv(5120).decode("utf8")
            print(recv_input)

if __name__ == "__main__":
    main()