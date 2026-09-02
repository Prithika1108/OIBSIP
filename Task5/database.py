import sqlite3
import hashlib
from datetime import datetime


DATABASE = "chat.db"


def connect_db():
    return sqlite3.connect(DATABASE)


def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_name TEXT UNIQUE NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_name TEXT NOT NULL,
            username TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        hashed_password = hash_password(password)

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password)
        )

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


def login_user(username, password):
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()

    hashed_password = hash_password(password)

    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, hashed_password)
    )

    user = cursor.fetchone()

    conn.close()

    return user is not None


def save_message(room_name, username, message, timestamp):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO messages (room_name, username, message, timestamp)
        VALUES (?, ?, ?, ?)
        """,
        (room_name, username, message, timestamp)
    )

    conn.commit()
    conn.close()


def get_messages(room_name):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT username, message, timestamp
        FROM messages
        WHERE room_name = ?
        ORDER BY id ASC
        """,
        (room_name,)
    )

    messages = cursor.fetchall()

    conn.close()

    return messages


if __name__ == "__main__":
    create_tables()
    print("Database created successfully!")