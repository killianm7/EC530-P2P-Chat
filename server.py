import socket
import threading
from encryption import encrypt_message, decrypt_message

connected_clients = []

def handle_client(client_socket, addr):
    while True:
        encrypted_msg = client_socket.recv(1024)
        if not encrypted_msg:
            break

        decrypted_msg = decrypt_message(encrypted_msg)

        for client in connected_clients:
            if client != client_socket:
                client.send(encrypted_msg)

        print(f"Message from {addr}: {decrypted_msg}")

    client_socket.close()
    connected_clients.remove(client_socket)

def main():
    host = input("Enter the server IP address: ")
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print("Server is listening...")

    while True:
        client_socket, addr = server_socket.accept()
        connected_clients.append(client_socket)
        print(f"Connection from {addr}")

        threading.Thread(target=handle_client, args=(client_socket, addr)).start()

if __name__ == "__main__":
    main()