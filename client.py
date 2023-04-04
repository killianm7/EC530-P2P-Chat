import socket
import threading

def receive_messages(client_socket):
    while True:
        try: 
            msg = client_socket.recv(1024).decode('utf-8')
            if not msg:
                break
            print(msg)
        except Exception as e:
            print(f"Error: {e}")
            break

    client_socket.close()

def main():
    host = '127.0.0.1'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket))
    receive_thread.start()

    while True:
        msg = input()
        if msg == "X":
            break
        client_socket.send(msg.encode('utf-8'))

    client_socket.close()

if __name__ == "__main__":
    main()