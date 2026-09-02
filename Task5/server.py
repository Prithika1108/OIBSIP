import socket
import threading
from datetime import datetime
from database import create_tables, save_message, get_messages


HOST = "127.0.0.1"
PORT = 5050

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))
server.listen(2)

print("===================================")
print("       CHAT SERVER STARTED")
print("===================================")
print("Waiting for clients...")

clients = {}
lock = threading.Lock()


def get_time():
    return datetime.now().strftime("%H:%M")


def broadcast(message, sender=None):
    with lock:
        for client in list(clients.keys()):
            if client != sender:
                try:
                    client.send(message.encode())
                except:
                    pass

def handle_client(client, address):
    username = None

    try:
        # Receive username and room
        data = client.recv(1024).decode().strip()

        if "|" in data:
            username, room_name = data.split("|", 1)
        else:
            username = data
            room_name = "general"

        if not username:
            username = "User"

        with lock:
            clients[client] = username

        print(f"[{get_time()}] {username} connected.")

        # Notify other users
        join_message = f"[{get_time()}] {username} joined the chat."
        broadcast(join_message, client)

        # Send welcome message
        welcome_message = f"[{get_time()}] Welcome, {username}!"
        client.send(welcome_message.encode())
        # Send message history
        history = get_messages(room_name)

        for old_username, old_message, old_timestamp in history:
         history_message = f"[{old_timestamp}] {old_username}: {old_message}"
         client.send(history_message.encode())

        # Receive messages
        while True:
            data = client.recv(1024)

            if not data:
                break

            message = data.decode().strip()

            if message.lower() == "exit":
                break

            timestamp = get_time()
            save_message(room_name, username, message, timestamp)

            formatted_message = (
                f"[{get_time()}] {username}: {message}"
            )

            print(formatted_message)

            broadcast(formatted_message, client)

    except Exception as error:
        print(f"Error with {address}: {error}")

    finally:
        with lock:
            if client in clients:
                del clients[client]
        print(f"{username} disconnected.")

        if username:
            if username:
             leave_message = f"[{get_time()}] {username} disconnected."
            broadcast(leave_message, client)
            
        client.close()


# Start accepting clients
try:
    while True:
        client, address = server.accept()

        print(f"Connection received from {address}")

        thread = threading.Thread(
            target=handle_client,
            args=(client, address),
            daemon=True
        )

        thread.start()

except KeyboardInterrupt:
    print("\nServer shutting down...")

finally:
    server.close()