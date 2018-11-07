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

def main():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 8888

    try:
        soc.connect((host, port))
    except:
        print("Connection error")
        sys.exit()

    print("Enter 'quit' to exit")
    message = input(" -> ")

    if message == 'exit':
        soc.close()
        exit()

    while message != 'quit':
        soc.sendall(message.encode("utf8"))
        if soc.recv(5120).decode("utf8") == "hogaya":
            print("done")

            # pass        # null operation

        message = input(" -> ")

    soc.send(b'--quit--')

if __name__ == "__main__":
    main()