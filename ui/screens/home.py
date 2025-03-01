# ui/screens/home.py
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRoundFlatButton
from kivy.properties import NumericProperty, StringProperty
from core.storage.storage import DataManager
from ui.widgets.cards import RatioCard, TransactionCard
from ui.widgets.inputs import CurrencyInput, DateInput
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from android.storage import get_app_path

class RatioCard(MDCard):
    """Custom card component for financial ratios"""
    title = StringProperty("Ratio")
    value = NumericProperty(0)
    icon = StringProperty("cash")
    theme_color = StringProperty("Primary")

class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_manager = DataManager(get_storage_path=get_app_path)
        self.budget_bar = MDProgressBar()
        self.budget_labels = MDLabel()
        self.build_ui()

    def on_enter(self):
        """Update data when screen becomes visible"""
        self.update_overview()

    def update_overview(self):
        """Refresh all financial data"""
        ratios = self.data_manager.calculate_ratios()
        
        # Update ratio cards
        self.ids.expenses_card.value = ratios['expenses_ratio']
        self.ids.debt_card.value = ratios['debt_ratio']
        self.ids.savings_card.value = ratios['savings_ratio']
        
        # Update quick stats
        overview = self.data_manager.transactions.generate_monthly_overview()
        self.ids.income_label.text = f"KES {overview['income']:,.2f}"
        self.ids.expenses_label.text = f"KES {overview['expenses']:,.2f}"

    def show_detailed_report(self):
        """Navigate to detailed reports screen"""
        self.manager.current = 'summaries'

    def build_ui(self):
        self.layout = MDBoxLayout(orientation="vertical", padding="16dp", spacing="16dp")
        
        # Budget Bar
        self.layout.add_widget(self.budget_bar)
        self.layout.add_widget(self.budget_labels)
        
        self.add_widget(self.layout)
        self.budget_button = MDRaisedButton(
            text="Set Budget",
            on_release=self.go_to_budget
        )
        self.layout.add_widget(self.budget_button)
    
    def go_to_budget(self, instance):
        self.manager.current = "budget"

    def update_budget_bar(self, budget):
        savings_percent = budget.savings_percentage()
        expenses_percent = budget.expenses_percentage()
        surplus_percent = budget.surplus_percentage()

        # Update Progress Bar
        self.budget_bar.value = savings_percent + expenses_percent

        # Update Labels
        self.budget_labels.text = (
            f"Savings: {savings_percent:.1f}% | "
            f"Expenses: {expenses_percent:.1f}% | "
            f"Surplus: {surplus_percent:.1f}%"
        )

        # Change Bar Color Based on Surplus
        if surplus_percent >= 20:
            self.budget_bar.color = (0, 1, 0, 1)  # Green
        else:
            self.budget_bar.color = (1, 0, 0, 1)  # Red

    def update_progress_bar(self):
        # Get the updated data from DataManager
        surplus = self.app.data_manager.get_surplus()
        expenses = self.app.data_manager.get_expenses()
        
        # Calculate the remaining surplus
        remaining_surplus = surplus - expenses
        
        # Update the progress bar
        self.ids.progress_bar.value = remaining_surplus
        
        # Optionally, show a warning if the user is dipping into debt
        if remaining_surplus < 0:
            self.show_warning_dialog("Warning", "You are dipping into debt!")