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
from threading import Thread


def main():
    start_server()


def start_server():
    host = "127.0.0.1"
    # port = 8888
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire
    print("Socket created")
    # port = soc.getsockname()[1]
    # print('listening on port:', soc.getsockname()[1])

    try:
        soc.bind((host, 0))
    except:
        print("Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()

    soc.listen(5)       # queue up to 5 requests
    print("Socket now listening")
    print('listening on port:', soc.getsockname()[1])

    # infinite loop- do not reset for every requests
    while True:
        connection, address = soc.accept()
        ip, port = str(address[0]), str(address[1])
        print("Connected with " + ip + ":" + port)

        try:
            Thread(target=client_thread, args=(connection, ip, port)).start()
        except:
            print("Thread did not start.")
            traceback.print_exc()

    soc.close()


def client_thread(connection, ip, port, max_buffer_size = 5120):
    is_active = True

    while is_active:
        client_input = receive_input(connection, max_buffer_size)

        if "exit" in client_input:
            print("Client is requesting to disconnect")
            connection.close()
            print("Connection " + ip + ":" + port + " closed")
            is_active = False

        elif "dir" in client_input:
            directory = os.listdir()
            data = '\n'.join(directory)
            connection.sendall(data.encode("utf8"))
        
        elif "cd" in client_input:
            directory = client_input[3:]
            directory_name = os.path.realpath(directory)
            change_directory = os.chdir(directory_name)
            data = 'Directory Changed'
            connection.sendall(data.encode("utf8"))

        elif client_input[:8] == "download":
            filename = client_input[9:]
            if os.path.isfile(filename):
                with open(filename, 'rb') as file_to_send:
                    bytesToSend = file_to_send.read(5120)
                    connection.sendall(bytesToSend)
                    while bytesToSend != "":
                        if bytesToSend != "":
                            break
                        bytesToSend = file_to_send.read(5120)
                        connection.sendall(bytesToSend)
        
        elif client_input[:6] == "create":
            filename = client_input[7:]
            open(filename, 'w+')
            msg = 'File Created' 
            connection.sendall(msg.encode("utf8"))

        elif client_input[:4] == "read":
            filename = client_input[5:]
            f = open(filename, 'rb')
            if f.mode == 'rb':
                data = f.read()
                connection.sendall(data)
        
        elif client_input[:6] == "update":
            filename = client_input[5:]
            f = open(filename, 'a')
            msg = "File Opened!"
            connection.sendall(msg.encode("utf8"))
            data = f.write(client_input)
            msg1 = 'File Updated'
            # if f.mode == 'rb':
            #     data = f.read()
            connection.sendall(msg1.encode("utf8"))

        else:
            print("Processed result: {}".format(client_input))
            connection.sendall(client_input.encode("utf8"))


def receive_input(connection, max_buffer_size):
    client_input = connection.recv(max_buffer_size)
    client_input_size = sys.getsizeof(client_input)

    if client_input_size > max_buffer_size:
        print("The input size is greater than expected {}".format(client_input_size))

    decoded_input = client_input.decode("utf8").rstrip()  # decode and strip end of line
    return decoded_input

if __name__ == "__main__":
    main()