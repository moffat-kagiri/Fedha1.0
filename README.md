# ExpensesTracker

## Overview
ExpensesTracker is a Python application that helps users track their income, expenses, savings, and loans. It includes functionalities for generating monthly overviews, calculating loan interests, and synchronizing data with Google Drive.

## Project Structure
ExpensesTracker/ 
├── android/ 
│ ├── permissions.py 
│ └── storage.py 
├── core/ 
│ ├── errors.py 
│ ├── finance.py 
│ ├── services/ 
│ │ └── gdrive_service.py 
│ └── storage/ 
│ ├── CSVManager.py 
│ ├── DataManager.py 
│ └── __init__.py 
├── ui/ 
│ ├── screens/ 
│ │ ├── budget.py 
│ │ ├── home.py 
│ │ ├── inputs.py 
│ │ ├── loans.py 
│ │ ├── summaries.py 
│ │ └── __init__.py 
│ ├── widgets/ 
│ │ ├── cards.kv 
│ │ ├── inputs.kv 
│ │ └── __init__.py 
│ └── __init__.py 
├── assets/ 
│ ├── fonts/ 
│ └── images/ 
├── buildozer.spec 
├── main.py 
├── README.md 
└── __init__.py


## Functions

### `core/storage/CSVManager.py`
- **initialize_csv**: Initializes a CSV file with headers.
- **add_loan**: Appends loan details to the CSV file.
- **generate_monthly_overview**: Generates a monthly overview of income, expenses, and savings.
- **calculate_ratios**: Calculates the ratios of expenses, debt, and savings.
- **append_data_to_csv**: Appends data to the CSV file.
- **read_latest_data**: Reads the latest data from the CSV file.

### `core/finance.py`
- **calculate_reducing_balance_interest(principal, annual_rate, term)**: Calculates the total interest for a loan using the reducing balance method.
- **validate_repayment(principal, remaining_balance, annualized_rate, term, repayments_made)**: Validates the repayments made against the expected repayments.
- **infer_annual_rate(principal, term, repayments_made)**: Infers the annualized interest rate based on the repayments made.

### `core/services/gdrive_service.py`
- **authenticate_gdrive()**: Authenticates Google Drive credentials and returns a drive object.
- **upload_file(drive, file_path, file_name)**: Uploads a file to Google Drive and returns the file ID.
- **download_file(drive, file_id, destination_path)**: Downloads a file from Google Drive to the specified destination path.

### `android/permissions.py`
- **AndroidPermissions**: Handles Android runtime permissions.
  - **check_permissions()**: Checks if all required permissions are granted.
  - **request_permissions(callback=None)**: Requests required permissions.
  - **ensure_permissions(callback=None)**: Ensures all permissions are granted.

### `ui/screens/home.py`
- **HomeScreen**: A Kivy screen class that updates the monthly overview labels.
  - **update_overview()**: Updates the income, expenses, and savings labels with data from the CSV file.

### `ui/screens/budget.py`
- **BudgetScreen**: A Kivy screen class for managing budget.
  - **submit_budget(instance)**: Submits the budget data.
  - **show_error(message)**: Shows an error dialog.

### `main.py`
- **TrackerApp**: The main Kivy application class.
  - **build()**: Builds the application UI and loads the KV files.
  - **initialize_app()**: Initializes the app after permissions are granted.
  - **register_screens()**: Registers the different screens of the app.
  - **save_data(data)**: Saves data to storage.
  - **sync_with_drive()**: Synchronizes data with Google Drive.
  - **show_warning_dialog(title, message)**: Shows a warning dialog.
  - **show_toast(message)**: Shows a toast message.
  - **show_error(message)**: Shows an error dialog.
  - **validate_monetary_input(value)**: Validates monetary input.

## Usage

1. Run the main application:
   ```sh
   python main.py

2. Build the APK for Android:
buildozer -v android debug

3. Install the APK on your Android device:
adb install bin/fedha-0.1-debug.apk

4. Run the app on your Android device:
adb shell monkey -p org.test.fedha -c android.intent.category.LAUNCHER 1

## Dependencies
    - Kivy
    - KivyMD
    - PyDrive2
    - SciPy
    - Buildozer
    - Cython

## License
This project is licensed under the MIT License.

This README.md file provides an overview of the project, its structure, and a detailed description of each function in the project.