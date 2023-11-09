import socket

MAX_PACKET = 1024
IP = '0.0.0.0'
PORT = 1234
QUEUE_LEN = 1

def time():
    return 'TIME'
def name():
    return 'NAME'
def rand():
    return 'RAND'
def exit():
    return 'EXIT'


my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:

    my_socket.bind((IP, PORT))

    my_socket.listen(QUEUE_LEN)

    client_socket, client_address = my_socket.accept()

    try :

        msg = client_socket.recv(MAX_PACKET).decode()


        if msg == "TIME":
            client_socket.send(time().encode())
        elif msg == "NAME":
            client_socket.send(name().encode())
        elif msg == "RAND":
            client_socket.send(rand.encode())
        elif msg == "EXIT":
            client_socket.send(rand.encode())

    except socket.error as err:

        print('received socket error on client socket' + str(err))

    finally:

        my_socket.close()
        client_socket.close()

except socket.error as err:

    print('received socket error on server socket' + str(err))

finally:

    my_socket.close()
