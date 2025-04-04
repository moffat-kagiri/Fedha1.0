# ui/screens/home.py
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.progressbar import MDProgressBar
from kivy.properties import NumericProperty, StringProperty, ListProperty
from kivy.logger import Logger
from core.storage.storage import DataManager
from android.storage import get_app_path

class RatioCard(MDCard):
    """Custom card component for financial ratios"""
    title = StringProperty("Ratio")
    value = NumericProperty(0)
    icon = StringProperty("cash")
    theme_color = StringProperty("Primary")
    bg_color = ListProperty([1, 1, 1, 1])  # Add this line

    def on_theme_color(self, instance, value):
        """Update background color when theme color changes"""
        colors = {
            "Red": [0.8, 0.2, 0.2, 1],
            "Green": [0.2, 0.8, 0.2, 1],
            "Blue": [0.2, 0.2, 0.8, 1],
            "Primary": [0.12, 0.58, 0.95, 1]
        }
        self.bg_color = colors.get(value, [1, 1, 1, 1])

class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Home"
        self.data_manager = DataManager(get_storage_path=get_app_path)
        self.budget_bar = MDProgressBar()
        self.budget_labels = MDLabel()
        self.build_ui()

    def on_enter(self):
        """Update data when screen becomes visible"""
        self.update_overview()

    def update_overview(self):
        """Refresh all financial data"""
        try:
            ratios = self.data_manager.calculate_ratios()
            
            # Update ratio cards with direct references
            self.expenses_card.value = ratios['expenses']
            self.debt_card.value = ratios['savings']
            self.savings_card.value = ratios['surplus']
            
            # Update quick stats if they exist
            overview = self.data_manager.transactions.generate_monthly_overview()
            if hasattr(self.ids, 'income_label'):
                self.ids.income_label.text = f"KES {overview['income']:,.2f}"
            if hasattr(self.ids, 'expenses_label'):
                self.ids.expenses_label.text = f"KES {overview['expenses']:,.2f}"
        except Exception as e:
            Logger.error(f"Error updating overview: {str(e)}")
    
    def show_detailed_report(self):
        """Navigate to detailed reports screen."""
        self.manager.current = 'summaries'

    def build_ui(self):
        """Initialize and arrange UI components"""
        self.layout = MDBoxLayout(orientation="vertical", padding="16dp", spacing="16dp")
        
        # Create ratio cards row
        cards_layout = MDBoxLayout(
            orientation="horizontal",
            spacing="8dp",
            size_hint_y=None,
            height="120dp"
        )
        
        # Expenses card
        self.expenses_card = RatioCard(
            title="Expenses",
            icon="cash-minus",
            theme_color="Red"
        )
        self.expenses_card.id = 'expenses_card'
        
        # Savings card
        self.savings_card = RatioCard(
            title="Savings",
            icon="piggy-bank",
            theme_color="Green"
        )
        self.savings_card.id = 'savings_card'
        
        # Debt card
        self.debt_card = RatioCard(
            title="Debt",
            icon="credit-card",
            theme_color="Blue"
        )
        self.debt_card.id = 'debt_card'
        
        # Add cards to layout
        cards_layout.add_widget(self.expenses_card)
        cards_layout.add_widget(self.savings_card)
        cards_layout.add_widget(self.debt_card)
        
        # Add cards layout to main layout
        self.layout.add_widget(cards_layout)
        
        # Budget Bar
        self.layout.add_widget(self.budget_bar)
        self.layout.add_widget(self.budget_labels)
        
        # Budget Button
        self.budget_button = MDRaisedButton(
            text="Set Budget",
            on_release=self.go_to_budget
        )
        self.layout.add_widget(self.budget_button)
        
        self.add_widget(self.layout)
    
    def go_to_budget(self, *args):
        """Navigate to input screen"""
        self.manager.current = 'input'  # Use screen manager's current property

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