import socket
import threading

HOST = "127.0.0.1"
PORT = 5050

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((HOST, PORT))

print("===================================")
print("       PYTHON CHAT CLIENT")
print("===================================")

username = input("Enter your username: ").strip()

if not username:
    username = "User"

# Send username to server
client.send(username.encode())

print("\nConnected to the chat!")
print("Type your message and press Enter.")
print("Type 'exit' to leave.\n")


def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()

            if not message:
                print("\nDisconnected from server.")
                break

            print(f"\n{message}")
            print("You: ", end="", flush=True)

        except ConnectionResetError:
            print("\nServer disconnected.")
            break

        except OSError:
            break


# Start background receiving thread
receive_thread = threading.Thread(
    target=receive_messages,
    daemon=True
)

receive_thread.start()


while True:
    try:
        message = input("You: ")

        if message.lower() == "exit":
            client.send("exit".encode())
            break

        if message.strip():
            client.send(message.encode())

    except (KeyboardInterrupt, EOFError):
        try:
            client.send("exit".encode())
        except:
            pass

        break

    except OSError:
        print("Connection lost.")
        break

client.close()