import tkinter as tk
from tkinter import messagebox
import secrets
import string
import pyperclip


password_history = []


def generate_password():
    try:
        length = int(length_var.get())

        if length < 8:
            messagebox.showerror(
                "Invalid Length",
                "Password length must be at least 8 characters."
            )
            return

        selected_types = []

        if uppercase_var.get():
            selected_types.append(string.ascii_uppercase)

        if lowercase_var.get():
            selected_types.append(string.ascii_lowercase)

        if numbers_var.get():
            selected_types.append(string.digits)

        if symbols_var.get():
            selected_types.append(string.punctuation)

        if len(selected_types) < 2:
            messagebox.showerror(
                "Invalid Selection",
                "Please select at least 2 character types."
            )
            return

        ambiguous = "0OIl1"
        available_characters = ""

        password_characters = []

        for character_set in selected_types:
            if exclude_var.get():
                character_set = "".join(
                    char for char in character_set
                    if char not in ambiguous
                )

            available_characters += character_set

            password_characters.append(
                secrets.choice(character_set)
            )

        while len(password_characters) < length:
            password_characters.append(
                secrets.choice(available_characters)
            )

        secrets.SystemRandom().shuffle(password_characters)

        password = "".join(password_characters)

        password_var.set(password)

        pyperclip.copy(password)

        password_history.insert(0, password)

        if len(password_history) > 5:
            password_history.pop()

        update_history()
        update_strength(password)

        status_label.config(
            text="Password generated and copied to clipboard."
        )

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter a valid number for password length."
        )


def update_strength(password):
    score = 0

    if len(password) >= 12:
        score += 1

    if any(char.isupper() for char in password):
        score += 1

    if any(char.islower() for char in password):
        score += 1

    if any(char.isdigit() for char in password):
        score += 1

    if any(char in string.punctuation for char in password):
        score += 1

    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Medium"
    else:
        strength = "Strong"

    strength_label.config(text=f"Strength: {strength}")


def copy_password():
    password = password_var.get()

    if not password:
        messagebox.showwarning(
            "No Password",
            "Generate a password first."
        )
        return

    pyperclip.copy(password)

    status_label.config(
        text="Password copied to clipboard."
    )


def update_history():
    history_list.delete(0, tk.END)

    for password in password_history:
        history_list.insert(tk.END, password)


root = tk.Tk()

root.title("Secure Random Password Generator")
root.geometry("600x680")
root.resizable(False, False)


title_label = tk.Label(
    root,
    text="Secure Random Password Generator",
    font=("Arial", 20, "bold")
)
title_label.pack(pady=20)


length_frame = tk.Frame(root)
length_frame.pack(pady=10)


tk.Label(
    length_frame,
    text="Password Length:",
    font=("Arial", 12)
).pack(side=tk.LEFT, padx=5)


length_var = tk.StringVar(value="16")


length_spinbox = tk.Spinbox(
    length_frame,
    from_=8,
    to=100,
    textvariable=length_var,
    width=8
)
length_spinbox.pack(side=tk.LEFT)


options_frame = tk.LabelFrame(
    root,
    text="Character Types",
    padx=15,
    pady=10
)
options_frame.pack(pady=15)


uppercase_var = tk.BooleanVar(value=True)
lowercase_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)


tk.Checkbutton(
    options_frame,
    text="Uppercase Letters",
    variable=uppercase_var
).pack(anchor="w")


tk.Checkbutton(
    options_frame,
    text="Lowercase Letters",
    variable=lowercase_var
).pack(anchor="w")


tk.Checkbutton(
    options_frame,
    text="Numbers",
    variable=numbers_var
).pack(anchor="w")


tk.Checkbutton(
    options_frame,
    text="Symbols",
    variable=symbols_var
).pack(anchor="w")


exclude_var = tk.BooleanVar(value=False)


tk.Checkbutton(
    root,
    text="Exclude ambiguous characters (0, O, I, l, 1)",
    variable=exclude_var
).pack(pady=10)


password_var = tk.StringVar()


password_entry = tk.Entry(
    root,
    textvariable=password_var,
    font=("Consolas", 14),
    width=42,
    justify="center"
)
password_entry.pack(pady=10)


strength_label = tk.Label(
    root,
    text="Strength: -",
    font=("Arial", 12, "bold")
)
strength_label.pack(pady=5)


generate_button = tk.Button(
    root,
    text="Generate Password",
    command=generate_password,
    font=("Arial", 12, "bold"),
    padx=20,
    pady=8
)
generate_button.pack(pady=8)


copy_button = tk.Button(
    root,
    text="Copy to Clipboard",
    command=copy_password,
    font=("Arial", 11),
    padx=20,
    pady=5
)
copy_button.pack(pady=5)


status_label = tk.Label(
    root,
    text="",
    font=("Arial", 10)
)
status_label.pack(pady=5)


history_frame = tk.LabelFrame(
    root,
    text="Last 5 Generated Passwords (Session Only)",
    padx=10,
    pady=10
)
history_frame.pack(pady=15)


history_list = tk.Listbox(
    history_frame,
    width=55,
    height=6
)
history_list.pack()


root.mainloop()