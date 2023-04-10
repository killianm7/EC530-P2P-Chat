import socket
import threading
from pymongo import MongoClient
from datetime import datetime
# from encryption import encrypt_message, decrypt_message

connected_clients = []

client = MongoClient('mongodb+srv://killianm:VXnjHFL9nRTAFaYF@cluster0.tgc659u.mongodb.net/test')

def handle_client(client_socket, addr):
    while True:
        msg = client_socket.recv(1024)
        if not msg or msg.decode() == "X":
            break

        # encrypted_msg = client_socket.recv(1024)
        # if not encrypted_msg:
        #     break
        
        # if len(encrypted_msg) > 0:
        #     decrypted_msg = decrypt_message(encrypted_msg)

        for client in connected_clients:
            if client != client_socket:
                client.send(msg)
                # client.send(encrypted_msg)

        print(f"Message from {addr}: {msg}")

        upload_to_mongodb("P2P", "Messages", {"Message": msg.decode()}, {"Address": addr}, {"Time (EST)": datetime.now()})

    client_socket.close()
    connected_clients.remove(client_socket)
    print(f"Connection from {addr} has closed.")

def upload_to_mongodb(database_name, collection_name, documents, user_info, date):
    db = client[database_name]
    collection = db[collection_name]

    result = collection.insert_one({**documents, **user_info, **date})
    # print(f"Inserted {result.inserted_id} messages into {database_name}.{collection_name}")

def main():
    host = input("Enter the server IP address: ")
    port = int(input("Enter the port #: "))

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