# Task 2 - BMI Calculator

## Project Overview

This project is a BMI Calculator developed using Python and Tkinter. It allows users to calculate their Body Mass Index (BMI), view their BMI category, and store BMI records in a local SQLite database.

## Features

- User-friendly graphical interface using Tkinter.
- Accepts user name, weight, and height.
- Calculates BMI using the formula:
  BMI = Weight (kg) / Height (m)²
- Displays the calculated BMI.
- Displays BMI category.
- Stores BMI records in a SQLite database.
- Displays BMI history with date and time.
- Validates numeric input.
- Prevents zero and negative weight or height values.
- Provides error messages for invalid input.

## Technologies Used

- Python
- Tkinter
- SQLite
- datetime

## How to Run

### 1. Install Python

Make sure Python is installed on your computer.

### 2. Open the Task2 folder

Open the terminal in the Task2 folder.

### 3. Run the application

```bash
python bmi_calculator.py


| BMI Range    | Category    |
| ------------ | ----------- |
| Below 18.5   | Underweight |
| 18.5 - 24.9  | Normal      |
| 25 - 29.9    | Overweight  |
| 30 and above | Obese       |

### Validation

The application validates user input.

Weight and height must be numeric values.
Weight and height must be greater than zero.
Invalid inputs display an error message.
Zero and negative values are rejected.
### Data Storage

BMI records are stored locally using SQLite.
Records include user information, weight, height, BMI, category, and timestamp.
BMI history can be viewed inside the application.
The database is stored locally on the user's computer.
### Security
The application does not require passwords or login credentials.
BMI data is stored locally in a SQLite database.
No data is sent to an external server.
This project is developed for educational purposes.

### How the Application Works


The user enters their name.
The user enters weight in kilograms.
The user enters height in meters.
The application validates the input.
BMI is calculated.
The BMI category is determined.
The result is displayed.
The BMI record is saved to the SQLite database.
Previous BMI records are displayed in the BMI History section.
Author

Prithika
