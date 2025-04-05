# ui/screens/loans.py
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDRoundFlatButton, MDFloatingActionButton
from kivymd.uix.label import MDLabel
from kivy.properties import DictProperty, NumericProperty, StringProperty
from kivy.metrics import dp
from core.storage.storage import DataManager
from core.finance import LoanCalculator
from ui.widgets.cards import RatioCard, TransactionCard
from ui.widgets.inputs import CurrencyInput, DateInput
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.boxlayout import MDBoxLayout
from android.storage import get_app_path
from kivymd.uix.list import MDList, TwoLineIconListItem, IconLeftWidget
from kivymd.uix.textfield import MDTextField
from datetime import datetime
from kivy.logger import Logger

class LoanItem(MDCard):
    loan_data = DictProperty()
    loan_index = NumericProperty()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_manager = DataManager()
        
    def update_balance(self):
        """Update displayed balance using current payment data"""
        principal = self.loan_data['Loan Amount']
        apr = self.loan_data['APR']
        term = self.loan_data['Term']
        payments_made = self.loan_data.get('Payments Made', 0)
        
        balance = LoanCalculator.calculate_remaining_balance(
            principal, apr, payments_made, term
        )
        self.ids.balance_label.text = f"Balance: KES {balance:,.2f}"
        
    def record_payment(self):
        """Record a payment for this loan"""
        try:
            payment = float(self.ids.payment_input.text)
            if payment <= 0:
                raise ValueError("Payment must be positive")
                
            self.data_manager.record_loan_payment(
                loan_index=self.loan_index,
                payment_amount=payment
            )
            self.update_balance()
            self.ids.payment_input.text = ""
            
        except ValueError as e:
            self.show_error(str(e))
            
    def show_payment_history(self):
        """Show payment history dialog"""
        # Implement payment history tracking
        pass
        
    def show_error(self, message):
        """Display error message"""
        MDDialog(
            title="Payment Error",
            text=message,
            buttons=[MDFlatButton(text="OK", on_release=lambda x: x.parent.parent.dismiss())]
        ).open()

class LoansScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Loans"
        self.data_manager = DataManager(get_storage_path=get_app_path)
        self.build_ui()
        
    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical', padding=dp(16))
        
        # Add loans list
        self.loans_list = MDList()
        layout.add_widget(self.loans_list)
        
        # Add floating action button for new loan
        fab = MDFloatingActionButton(
            icon="plus",
            pos_hint={"center_x": .85, "center_y": .1},
            on_release=self.show_new_loan_dialog
        )
        layout.add_widget(fab)
        
        self.add_widget(layout)
        self.refresh_loans()
    
    def refresh_loans(self):
        self.loans_list.clear_widgets()
        # Add sample loans (replace with actual data)
        loans = [
            {"name": "Car Loan", "amount": "500,000", "icon": "car"},
            {"name": "Home Loan", "amount": "2,500,000", "icon": "home"},
        ]
        for loan in loans:
            item = TwoLineIconListItem(
                text=loan["name"],
                secondary_text=f"KES {loan['amount']}",
                on_release=lambda x: self.show_loan_details(loan)
            )
            item.add_widget(IconLeftWidget(icon=loan["icon"]))
            self.loans_list.add_widget(item)
        
    def on_enter(self):
        """Load loans when screen becomes visible"""
        self.refresh_loans()
        
    def update_loans(self, sort_key='Date', ascending=False):
        """Refresh loan list with sorting options"""
        self.ids.loan_container.clear_widgets()
        
        try:
            loans = self.data_manager.loans.load_loans(sort_by=sort_key, ascending=ascending)
            
            if not loans:
                self.ids.loan_container.add_widget(MDLabel(
                    text="No Active Loans",
                    halign="center",
                    theme_text_color="Secondary"
                ))
                return
                
            for idx, loan in enumerate(loans):
                loan_item = LoanItem(
                    size_hint=(1, None),
                    height=dp(160),
                    loan_data=loan,
                    loan_index=idx
                )
                loan_item.update_balance()
                self.ids.loan_container.add_widget(loan_item)
                
        except Exception as e:
            self.show_error(f"Error loading loans: {str(e)}")
            
    def show_sort_menu(self):
        """Show sorting options menu"""
        menu_items = [
            {
                "text": "Newest First",
                "viewclass": "OneLineListItem",
                "on_release": lambda: self.update_loans(sort_key='Date', ascending=False)
            },
            {
                "text": "Oldest First",
                "viewclass": "OneLineListItem",
                "on_release": lambda: self.update_loans(sort_key='Date', ascending=True)
            },
            {
                "text": "Highest Balance",
                "viewclass": "OneLineListItem",
                "on_release": lambda: self.update_loans(sort_key='Loan Amount', ascending=False)
            },
            {
                "text": "Lowest Balance",
                "viewclass": "OneLineListItem",
                "on_release": lambda: self.update_loans(sort_key='Loan Amount', ascending=True)
            }
        ]
        
        self.sort_menu = MDDropdownMenu(
            caller=self.ids.sort_button,
            items=menu_items,
            width_mult=4
        )
        self.sort_menu.open()
        
    def add_new_loan(self, *args):
        # Add loan logic here
        self.parent.parent.parent.switch_tab('input')  # Go to input screen
        
    def show_error(self, message):
        """Display error dialog"""
        MDDialog(
            title="Loan Error",
            text=message,
            buttons=[MDFlatButton(text="OK", on_release=lambda x: x.parent.parent.dismiss())]
        ).open()
    
    def show_new_loan_dialog(self, *args):
        """Show dialog to add a new loan"""
        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=dp(20),
            size_hint_y=None,
            height=dp(300)
        )
        
        # Add input fields
        self.loan_name = MDTextField(
            hint_text="Loan Name",
            helper_text="Enter loan name",
            helper_text_mode="on_error"
        )
        self.loan_amount = MDTextField(
            hint_text="Amount",
            helper_text="Enter loan amount",
            helper_text_mode="on_error",
            input_filter="float"
        )
        self.interest_rate = MDTextField(
            hint_text="Interest Rate (%)",
            helper_text="Enter annual interest rate",
            helper_text_mode="on_error",
            input_filter="float"
        )
        self.loan_term = MDTextField(
            hint_text="Term (months)",
            helper_text="Enter loan term in months",
            helper_text_mode="on_error",
            input_filter="int"
        )
        
        content.add_widget(self.loan_name)
        content.add_widget(self.loan_amount)
        content.add_widget(self.interest_rate)
        content.add_widget(self.loan_term)
        
        self.dialog = MDDialog(
            title="Add New Loan",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=lambda x: self.dialog.dismiss()
                ),
                MDRaisedButton(
                    text="SAVE",
                    on_release=self.save_loan
                )
            ]
        )
        self.dialog.open()
    
    def save_loan(self, *args):
        """Save the new loan details"""
        try:
            # Validate inputs
            name = self.loan_name.text.strip()
            amount = float(self.loan_amount.text)
            rate = float(self.interest_rate.text)
            term = int(self.loan_term.text)
            
            if not name:
                raise ValueError("Loan name is required")
            if amount <= 0:
                raise ValueError("Amount must be greater than 0")
            if rate <= 0:
                raise ValueError("Interest rate must be greater than 0")
            if term <= 0:
                raise ValueError("Term must be greater than 0")
            
            # Create loan object
            loan_data = {
                "name": name,
                "amount": amount,
                "interest_rate": rate,
                "term": term,
                "date": datetime.now().strftime("%Y-%m-%d")
            }
            
            # Save loan data
            self.data_manager.loans.write_csv([loan_data])
            
            # Refresh loans list
            self.refresh_loans()
            
            # Close dialog
            self.dialog.dismiss()
            
        except ValueError as e:
            self.show_error(str(e))
        except Exception as e:
            self.show_error(f"Error saving loan: {str(e)}")
    def show_loan_details(self, loan):
        """Show detailed information about the selected loan"""
        # Create a layout for the popup content
        content = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(20),
            size_hint_y=None,
            height=dp(200)
        )

        # Add loan details to the popup content
        content.add_widget(MDLabel(text=f"Loan Name: {loan['name']}", theme_text_color="Primary"))
        content.add_widget(MDLabel(text=f"Amount: KES {loan['amount']}", theme_text_color="Secondary"))
        content.add_widget(MDLabel(text=f"Icon: {loan['icon']}", theme_text_color="Secondary"))

        # Create and open the popup dialog
        self.dialog = MDDialog(
            title="Loan Details",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="CLOSE",
                    on_release=lambda x: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()