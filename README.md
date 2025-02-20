# ExpensesTracker

## Overview
ExpensesTracker is a Python application that helps users track their 
income, expenses, savings, and loans. It includes functionalities for 
generating monthly overviews, calculating loan interests, and 
synchronizing data with Google Drive.

## Project Structure
ExpensesTracker/ 
├── app/ 
│ ├── assets/ 
│ │ ├── fonts/ 
│ │ └── images/ 
│ ├── main.kv 
│ ├── main.py 
│ └── __init__.py 
├── client_secrets.json 
├── csv_handler.py 
├── expense.csv 
├── expensemain.py 
├── gdrive.py 
├── loan_calculations.py 
├── Progress.docx 
├── README.md 
└── __init__.py


## Functions

### `csv_handler.py`
- **initialize_csv: Initializes a CSV file with headers.**
- **add_loan: Appends loan details to the CSV file.**
- **generate_monthly_overview: Generates a monthly overview of income, expenses, and savings.**
- **calculate_ratios: Calculates the ratios of expenses, debt, and savings.**
- **append_data_to_csv: Appends data to the CSV file.**
- **read_latest_data: Reads the latest data from the CSV file.**

### `loan_calculations.py`
- **calculate_reducing_balance_interest(principal, annual_rate, term)**: 
    Calculates the total interest for a loan using the reducing balance 
    method.
- **validate_repayment(principal, remaining_balance, annualized_rate, 
    term, repayments_made)**: Validates the repayments made against 
    the expected repayments.
- **infer_annual_rate(principal, term, repayments_made)**: Infers the 
    annualized interest rate based on the repayments made.

### `gdrive.py`
- **authenticate_gdrive()**: Authenticates Google Drive credentials and 
    returns a drive object.
- **upload_file(drive, file_path, file_name)**: Uploads a file to 
    Google Drive and returns the file ID.
- **download_file(drive, file_id, destination_path)**: Downloads a file 
    from Google Drive to the specified destination path.

### `app/main.py`
- **HomeScreen**: A Kivy screen class that updates the monthly overview 
    labels.
  - **update_overview()**: Updates the income, expenses, and savings 
    labels with data from the CSV file.
- **ExpenseTrackerApp**: The main Kivy application class.
  - **build()**: Builds the application UI and loads the KV file.
  - **show_loans()**: Placeholder for showing the loans screen.
  - **show_add_screen()**: Placeholder for showing the add income/expense 
    screen.
  - **sync_data()**: Placeholder for synchronizing data.

### `expensemain.py`
- **main()**: The main function that authenticates Google Drive, 
    initializes the CSV file, adds a loan, and generates a monthly 
    overview.

## Usage
1. Run the main application:
   ```sh
   python app/main.py

2. Run the command-line interface:

python main.py

Dependencies
Kivy
KivyMD
PyDrive2
SciPy
License
This project is licensed under the MIT License.

This `README.md` file provides an overview of the project, its structure, 
and a detailed description of each function in the project.