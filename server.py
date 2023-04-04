import socket
import threading

def handle_client(client_socket, addr):
    while True:
        try:
            msg = client_socket.recv(1024).decode('utf-8')
            if not msg:
                break
            print(f"{addr}: {msg}")
        except Exception as e:
            print(f"Error: {e}")
            break

    client_socket.close()

def main():
    host = '127.0.0.1'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Server listening on {host}:{port}\n")

    print(f"Type 'X' to exit chat\n")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

if __name__ == "__main__":
    main()