# ui/screens/budget.py
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from core.budget import Budget

class BudgetScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.budget = Budget()
        self.build_ui()

    def build_ui(self):
        self.layout = MDBoxLayout(orientation="vertical", padding="16dp", spacing="16dp")

        # Salary Input
        self.salary_input = MDTextField(hint_text="Monthly Salary", input_filter="float")
        self.layout.add_widget(self.salary_input)

        # Fixed Savings Input
        self.savings_input = MDTextField(hint_text="Fixed Savings", input_filter="float")
        self.layout.add_widget(self.savings_input)

        # Fixed Expenses Input
        self.expense_input = MDTextField(hint_text="Fixed Expense", input_filter="float")
        self.layout.add_widget(self.expense_input)

        # Add Expense Button
        self.add_expense_button = MDRaisedButton(text="Add Expense", on_release=self.add_expense)
        self.layout.add_widget(self.add_expense_button)

        # Submit Button
        self.submit_button = MDRaisedButton(text="Submit Budget", on_release=self.submit_budget)
        self.layout.add_widget(self.submit_button)

        self.add_widget(self.layout)

    def add_expense(self, instance):
        expense = self.expense_input.text
        if expense:
            self.budget.add_fixed_expense(expense)
            self.expense_input.text = ""  # Clear input field
            print(f"Added Expense: {expense}")

    def submit_budget(self, instance):
        self.budget.salary = float(self.salary_input.text)
        self.budget.fixed_savings = float(self.savings_input.text)
        print("Budget Submitted:", self.budget.__dict__)
        self.manager.get_screen("home").update_budget_bar(self.budget)