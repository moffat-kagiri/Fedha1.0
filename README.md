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

- __initialize_csv__: Initializes a CSV file with headers.
- __add_loan__: Appends loan details to the CSV file.
- __generate_monthly_overview__: Generates a monthly overview of income, expenses, and savings.
- __calculate_ratios__: Calculates the ratios of expenses, debt, and savings.
- __append_data_to_csv__: Appends data to the CSV file.
- __read_latest_data__: Reads the latest data from the CSV file.

### `core/finance.py`

- __calculate_reducing_balance_interest(principal, annual_rate, term)__: Calculates the total interest for a loan using the reducing balance method.
- __validate_repayment(principal, remaining_balance, annualized_rate, term, repayments_made)__: Validates the repayments made against the expected repayments.
- __infer_annual_rate(principal, term, repayments_made)__: Infers the annualized interest rate based on the repayments made.

### `core/services/gdrive_service.py`

- __authenticate_gdrive()__: Authenticates Google Drive credentials and returns a drive object.
- __upload_file(drive, file_path, file_name)__: Uploads a file to Google Drive and returns the file ID.
- __download_file(drive, file_id, destination_path)__: Downloads a file from Google Drive to the specified destination path.

### `android/permissions.py`

- __AndroidPermissions__: Handles Android runtime permissions.
  - __check_permissions()__: Checks if all required permissions are granted.
  - __request_permissions(callback=None)__: Requests required permissions.
  - __ensure_permissions(callback=None)__: Ensures all permissions are granted.

### `ui/screens/home.py`

- __HomeScreen__: A Kivy screen class that updates the monthly overview labels.
  - __update_overview()__: Updates the income, expenses, and savings labels with data from the CSV file.

### `ui/screens/budget.py`

- __BudgetScreen__: A Kivy screen class for managing budget.
  - __submit_budget(instance)__: Submits the budget data.
  - __show_error(message)__: Shows an error dialog.

### `main.py`

- __TrackerApp__: The main Kivy application class.
  - __build()__: Builds the application UI and loads the KV files.
  - __initialize_app()__: Initializes the app after permissions are granted.
  - __register_screens()__: Registers the different screens of the app.
  - __save_data(data)__: Saves data to storage.
  - __sync_with_drive()__: Synchronizes data with Google Drive.
  - __show_warning_dialog(title, message)__: Shows a warning dialog.
  - __show_toast(message)__: Shows a toast message.
  - __show_error(message)__: Shows an error dialog.
  - __validate_monetary_input(value)__: Validates monetary input.

## Usage

1. Run the main application:

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
