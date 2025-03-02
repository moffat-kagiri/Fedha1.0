# ui/widgets/inputs.py
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivy.properties import BooleanProperty, StringProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout

class CurrencyInput(MDTextField):
    """Currency input field with validation"""
    currency_symbol = StringProperty("KES")
    min_value = NumericProperty(0)
    
    def insert_text(self, substring, from_undo=False):
        # Allow only numbers and decimal point
        if not substring.isdigit() and substring not in (".", ","):
            return
        return super().insert_text(substring, from_undo)

class DateInput(MDBoxLayout):
    """Date picker input with calendar integration"""
    selected_date = StringProperty("")
    
    def show_date_picker(self):
        from kivymd.uix.pickers import MDDatePicker
        MDDatePicker(callback=self.on_date_selected).open()
    
    def on_date_selected(self, instance, value, date_range):
        self.selected_date = value.strftime("%Y-%m-%d")

class LoanInputGroup(MDBoxLayout):
    """Loan-specific input fields with APR calculation"""
    show_apr = BooleanProperty(False)
    
    def calculate_apr(self, principal, instalment, term):
        from core.finance import LoanCalculator
        try:
            return LoanCalculator.appraise_loan(
                float(principal),
                float(instalment),
                int(term)
            )
        except:
            return 0, 0

class CategorySelect(MDBoxLayout):
    """Visual category selector with icons"""
    selected_category = StringProperty("income")
    categories = ["income", "expense", "loan"]
    
    def select_category(self, category):
        self.selected_category = category

class InputContent(BoxLayout):
    hint_text = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(MDTextField(hint_text="Enter some text"))
        # Additional initialization code