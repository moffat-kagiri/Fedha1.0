import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class CSVManager:
    """Platform-agnostic CSV operations"""
    def __init__(self, filename, get_storage_path):
        self.filepath = Path(get_storage_path(filename))
        self.headers = {
            'loans': ["Date", "Loan Amount", "Term", "Monthly Instalment", 
                     "APR", "Total Interest", "Description", "Payments Made"],
            'transactions': ["Date", "Income", "Expenses", "Debt", "Description"]
        }

    # Keep all existing CSVManager methods unchanged
    # (remove any Android-specific imports/references)

class DataManager:
    def __init__(self, get_storage_path):
        self.get_storage_path = get_storage_path
        self.loans = CSVManager("loans.csv", get_storage_path)
        self.transactions = CSVManager("expenses.csv", get_storage_path)