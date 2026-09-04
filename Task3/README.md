# Task 3 - Random Password Generator

## Project Overview

This project is a secure Random Password Generator developed using Python and Tkinter. It provides a graphical user interface for generating strong passwords based on user-defined requirements.

## Features

- Generate passwords with a user-defined length.
- Minimum password length of 8 characters.
- Support for uppercase letters.
- Support for lowercase letters.
- Support for numbers.
- Support for symbols.
- Requires at least two character types.
- Uses the Python `secrets` module for secure password generation.
- Guarantees at least one character from each selected character type.
- Password strength indicator: Weak, Medium, or Strong.
- Copy generated password to clipboard.
- Option to exclude ambiguous characters such as `0`, `O`, `I`, `l`, and `1`.
- Displays the last 5 generated passwords during the current session.
- Input validation and error handling.
- Generate multiple passwords without restarting the application.

## Technologies Used

- Python
- Tkinter
- secrets
- string
- pyperclip

## How to Run

### 1. Install Python

Make sure Python is installed on your computer.

### 2. Install pyperclip

Open the terminal in the Task3 folder and run:

```bash
pip install pyperclip

### 3. Run the Application
python password_generator.py

The application will open with a graphical interface where users can select password length and character types.

Security
The application uses Python's secrets module for cryptographically secure password generation.
Generated passwords are not permanently stored in a file or database.
The application keeps only the last 5 generated passwords temporarily during the current session.
Users should not share generated passwords with others.
This project is developed for educational purposes.

## Project Structure

```text
Task3/
├── password_generator.py
└── README.md

## Task Requirements Completed

- [x] Password length selection
- [x] Minimum 8 characters enforced
- [x] Uppercase letters
- [x] Lowercase letters
- [x] Numbers
- [x] Symbols
- [x] At least 2 character types required
- [x] Input validation
- [x] Generate multiple passwords without restarting
- [x] Tkinter GUI
- [x] Secure password generation using `secrets`
- [x] Password strength indicator
- [x] Copy to Clipboard
- [x] Exclude ambiguous characters
- [x] Last 5 generated passwords stored for the current session

## How the Application Works

1. The user selects the required password length.
2. The user selects the character types.
3. The application validates the selected options.
4. A secure password is generated using the `secrets` module.
5. The generated password is displayed in the GUI.
6. The password strength is calculated and displayed.
7. The password is copied to the clipboard.
8. The last 5 generated passwords are displayed in the session history.

## Author

**Prithika**