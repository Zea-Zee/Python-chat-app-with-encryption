import socket
import threading
from datetime import datetime
import os
import sys



client_names = set()
client_socks = {}
client_colors = {}
public_keys = {}


color_codes = {
    'BLUE': '\033[94m',
    'CYAN': '\033[96m',
    'GREEN': '\033[92m',
    'YELLOW': '\033[93m',
    'RED': '\033[91m'
}

available_color_codes = {
    'BLUE': '\033[94m',
    'CYAN': '\033[96m',
    'GREEN': '\033[92m',
    'YELLOW': '\033[93m',
    'RED': '\033[91m'
}

mode_codes = {
    'HEADER': '\033[95m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m',
    'RESET': '\033[0m'
}


def color_text(text, color):
    if color:
        return f"{color_codes[color]}{text}{mode_codes['RESET']}"
    return f"{mode_codes['BOLD']}{text}{mode_codes['RESET']}"



def decoder(data) :
    bits = [int(bit) for bit in data]
    tmp = 0
    while 2 ** tmp < len(bits):
        tmp += 1

    posision_error = 0

    bits_check = [2 ** i for i in range(tmp)]
    bits_check.reverse()
    for _, bit_check in enumerate(bits_check):
        check = 0
        for j in range(bit_check - 1, len(bits), bit_check * 2):
            check += sum(bits[j:j + bit_check])
        if check % 2 == 1:
            posision_error += bit_check


    if posision_error > 0:
        bits[posision_error - 1] = 1 - bits[posision_error - 1]


    decoded_data = ''.join(
        str(bit)
        for i, bit in enumerate(bits)
        if not (((i+1) & ((i+1) - 1)) == 0 and (i+1) != 0)
    )


    part = [decoded_data[i:i + 8] for i in range(0, len(decoded_data), 8)]
    str_binary = ' '.join(part)

    value_binary = str_binary.split()
    str_ascii = ''.join(chr(int(binary, 2)) for binary in value_binary)
    return str_ascii




def encoder(string):
    binary_str = ' '.join(format(ord(char), '08b') for char in string)
    binary_list = binary_str.split()
    connect_string = ''.join(binary_list)

    bits = [int(bit) for bit in connect_string]
    tmp = 0
    while 2 ** tmp < len(bits) + tmp + 1:
        tmp += 1

    result = [0] * (len(bits) + tmp)
    j = 0
    for i in range(len(result)):
        if i + 1 == 2 ** j:
            j += 1
        else:
            result[i] = bits.pop(0)

    for i in range(tmp):
        posision = 2 ** i - 1
        check = 0
        for j in range(posision, len(result), 2 * posision + 2):
            check ^= result[j:j + posision + 1].count(1) % 2
        result[posision] = check

    return ''.join([str(bit) for bit in result])


def receive_messages(sock):
    while True:
        try:
            encrypted_message = sock.recv(4096).decode('utf-8')
            if encrypted_message:

                message = decoder(encrypted_message)
                print(message)
                if message == "that nickname already taken, try again with another one" or message == "Room on that port is full, try another port":
                    os._exit(1)
        except Exception as e:
            print(f"Error receiving message: {e}")
            break


def send_message(sock, name, message, service=False):
    try:
        if service:
            full_message = message
        else:
            time_now = datetime.now().strftime('%H:%M')
            full_message = f"{name} said at {time_now}:\n   {message}"
        encrypted_message = encoder(full_message)
        # encrypted_message = full_message.encode('utf-8')
        sock.send(f"{encrypted_message}".encode('utf-8'))
    except Exception as e:
        print(f"Error sending message: {e}")


def send_messages(sock, name):
    while True:
        try:
            message = input('')
            # clear_last_line()
        except Exception as e:
            print(f"Error sending messages: {e}")
            break
        print(datetime.now().strftime('%H:%M'))
        send_message(sock, name, message)


def distribute(message):
    try:
        time_now = datetime.now().strftime('%H:%M')
        encrypted_message = message.encode('utf-8')
        for client_sock in client_socks.values():
            send_message(client_sock, 'server',
                         message, service=False)
            # client_sock.send(encrypted_message)

    except Exception as e:
        print(f"Error receiving message: {e}")


def handle_client_exit(sock, client_name):
    try:
        if client_name in client_socks:
            del client_socks[client_name]
        if client_name in client_names:
            client_names.remove(client_name)
        if client_name in client_colors and client_colors[client_name] in color_codes:
            available_color_codes[client_colors[client_name]
                                  ] = color_codes[client_colors[client_name]]
        sock.close()
        distribute(f"{client_name} has left the chat")
    except Exception as e:
        print(f"Error cleaning up client {client_name}: {e}")


def receive_and_distribute(sock, client_name):
    distribute(f"{client_name} joined the chat")
    while True:
        try:
            encrypted_message = sock.recv(4096)
            for client_sock in client_socks.values():
                if client_sock == sock:
                    continue
                message = encrypted_message.decode('utf-8')
                encrypted_message = message.encode('utf-8')
                client_sock.send(encrypted_message)

        except Exception as e:
            handle_client_exit(sock, client_name)
            break


def client(server_host, server_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((server_host, server_port))
        name = input("Enter your unique nickname: ")

        sock.send(name.encode('utf-8'))
        threading.Thread(target=receive_messages,
                         args=(sock,)).start()
        threading.Thread(target=(send_messages), args=(
            sock, name,)).start()
        print(color_text(
            '-------------------- Chat started --------------------', 'GREEN'))
    except Exception as e:
        # print(f"Failed to connect to an existing server: {e}")
        server(server_host, server_port)


def server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(6)
    # print("There was no server on that port, so you've become the server!")

    client(host, port)

    while True:
        client_sock, client_addr = sock.accept()
        client_name = client_sock.recv(4096).decode('utf-8')
        if client_name in client_names:
            send_message(client_sock, 'server',
                         "that nickname already taken, try again with another one", service=True)
            client_sock.close()
        elif not len(available_color_codes):
            send_message(client_sock, 'server',
                         "Room on that port is full, try another port", service=True)
            client_sock.close()
        else:
            msg = f"There are {len(client_names)} people in that room"
            # msg = color_text(
            #     f"There are {len(client_names)} people in that room", '')
            send_message(client_sock, 'server',
                         msg, service=True)
            client_names.add(client_name)
            client_colors[client_name] = list(available_color_codes.keys())[-1]
            del available_color_codes[client_colors[client_name]]
            # print(f"{client_name} color is {client_colors[client_name]}, remain colors: {available_color_codes}")
            # print(f"Client {client_name} has successfully joined the chat with address {client_addr}")
            client_socks[client_name] = client_sock
            threading.Thread(target=receive_and_distribute,
                             args=(client_sock, client_name,)).start()


def main():
    # server_host = input("Enter the server ip:\n")
    server_port = int(input("Enter the server port:\n"))
    server_host = "127.0.0.1"
    # server_port = 5632
    client(server_host, server_port)


if __name__ == '__main__':
    main()
