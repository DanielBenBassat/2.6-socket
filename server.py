import socket
import datetime
import random

MAX_PACKET = 4
IP = '0.0.0.0'
PORT = 1234
QUEUE_LEN = 1


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
                    print ("the message from client" + msg)

                    if msg != "EXIT":
                        client_socket.send(protocol_send(return_value(msg)).encode())
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
    main()
