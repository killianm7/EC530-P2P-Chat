import socket
import threading
from encryption import encrypt_message, decrypt_message

def receive_messages(server_socket):
    while True:
        encrypted_msg = server_socket.recv(1024)
        decrypted_msg = decrypt_message(encrypted_msg)
        print(f'\nReceived: {decrypted_msg}\n')

def main():
    host = input("Enter the server IP address: ")
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((host, port))

    threading.Thread(target=receive_messages, args=(server_socket,)).start()

    while True:
        message = input("Enter your message: ")
        encrypted_msg = encrypt_message(message)
        server_socket.send(encrypted_msg)

if __name__ == "__main__":
    main()