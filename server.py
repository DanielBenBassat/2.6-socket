import socket
import datetime
import random

MAX_PACKET = 1024
IP = '0.0.0.0'
PORT = 1234
QUEUE_LEN = 1

def time(client_socket):
    temp = datetime.datetime.now().strftime("%H:%M:%S")
    client_socket.send(temp.encode())
def name():
    return "daniel's server"
def rand():
    num = random.randint(1, 10)
    return num


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:

        my_socket.bind((IP, PORT))

        my_socket.listen(QUEUE_LEN)
        while True:
            client_socket, client_address = my_socket.accept()

            try:
                msg = client_socket.recv(MAX_PACKET).decode()


                if msg == "TIME":
                    client_socket.send(str(time(client_socket)).encode())
                elif msg == "NAME":
                    client_socket.send(name().encode())
                elif msg == "RAND":
                    client_socket.send(str(rand()).encode())
                elif msg == "EXIT":
                    check = False


            except socket.error as err:

                print('received socket error on client socket' + str(err))

            finally:
                client_socket.close()



    except socket.error as err:

        print('received socket error on server socket' + str(err))

    finally:
        my_socket.close()


if __name__ == "__main__":
    main()
