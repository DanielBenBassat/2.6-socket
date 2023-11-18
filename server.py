import socket
import datetime
import random
import logging
import os

IP = '0.0.0.0'
PORT = 1234
QUEUE_LEN = 1
SERVER_NAME = "daniel's server"

LOG_FORMAT = '%(levelname)s | %(asctime)s | %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_DIR = 'log'
LOG_FILE = LOG_DIR + '/server.log'


def protocol_send(message):
    """
    the function receives msg and returns its length and ! and the message
    :param message: message that will be sent:
    :return: the length and ! and the original message
    """
    msg_len = len(message)
    final_msg = str(msg_len) + '!' + message
    return final_msg


def receive_len_protocol(my_socket):
    """
    check the length of the message that will be received
    :param my_socket:
    :return: the length of message
    """
    received_len = ""
    current_char = my_socket.recv(1).decode()
    while current_char != '!':
        received_len += current_char
        current_char = my_socket.recv(1).decode()
    return int(received_len)


def time():
    """
    returns the exact time
    """
    hour = datetime.datetime.now().strftime("%H:%M:%S")
    return str(hour)


def name():
    """
    returns the server's name
    """
    return "daniel's server"


def rand():
    """
    returns random number from 1 to 10
    """
    num = random.randint(1, 10)
    return str(num)


def return_value(msg):
    """
    receive a message and call its function
    :param msg: the function that the client had sent
    :return: call function
    """
    if msg == "TIME":
        return time()
    elif msg == "NAME":
        return name()
    elif msg == "RAND":
        return rand()


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
                    msg = client_socket.recv(receive_len_protocol(client_socket)).decode()
                    logging.debug("the server receive " + msg)
                    if msg != "EXIT":
                        response = return_value(msg)
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
    assert protocol_send("daniel") == "6!daniel"
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)
    logging.basicConfig(format=LOG_FORMAT, filename=LOG_FILE, level=LOG_LEVEL)

    main()
