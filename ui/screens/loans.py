# ui/screens/loans.py
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivy.properties import DictProperty, NumericProperty
from kivy.metrics import dp
from core.storage.storage import DataManager
from core.finance import LoanCalculator
from ui.widgets.cards import RatioCard, TransactionCard
from ui.widgets.inputs import CurrencyInput, DateInput

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
        self.data_manager = DataManager()
        self.sort_menu = None
        
    def on_enter(self):
        """Load loans when screen becomes visible"""
        self.update_loans()
        
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
        
    def show_error(self, message):
        """Display error dialog"""
        MDDialog(
            title="Loan Error",
            text=message,
            buttons=[MDFlatButton(text="OK", on_release=lambda x: x.parent.parent.dismiss())]
        ).open()
