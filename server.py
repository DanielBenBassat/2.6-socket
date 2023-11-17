import socket
import datetime
import random
import logging
import os

MAX_PACKET = 4
IP = '0.0.0.0'
PORT = 1234
QUEUE_LEN = 1
SERVER_NAME = "daniel's server"

LOG_FORMAT = '%(levelname)s | %(asctime)s | %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_DIR = 'log'
LOG_FILE = LOG_DIR + '/server.log'


def protocol_send(message):
    msg_len = len(message)
    final_msg = str(msg_len) + '!' + message
    return final_msg


def recieve_len_protocol(my_socket):
    current_char = ''
    len = ""
    current_char = my_socket.recv(1).decode()
    while current_char != '!':
        len += current_char
        current_char = my_socket.recv(1).decode()
    return int(len)

def time():
    hour = datetime.datetime.now().strftime("%H:%M:%S")
    return str(hour)


def name():
    return "daniel's server"


def rand():
    num = random.randint(1, 10)
    return str(num)


def return_value(msg):
    if msg == "TIME":
        return time()
    elif msg == "NAME":
        return name()
    elif msg == "RAND":
        return rand()
    else:
        return "enter again"





def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        my_socket.bind((IP, PORT))
        my_socket.listen(QUEUE_LEN)

        while True:
            client_socket, client_address = my_socket.accept()

            try:
                check = True
                while check:
                    msg = client_socket.recv(recieve_len_protocol(client_socket)).decode()
                    logging.debug("the server recieve " + msg)
                    if msg != "EXIT":

                        response= return_value(msg)
                        client_socket.send(protocol_send(response).encode())
                        logging.debug("the server sent " + protocol_send(response))
                    else:
                        check = False

            except socket.error as err:

                print('received socket error on client socket' + str(err))

            finally:
                print("client left")
                client_socket.close()

    except socket.error as err:
        print('received socket error on server socket' + str(err))

    finally:
        my_socket.close()


if __name__ == "__main__":

    assert name() == SERVER_NAME
    assert 0 < int(rand()) < 11

    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)
    logging.basicConfig(format=LOG_FORMAT, filename=LOG_FILE, level=LOG_LEVEL)

    main()
