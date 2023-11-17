import socket

MAX_PACKET = 1024
IP = '127.0.0.1'
PORT = 1234


def protocol_send(message):
    msg_len = len(message)
    final_msg = str(msg_len) + '!' + message
    return final_msg


def recieve_len_protocol(my_socket):
    current_char = ''
    len = ""
    current_char= my_socket.recv(1).decode()
    while current_char != '!':
        len += current_char
        current_char = my_socket.recv(1).decode()
    return my_socket.recv(int(len)).decode()


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        my_socket.connect((IP, PORT))
        check = True
        while check:
            func = input("enter a func")
            my_socket.send(protocol_send(func).encode())
            print ("msg sent")
            if func != "EXIT":
                response = recieve_len_protocol(my_socket)
                print(response)
            elif func == "EXIT":
                check = False

    except socket.error as err:
        print('received socket error ' + str(err))

    finally:
        print("client left the server")
        my_socket.close()


if __name__ == "__main__":
    main()