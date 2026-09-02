import tkinter as tk
from tkinter import messagebox
import socket
import threading
from database import login_user, register_user, get_messages

EMOJIS = {
    ":smile:": "😄",
    ":heart:": "❤️",
    ":thumbsup:": "👍",
    ":laughing:": "😆",
    ":fire:": "🔥",
    ":sad:": "😢",
    ":wink:": "😉",
    ":grin:": "😁",
    ":angry:": "😠",
    ":clap:": "👏"
}

HOST = "127.0.0.1"
PORT = 5050

client = None
username = ""
def show_chat_window():
    global client

    chat_window = tk.Toplevel(window)
    chat_window.title("Python Chat Application")
    chat_window.geometry("700x600")

    # Close chat window properly
    def close_chat():
        global client

        try:
            if client:
                client.shutdown(socket.SHUT_RDWR)
                client.close()
        except:
            pass

        client = None
        chat_window.destroy()

    chat_window.protocol("WM_DELETE_WINDOW", close_chat)

    # Chat display area
    chat_area = tk.Text(
        chat_window,
        state="disabled"
    )
    chat_area.pack(
        padx=10,
        pady=10,
        fill="both",
        expand=True
    )

    # Message frame
    message_frame = tk.Frame(chat_window)
    message_frame.pack(
        side="bottom",
        fill="x",
        padx=10,
        pady=10
    )

    # Message entry
    message_entry = tk.Entry(message_frame)
    message_entry.pack(
        side="left",
        fill="x",
        expand=True
    )

    # Send message
    def send_message():
        message = message_entry.get().strip()

        if not message:
            return

        # Convert emoji shortcodes
        for shortcode, emoji in EMOJIS.items():
            message = message.replace(shortcode, emoji)

        try:
            client.send(message.encode("utf-8"))
            message_entry.delete(0, tk.END)

        except Exception as error:
            messagebox.showerror(
                "Send Error",
                f"Could not send message.\n{error}"
            )

    # Send button
    send_button = tk.Button(
        message_frame,
        text="Send",
        command=send_message
    )
    send_button.pack(
        side="right",
        padx=(10, 0)
    )

    # Press Enter to send
    message_entry.bind(
        "<Return>",
        lambda event: send_message()
    )

    # Notification for new messages
    def show_notification(message):
        if chat_window.focus_displayof() is None:
            messagebox.showinfo(
                "New Message",
                message,
                parent=chat_window
            )

    # Receive messages
    def receive_messages():
        while True:
            try:
                data = client.recv(4096)

                if not data:
                    break

                message = data.decode("utf-8")

                chat_area.config(state="normal")
                chat_area.insert(tk.END, message + "\n")
                chat_area.config(state="disabled")
                chat_area.see(tk.END)

                chat_window.after(
                    0,
                    show_notification,
                    message
                )

            except:
                break

    # Start receiving messages in background
    threading.Thread(
        target=receive_messages,
        daemon=True
    ).start()
def connect_to_server(room_name):
    global client

    try:
        client = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        client.connect((HOST, PORT))

        client.send(
            f"{username}|{room_name}".encode()
        )

        messagebox.showinfo(
            "Connected",
            f"Connected to room: {room_name}"
        )

        show_chat_window()

    except Exception as error:
        messagebox.showerror(
            "Connection Error",
            f"Could not connect to server.\n\n{error}"
        )


def join_room():
    room_name = room_entry.get().strip()

    if not room_name:
        messagebox.showwarning(
            "Warning",
            "Please enter a chat room name."
        )
        return

    room_window.destroy()

    connect_to_server(room_name)


def show_room_window():
    global room_window
    room_window = tk.Toplevel(window)

    room_window.title("Chat Rooms")
    room_window.geometry("450x300")

    tk.Label(
        room_window,
        text="Enter Chat Room",
        font=("Arial", 18, "bold")
    ).pack(pady=30)

    global room_entry

    room_entry = tk.Entry(
        room_window,
        width=30
    )
    room_entry.pack(pady=10)

    tk.Button(
        room_window,
        text="Join Room",
        command=join_room,
        width=15
    ).pack(pady=20)


def login():
    global username

    username_value = username_entry.get().strip()
    password_value = password_entry.get()

    if not username_value or not password_value:
        messagebox.showwarning(
            "Warning",
            "Please enter username and password."
        )
        return

    if login_user(username_value, password_value):
        username = username_value

        messagebox.showinfo(
            "Login Successful",
            f"Welcome, {username}!"
        )

        show_room_window()

    else:
        messagebox.showerror(
            "Login Failed",
            "Invalid username or password."
        )


def register():
    username_value = username_entry.get().strip()
    password_value = password_entry.get()

    if not username_value or not password_value:
        messagebox.showwarning(
            "Warning",
            "Please enter username and password."
        )
        return

    if register_user(username_value, password_value):
        messagebox.showinfo(
            "Registration Successful",
            "Account created successfully."
        )
    else:
        messagebox.showerror(
            "Registration Failed",
            "Username already exists."
        )


# Main login window
window = tk.Tk()
window.title("Chat Application Login")
window.geometry("450x400")


tk.Label(
    window,
    text="Python Chat Application",
    font=("Arial", 24, "bold")
).pack(pady=30)


tk.Label(
    window,
    text="Username"
).pack()

username_entry = tk.Entry(
    window,
    width=25
)
username_entry.pack(pady=5)


tk.Label(
    window,
    text="Password"
).pack()

password_entry = tk.Entry(
    window,
    width=25,
    show="*"
)
password_entry.pack(pady=5)


button_frame = tk.Frame(window)
button_frame.pack(pady=25)


tk.Button(
    button_frame,
    text="Register",
    command=register,
    width=12
).pack(
    side="left",
    padx=5
)


tk.Button(
    button_frame,
    text="Login",
    command=login,
    width=12
).pack(
    side="left",
    padx=5
)


window.mainloop()