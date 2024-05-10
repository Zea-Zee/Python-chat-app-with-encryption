import socket
import threading
from datetime import datetime


import rsa


# public_key, private_key = rsa.newkeys(512)
public_key, private_key = None, None


def receive_messages(sock, private_key):
    while True:
        try:
            encrypted_message = sock.recv(4096)
            if encrypted_message:
                # message = rsa.decrypt(encrypted_message, private_key).decode('utf-8')
                message = encrypted_message.decode('utf-8')
                print(message)
        except Exception as e:
            print(f"Error receiving message: {e}")
            break


def send_messages(sock, name, public_key):
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


def client(server_host, server_port, alias, public_key):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((server_host, server_port))
        print("Connected to the server. Sending alias...")
        sock.send(alias.encode('utf-8'))
        print("Alias sent. You can start sending messages.")
        threading.Thread(target=receive_messages,
                         args=(sock, private_key)).start()
        threading.Thread(target=send_messages, args=(
            sock, alias, public_key)).start()
    except Exception as e:
        # print(f"Failed to connect to an existing server: {e}")
        server(alias, server_host, server_port, public_key)


def server(name, host, port, public_key):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)
    print("There was no server on that port, so you've become the server!")
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
            threading.Thread(target=receive_messages, args=(client_sock, private_key)).start()
            threading.Thread(target=send_messages, args=(client_sock, client_name, public_key)).start()


def main():
    alias = input("Enter your unique alias: ")
    server_host = 'localhost'
    server_port = int(input("Enter the server port: "))
    client(server_host, server_port, alias, public_key)


print('bebra')

if __name__ == '__main__':
    main()
else:
    print('el bebra')
