# ui/screens/budget.py
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ObjectProperty
from kivymd.uix.dialog import MDDialog
from core.budget import Budget

class BudgetScreen(MDScreen):
    salary_input = ObjectProperty(None)
    expenses_input = ObjectProperty(None)
    savings_input = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.budget = Budget()
        self.build_ui()

    def build_ui(self):
        self.layout = MDBoxLayout(orientation="vertical", padding="16dp", spacing="16dp")
        
        self.salary_input = MDTextField(hint_text="Enter your salary")
        self.expenses_input = MDTextField(hint_text="Enter your expenses")
        self.savings_input = MDTextField(hint_text="Enter your savings")
        
        submit_button = MDRaisedButton(text="Submit", on_release=self.submit_budget)
        
        self.layout.add_widget(self.salary_input)
        self.layout.add_widget(self.expenses_input)
        self.layout.add_widget(self.savings_input)
        self.layout.add_widget(submit_button)
        
        self.add_widget(self.layout)

    def submit_budget(self, instance):
        try:
            salary = float(self.salary_input.text) if self.salary_input.text else 0.0
            expenses = float(self.expenses_input.text) if self.expenses_input.text else 0.0
            savings = float(self.savings_input.text) if self.savings_input.text else 0.0
            
            self.budget.salary = salary
            self.budget.expenses = expenses
            self.budget.savings = savings
            
            # Perform further actions with the budget data
        except ValueError as e:
            self.show_error(f"Invalid input: {str(e)}")

    def show_error(self, message):
        dialog = MDDialog(
            title="Error",
            text=message,
            buttons=[MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()