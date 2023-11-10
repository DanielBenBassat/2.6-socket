import socket

MAX_PACKET = 1024
IP= '127.0.0.1'
PORT = 1234

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    my_socket.connect((IP, PORT))
    check= True
    while check:

        func= input("enter a func")
        my_socket.send(func.encode())
        if func != "EXIT":
            response = my_socket.recv(MAX_PACKET).decode()
            print (response)
        elif func == "EXIT":
            check= False




except socket.error as err:

    print('received socket error ' + str(err))

finally:

    my_socket.close()