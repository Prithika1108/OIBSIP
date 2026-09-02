# Task 5 - Real-Time Chat Application

## Objective

Build a real-time messaging application in Python using socket programming
and threading.

## Technologies Used

- Python
- Socket Programming
- TCP/IP
- Threading
- Datetime

## Features

- Server listens for incoming client connections
- Client connects to the server
- Two users can communicate in real time
- Bidirectional message exchange
- Username support
- Timestamped messages
- Join notifications
- Graceful disconnection handling
- Runs on the same computer using localhost

## Project Structure

```text
chatapp_task5/
│
├── server.py
├── client.py
└── README.md


## How to Run
Step 1 - Start the server

Open a terminal in the project folder and run:
python server.py
The server will display:

CHAT SERVER STARTED
Waiting for clients...

Step 2 - Start Client 1

Open another terminal and run:

python client.py

Enter a username when requested.
Example:

prithika

Step 3 - Start Client 2

Open another terminal and run:

python client.py

Enter another username.

Example:

bob

Example
[10:30] prithika connected.
[10:31] bob connected.

[10:31] prithika: Hello Bob
[10:31] bob: Hello Prithika

[10:32] bob disconnected.

## Networking Details

The application uses TCP sockets.

Server:

Host: 127.0.0.1
Port: 5050

127.0.0.1 refers to the local computer.

The server waits for clients using listen() and accepts connections
using accept().

The client connects using connect().

## Threading

Threading is used so that messages can be received in the background
while the user can continue sending messages.
Graceful Disconnection

When a user types:

exit

the client disconnects and the server informs the other connected user.

Security Note

This beginner version is designed for learning socket programming.

Messages are transmitted through a TCP connection but are not
end-to-end encrypted.

The application is intended to run locally using 127.0.0.1.

## Implemented Features

Graphical user interface
User registration and login
SQLite database
Multiple chat rooms
Persistent message history
Emoji support
Notifications
Password hashing
Improved security


## Security and Data Storage

- User registration details are stored in a SQLite database.
- Chat messages are stored in the SQLite database as message history.
- Messages are transmitted through a Python socket connection.
- The current application does not use end-to-end encryption (E2EE).
- Passwords should be protected appropriately in a production application.
- This project is intended for learning and demonstration purposes and should not be considered production-secure.
