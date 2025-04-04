import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from kivy.logger import Logger

def get_storage_path(filename):
    """Get the platform-specific storage path for a file."""
    # Implement the logic to get the storage path
    pass

class CSVManager:
    """Platform-agnostic CSV operations"""
    def __init__(self, filename, get_storage_path):
        self.filepath = Path(get_storage_path(filename))
        self.headers = {
            'loans': ["Date", "Loan Amount", "Term", "Monthly Instalment", 
                     "APR", "Total Interest", "Description", "Payments Made"],
            'transactions': ["Date", "Income", "Expenses", "Debt", "Description"]
        }

    def read_csv(self):
        """Read data from a CSV file."""
        if not self.filepath.exists():
            return []
        
        with open(self.filepath, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return list(reader)

    def write_csv(self, data):
        """Write data to a CSV file."""
        with open(self.filepath, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.headers.get(self.filepath.stem, []))
            writer.writeheader()
            writer.writerows(data)

    def generate_monthly_overview(self):
        """Generate monthly overview of transactions"""
        try:
            data = self.read_csv()
            if not data:
                return {"income": 0, "expenses": 0, "savings": 0}

            current_month = datetime.now().strftime("%Y-%m")
            
            # Filter transactions for current month
            monthly_data = [
                row for row in data 
                if row.get("date", "").startswith(current_month)
            ]
            
            # Calculate totals
            income = sum(float(row.get("income", 0)) for row in monthly_data)
            expenses = sum(float(row.get("expenses", 0)) for row in monthly_data)
            savings = income - expenses
            
            return {
                "income": income,
                "expenses": expenses,
                "savings": savings
            }
        except Exception as e:
            Logger.error(f"Error generating monthly overview: {str(e)}")
            return {"income": 0, "expenses": 0, "savings": 0}

class DataManager:
    """Manages all data operations (local and remote)."""
    def __init__(self, get_storage_path):
        self.get_storage_path = get_storage_path
        self.loans = CSVManager("loans.csv", get_storage_path)
        self.transactions = CSVManager("expenses.csv", get_storage_path)

    def calculate_ratios(self):
        """Calculate financial ratios based on transaction data."""
        try:
            transactions = self.transactions.read_csv()
            if not transactions:
                return {"expenses": 0, "savings": 0, "surplus": 0}

            # Get the most recent transaction
            latest = transactions[-1]
            
            # Convert string values to float
            income = float(latest.get("Income", 0))
            expenses = float(latest.get("Expenses", 0))
            debt = float(latest.get("Debt", 0))
            
            # Avoid division by zero
            if income == 0:
                return {"expenses": 0, "savings": 0, "surplus": 0}
            
            # Calculate ratios as percentages
            expenses_ratio = (expenses / income) * 100
            debt_ratio = (debt / income) * 100
            savings_ratio = 100 - expenses_ratio - debt_ratio
            
            return {
                "expenses": round(expenses_ratio, 2),
                "savings": round(savings_ratio, 2),
                "surplus": round(100 - expenses_ratio, 2)
            }
            
        except Exception as e:
            Logger.error(f"Error calculating ratios: {str(e)}")
            return {"expenses": 0, "savings": 0, "surplus": 0}