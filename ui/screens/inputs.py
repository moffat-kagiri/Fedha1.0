# ui/screens/input.py
from datetime import datetime
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from core.storage.storage import DataManager
from android.storage import get_app_path

from kivymd.uix.dialog import MDDialog
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty

# App imports using absolute paths
from core.finance import LoanCalculator
from core.errors import ValidationError
from ui.widgets.inputs import InputContent, CurrencyInput, DateInput
from ui.widgets.cards import RatioCard, TransactionCard

class CurrencyInput:
    def validate(self):
        if self.text < self.min_value:
            raise ValidationError(
                "amount", 
                f"Minimum {self.currency_symbol} {self.min_value}"
            )

class InputScreen(MDScreen):
    current_input_type = StringProperty("income")
    show_loan_fields = BooleanProperty(False)
    input_content = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "New Entry"
        self.data_manager = DataManager(get_storage_path=get_app_path)
        self.dialog = None
        self.build_ui()

    def build_ui(self):
        """Initialize and arrange UI components"""
        # Main layout with padding and spacing
        self.main_layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(16),
            spacing=dp(16),
            md_bg_color=[0.9, 0.9, 0.9, 1]  # Light background
        )

        # Title
        title = MDLabel(
            text="New Transaction",
            halign="center",
            font_style="H5",
            size_hint_y=None,
            height=dp(48)
        )
        self.main_layout.add_widget(title)

        # Create input container
        self.input_container = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16),
            size_hint_y=None,
            height=dp(400)
        )
        self.main_layout.add_widget(self.input_container)

        # Initialize default input content
        self.input_content = None
        
        # Initialize the inputs
        self.create_input_fields()
        
        # Add main layout to screen
        self.add_widget(self.main_layout)

    def create_input_fields(self):
        """Create and initialize input fields"""
        # Amount input with currency
        self.amount_input = MDTextField(
            hint_text="Amount (KES)",
            helper_text="Enter amount in Kenyan Shillings",
            helper_text_mode="on_error",
            input_filter="float",
            size_hint_y=None,
            height=dp(48)
        )
        self.input_container.add_widget(self.amount_input)

        # Description input
        self.desc_input = MDTextField(
            hint_text="Description",
            helper_text="Enter transaction description",
            multiline=False,
            size_hint_y=None,
            height=dp(48)
        )
        self.input_container.add_widget(self.desc_input)

        # Category input
        self.category_input = MDTextField(
            hint_text="Category",
            helper_text="E.g., Food, Transport, Utilities",
            multiline=False,
            size_hint_y=None,
            height=dp(48)
        )
        self.input_container.add_widget(self.category_input)

        # Buttons container
        buttons_container = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(8),
            size_hint_y=None,
            height=dp(56),
            padding=[dp(8), 0]
        )

        # Clear button
        clear_button = MDRaisedButton(
            text="Clear",
            on_release=self.clear_inputs,
            md_bg_color=[0.8, 0.2, 0.2, 1]
        )
        buttons_container.add_widget(clear_button)

        # Save button
        save_button = MDRaisedButton(
            text="Save",
            on_release=self.save_transaction,
            md_bg_color=[0.2, 0.8, 0.2, 1]
        )
        buttons_container.add_widget(save_button)

        self.input_container.add_widget(buttons_container)

    def on_enter(self):
        """Called when screen is entered"""
        # Reset input fields
        self.clear_inputs()
        
    def show_input_dialog(self, input_type):
        """Show appropriate input form based on transaction type"""
        self.current_input_type = input_type
        self.show_loan_fields = (input_type == "loan")
        
        if not self.dialog:
            self.create_input_dialog()
            
        self.update_dialog_fields()
        self.dialog.open()

    def create_input_dialog(self):
        """Create reusable input dialog"""
        self.dialog = MDDialog(
            title=self.get_dialog_title(),
            type="custom",
            content_cls=InputContent(),
            buttons=[
                MDFlatButton(text="CANCEL", on_release=self.close_dialog),
                MDRaisedButton(text="SAVE", on_release=self.save_transaction)
            ]
        )

    def update_dialog_fields(self):
        """Update dialog based on input type"""
        self.dialog.title = self.get_dialog_title()
        self.dialog.content_cls.ids.term_input.disabled = not self.show_loan_fields
        self.dialog.content_cls.ids.instalment_input.disabled = not self.show_loan_fields
        self.dialog.content_cls.ids.apr_label.opacity = 1 if self.show_loan_fields else 0

    def get_dialog_title(self):
        """Get localized dialog title"""
        titles = {
            "income": "New Income",
            "expense": "New Expense",
            "loan": "New Loan"
        }
        return titles.get(self.current_input_type, "New Transaction")

    def close_dialog(self, *args):
        """Close input dialog"""
        self.dialog.dismiss()
        self.clear_inputs()

    def validate_monetary_input(value):
        try:
            # Convert the input to a float
            value = float(value)
            # Round to 2 decimal places
            value = round(value, 2)
            return value
        except ValueError:
            # Handle the case where the input is not a valid number
            return None

    def save_transaction(self, *args):
        """Save transaction to appropriate storage"""
        try:
            content = self.dialog.content_cls
            amount = self.validate_monetary_input(content.ids.amount_input.text)
            description = content.ids.description_input.text
            
            if self.current_input_type == "loan":
                self.save_loan(content, amount, description)
            else:
                self.save_regular_transaction(amount, description)
                
            self.update_parent_screens()
            self.close_dialog()
            
        except ValueError as e:
            self.show_error(f"Invalid input: {str(e)}")
        except Exception as e:
            self.show_error(f"Save failed: {str(e)}")

    def save_regular_transaction(self, amount, description):
        """Save income/expense transaction"""
        self.data_manager.transactions.save_transaction(
            transaction_type=self.current_input_type,
            amount=amount,
            description=description
        )

    def save_loan(self, content, amount, description):
        """Save loan with calculated APR"""
        term = int(content.ids.term_input.text)
        instalment = self.validate_monetary_input(content.ids.instalment_input.text)
        
        # Validate loan terms
        if instalment < (amount / term):
            raise ValueError("Instalment too low to repay principal")
            
        # Calculate APR and total interest
        apr, total_interest = LoanCalculator.appraise_loan(
            principal=amount,
            monthly_instalment=instalment,
            term_months=term
        )
        
        # Save loan data
        self.data_manager.loans.save_loan({
            'amount': amount,
            'term': term,
            'instalment': instalment,
            'apr': apr,
            'total_interest': total_interest,
            'description': description
        })
    def on_text_change(self, instance, value):
        """Update APR calculation when loan fields change"""
        if self.current_input_type == "loan":
            try:
                content = self.dialog.content_cls
                amount = float(content.ids.amount_input.text)
                term = int(content.ids.term_input.text)
                instalment = float(content.ids.instalment_input.text)
                
                apr, total_interest = LoanCalculator.appraise_loan(amount, instalment, term)
                content.ids.apr_label.text = f"APR: {apr:.2f}% | Total Interest: KES {total_interest:.2f}"
                content.ids.apr_label.opacity = 1
            except:
                content.ids.apr_label.opacity = 0

    def update_parent_screens(self):
        """Refresh data on related screens"""
        self.manager.get_screen('home').update_overview()
        self.manager.get_screen('loans').update_loans()

    def clear_inputs(self, *args):
        """Reset all input fields"""
        if hasattr(self, 'amount_input'):
            self.amount_input.text = ""
        if hasattr(self, 'desc_input'):
            self.desc_input.text = ""
        if hasattr(self, 'category_input'):
            self.category_input.text = ""

    def show_error(self, message):
        """Display error message"""
        error_dialog = MDDialog(
            title="Input Error",
            text=message,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: error_dialog.dismiss()
                )
            ]
        )
        error_dialog.open()

    def add_expense(self, expense_amount):
        # Validate the expense amount
        expense_amount = self.validate_monetary_input(expense_amount)
        if expense_amount is None:
            self.show_error("Invalid expense amount")
            return
        
        # Update the data in DataManager
        self.app.data_manager.add_expense(expense_amount)
        
        # Refresh the home screen
        home_screen = self.app.root.get_screen('home')
        home_screen.update_progress_bar()

    def on_save(self, *args):
        # Save data logic here
        self.parent.parent.parent.switch_tab('home')  # Return to home screen