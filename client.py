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
    msg_len = len(message)
    final_msg = str(msg_len) + '!' + message
    return final_msg


def recieve_len_protocol(my_socket):
    len = ""
    current_char = my_socket.recv(1).decode()
    while current_char != '!':
        len += current_char
        current_char = my_socket.recv(1).decode()
    return int(len)


def valid_func(func):
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
                    response = my_socket.recv(recieve_len_protocol(my_socket)).decode()
                    logging.debug("the client recieve: " + response)
                    print(response)
                elif func == "EXIT":
                    check = False
            else:
                print("enter another func")

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
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)
    logging.basicConfig(format=LOG_FORMAT, filename=LOG_FILE, level=LOG_LEVEL)
    main()