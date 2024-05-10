import socket
import threading
from datetime import datetime


import rsa
from colorama import Fore


# public_key, private_key = rsa.newkeys(512)
public_key, private_key = None, None
client_socks = []


def receive_messages(sock):
    while True:
        try:
            encrypted_message = sock.recv(4096)
            if encrypted_message:
                # message = rsa.decrypt(encrypted_message, private_key).decode('utf-8')
                message = encrypted_message.decode('utf-8')
                print(f"{Fore.BLUE}{message}{Fore.RESET}")
        except Exception as e:
            print(f"Error receiving message: {e}")
            break


def send_messages(sock, name):
    while True:
        try:
            message = input('')
            time_now = datetime.now().strftime('%H:%M')
            full_message = f"{name} said at {time_now}:\n\t{message}"
            # encrypted_message = rsa.encrypt(full_message.encode('utf-8'), public_key)
            encrypted_message = full_message.encode('utf-8')
            sock.send(encrypted_message)
        except Exception as e:
            print(f"Error sending message: {e}")
            break


def send_and_distribute(name):
    while True:
        try:
            message = input('')
            time_now = datetime.now().strftime('%H:%M')
            full_message = f"{name} said at {time_now}:\n\t{message}"
            # encrypted_message = rsa.encrypt(full_message.encode('utf-8'), public_key)
            encrypted_message = full_message.encode('utf-8')
            for client_sock in client_socks:
                client_sock.send(encrypted_message)

        except Exception as e:
            print(f"Error receiving message: {e}")
            break


def distribute(message):
    while True:
        try:
            time_now = datetime.now().strftime('%H:%M')
            # encrypted_message = rsa.encrypt(full_message.encode('utf-8'), public_key)
            encrypted_message = message.encode('utf-8')
            for client_sock in client_socks:
                client_sock.send(encrypted_message)

        except Exception as e:
            print(f"Error receiving message: {e}")
            break


def receive_and_distribute(sock):
    while True:
        try:
            encrypted_message = sock.recv(4096)
            if encrypted_message:
                # message = rsa.decrypt(encrypted_message, private_key).decode('utf-8')
                message = encrypted_message.decode('utf-8')
                print(message)
            for client_sock in client_socks:
                # if client_sock == sock:
                #     continue
                client_sock.send(encrypted_message)

        except Exception as e:
            print(f"Error receiving message: {e}")
            break


def client(server_host, server_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((server_host, server_port))
        name = input("Enter your unique nickname: ")
        print("Connected to the server. Sending your nickname...")
        sock.send(name.encode('utf-8'))
        print("Nickname sent. You can start sending messages.")
        threading.Thread(target=receive_messages,
                         args=(sock,)).start()
        threading.Thread(target=(send_messages), args=(
            sock, name,)).start()
        print(f"{Fore.GREEN}-------------------- Chat started --------------------{Fore.RESET}")
    except Exception as e:
        # print(f"Failed to connect to an existing server: {e}")
        server(server_host, server_port)


def server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)
    print("There was no server on that port, so you've become the server!")

    name = input("Enter your unique nickname: ")
    threading.Thread(target=send_and_distribute, args=(name,)).start()

    names = set([name])
    while True:
        client_sock, client_addr = sock.accept()
        client_name = client_sock.recv(4096).decode('utf-8')
        if client_name in names:
            print(
                f"Client {client_name} is already in names, closing connection.")
            client_sock.close()
        else:
            names.add(client_name)
            print(f"Client {client_name} has successfully joined the chat with address {client_addr}")
            client_socks.append(client_sock)
            threading.Thread(target=receive_and_distribute, args=(client_sock,)).start()
            distribute(f"{client_name} joined the chat")


def main():
    server_host = 'localhost'
    # server_port = int(input("Enter the server port: "))
    server_port = 9999
    client(server_host, server_port)


if __name__ == '__main__':
    main()
