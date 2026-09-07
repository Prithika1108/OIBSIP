import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime


# ---------------- DATABASE ----------------

def create_database():
    try:
        connection = sqlite3.connect("bmi_records.db")
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bmi_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                weight REAL NOT NULL,
                height REAL NOT NULL,
                bmi REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL
            )
        """)

        connection.commit()
        connection.close()

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Could not create database.\n{error}"
        )


# ---------------- BMI CALCULATION ----------------

def calculate_bmi():
    username = username_entry.get().strip()
    weight_text = weight_entry.get().strip()
    height_text = height_entry.get().strip()

    if not username:
        messagebox.showerror(
            "Invalid Input",
            "Please enter a user name."
        )
        return

    if not weight_text or not height_text:
        messagebox.showerror(
            "Invalid Input",
            "Please enter both weight and height."
        )
        return

    try:
        weight = float(weight_text)
        height = float(height_text)

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Weight and height must be numeric values."
        )
        return

    if weight <= 0 or height <= 0:
        messagebox.showerror(
            "Invalid Input",
            "Weight and height must be greater than zero."
        )
        return

    bmi = weight / (height ** 2)

    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    bmi_result_label.config(
        text=f"BMI: {bmi:.2f}"
    )

    category_label.config(
        text=f"Category: {category}"
    )

    save_bmi_record(
        username,
        weight,
        height,
        bmi,
        category
    )


# ---------------- SAVE RECORD ----------------

def save_bmi_record(username, weight, height, bmi, category):
    try:
        connection = sqlite3.connect("bmi_records.db")
        cursor = connection.cursor()

        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO bmi_records
            (username, weight, height, bmi, category, date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            username,
            weight,
            height,
            bmi,
            category,
            date
        ))

        connection.commit()
        connection.close()

        status_label.config(
            text="BMI calculated and record saved successfully."
        )

        load_history(username)

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Could not save BMI record.\n{error}"
        )


# ---------------- LOAD HISTORY ----------------

def load_history(username):
    history_list.delete(0, tk.END)

    try:
        connection = sqlite3.connect("bmi_records.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT weight, height, bmi, category, date
            FROM bmi_records
            WHERE username = ?
            ORDER BY id DESC
        """, (username,))

        records = cursor.fetchall()

        connection.close()

        for record in records:
            weight, height, bmi, category, date = record

            history_list.insert(
                tk.END,
                f"{date} | Weight: {weight} kg | "
                f"Height: {height} m | BMI: {bmi:.2f} | {category}"
            )

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Could not load BMI history.\n{error}"
        )


# ---------------- MAIN WINDOW ----------------

root = tk.Tk()

root.title("BMI Calculator")
root.geometry("750x650")
root.resizable(False, False)


# Title

title_label = tk.Label(
    root,
    text="BMI Calculator",
    font=("Arial", 24, "bold")
)
title_label.pack(pady=20)


# User name

username_frame = tk.Frame(root)
username_frame.pack(pady=8)

tk.Label(
    username_frame,
    text="User Name:",
    font=("Arial", 12)
).pack(side=tk.LEFT, padx=10)

username_entry = tk.Entry(
    username_frame,
    width=30,
    font=("Arial", 12)
)
username_entry.pack(side=tk.LEFT)


# Weight

weight_frame = tk.Frame(root)
weight_frame.pack(pady=8)

tk.Label(
    weight_frame,
    text="Weight (kg):",
    font=("Arial", 12)
).pack(side=tk.LEFT, padx=10)

weight_entry = tk.Entry(
    weight_frame,
    width=30,
    font=("Arial", 12)
)
weight_entry.pack(side=tk.LEFT)


# Height

height_frame = tk.Frame(root)
height_frame.pack(pady=8)

tk.Label(
    height_frame,
    text="Height (m):",
    font=("Arial", 12)
).pack(side=tk.LEFT, padx=10)

height_entry = tk.Entry(
    height_frame,
    width=30,
    font=("Arial", 12)
)
height_entry.pack(side=tk.LEFT)


# Calculate button

calculate_button = tk.Button(
    root,
    text="Calculate BMI",
    command=calculate_bmi,
    font=("Arial", 13, "bold"),
    padx=30,
    pady=10
)
calculate_button.pack(pady=15)


# Results

bmi_result_label = tk.Label(
    root,
    text="BMI: -",
    font=("Arial", 18, "bold")
)
bmi_result_label.pack(pady=5)


category_label = tk.Label(
    root,
    text="Category: -",
    font=("Arial", 16, "bold")
)
category_label.pack(pady=5)


status_label = tk.Label(
    root,
    text="",
    font=("Arial", 10)
)
status_label.pack(pady=5)


# History

history_frame = tk.LabelFrame(
    root,
    text="BMI History",
    padx=10,
    pady=10
)
history_frame.pack(
    pady=15,
    padx=20,
    fill=tk.BOTH,
    expand=True
)


history_list = tk.Listbox(
    history_frame,
    width=90,
    height=8
)
history_list.pack(
    side=tk.LEFT,
    fill=tk.BOTH,
    expand=True
)


history_scrollbar = tk.Scrollbar(
    history_frame,
    orient=tk.VERTICAL,
    command=history_list.yview
)
history_scrollbar.pack(
    side=tk.RIGHT,
    fill=tk.Y
)


history_list.config(
    yscrollcommand=history_scrollbar.set
)


# Create database

create_database()


# Start application

root.mainloop()