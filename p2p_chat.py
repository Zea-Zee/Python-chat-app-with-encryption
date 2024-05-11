import socket
import threading
from datetime import datetime
import os
import sys


import rsa


public_key, private_key = rsa.newkeys(512)

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


def receive_messages(sock):
    while True:
        try:
            encrypted_message = sock.recv(4096)
            if encrypted_message:
                # message = rsa.decrypt(encrypted_message, private_key).decode('utf-8')
                message = encrypted_message.decode('utf-8')
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
        # encrypted_message = rsa.encrypt(full_message.encode('utf-8'), public_key)
        encrypted_message = full_message.encode('utf-8')
        sock.send(encrypted_message)
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
        # encrypted_message = rsa.encrypt(full_message.encode('utf-8'), public_key)
        encrypted_message = message.encode('utf-8')
        for client_sock in client_socks.values():
            client_sock.send(encrypted_message)

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
        distribute(color_text(f"\t\t{client_name} has left the chat", ''))
    except Exception as e:
        print(f"Error cleaning up client {client_name}: {e}")


def receive_and_distribute(sock, client_name):
    distribute(color_text(f"\t\t{client_name} joined the chat", ''))
    while True:
        try:
            encrypted_message = sock.recv(4096)
            for client_sock in client_socks.values():
                if client_sock == sock:
                    continue
                message = encrypted_message.decode('utf-8')
                message = color_text(message, client_colors[client_name])
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
            msg = color_text(
                f"\tThere are {len(client_names)} people in that room", '')
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
    server_host = input("Enter the server ip:\n")
    server_port = int(input("Enter the server port:\n"))
    # server_port = 9999
    client(server_host, server_port)


if __name__ == '__main__':
    main()
