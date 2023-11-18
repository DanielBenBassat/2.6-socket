import socket
import logging
import os

IP = '127.0.0.1'
PORT = 1234

LOG_FORMAT = '%(levelname)s | %(asctime)s | %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_DIR = 'log'
LOG_FILE = LOG_DIR + '/client.log'


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


def valid_func(func):
    """
    received string and return true if its one of the four valid function and false if it is not
    """
    if func == "TIME" or func == "NAME" or func == "RAND" or func == "EXIT":
        return True
    return False


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        my_socket.connect((IP, PORT))
        check = True
        while check:
            func = input("enter a func")
            if valid_func(func):
                my_socket.send(protocol_send(func).encode())
                logging.debug("the client sent: " + protocol_send(func))
                if func != "EXIT":
                    response = my_socket.recv(receive_len_protocol(my_socket)).decode()
                    logging.debug("the client receive: " + response)
                    print(response)
                elif func == "EXIT":
                    check = False
            else:
                print("you can only enter one of these functions: TIME, NAME, RAND, EXIT")

    except socket.error as err:
        print('received socket error ' + str(err))

    finally:
        print("client left the server")
        my_socket.close()


if __name__ == "__main__":
    assert valid_func("TIME")
    assert valid_func("NAME")
    assert valid_func("RAND")
    assert valid_func("EXIT")
    assert protocol_send("daniel") == "6!daniel"
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)
    logging.basicConfig(format=LOG_FORMAT, filename=LOG_FILE, level=LOG_LEVEL)
    main()