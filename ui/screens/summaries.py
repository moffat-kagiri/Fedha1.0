# ui/screens/summaries.py
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDLineChart, MDBarChart
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDButton
from kivymd.uix.button import MDButtonText
from kivy.properties import StringProperty, NumericProperty
from kivy.properties import DictProperty
from core.storage import DataManager
from datetime import datetime
from ui.widgets.cards import RatioCard, TransactionCard
from ui.widgets.inputs import CurrencyInput, DateInput

class SummaryCard(MDCard):
    """Reusable card component for summary items"""
    category = StringProperty("Category")
    amount = StringProperty("KES 0.00")
    percentage = NumericProperty(0)
    icon = StringProperty("cash")

class SummariesScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_manager = DataManager()
        self.chart = None
        
    def on_enter(self):
        """Refresh data when screen becomes visible"""
        self.update_overview()
        
    def update_overview(self):
        """Load and display financial data"""
        overview = self.data_manager.transactions.generate_monthly_overview()
        ratios = self.data_manager.calculate_ratios()
        
        # Update summary cards
        self.ids.income_card.amount = f"KES {overview['income']:,.2f}"
        self.ids.income_card.percentage = ratios['income_percentage']
        
        self.ids.expenses_card.amount = f"KES {overview['expenses']:,.2f}"
        self.ids.expenses_card.percentage = ratios['expenses_ratio']
        
        self.ids.savings_card.amount = f"KES {overview['savings']:,.2f}"
        self.ids.savings_card.percentage = ratios['savings_ratio']
        
        # Update charts
        self.update_chart()

    def update_chart(self, chart_type="bar"):
        """Create or update financial chart"""
        if self.chart:
            self.ids.chart_container.remove_widget(self.chart)
            
        if chart_type == "bar":
            self.chart = MDBarChart(
                labels=True,
                legend=True,
                anim=True,
                y_grid=True,
                x_grid=True,
                padding="24dp"
            )
        else:
            self.chart = MDLineChart(
                labels=True,
                legend=True,
                anim=True,
                y_grid=True,
                x_grid=True,
                padding="24dp"
            )
            
        # Add chart data (example with 6 months history)
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        income_data = [15000, 18000, 16500, 21000, 19500, 23000]
        expenses_data = [12000, 14000, 13000, 16000, 15000, 17000]
        
        self.chart.add_data_collection("Income", income_data, [0.2, 0.5, 0.8, 1])
        self.chart.add_data_collection("Expenses", expenses_data, [0.8, 0.2, 0.2, 1])
        self.chart.x_labels = months
        
        self.ids.chart_container.add_widget(self.chart)

    def show_detailed_statement(self, category):
        """Show transaction list for specific category"""
        overview = self.data_manager.transactions.generate_monthly_overview()
        transactions = overview['transactions'][category]
        
        # Implement transaction list dialog
        self.show_transaction_dialog(category, transactions)

    def show_transaction_dialog(self, title, transactions):
        """Display detailed transaction list"""
        from kivymd.uix.list import OneLineListItem
        
        dialog = MDDialog(
            title=f"{title.capitalize()} Transactions",
            type="confirmation",
            items=[OneLineListItem(text=f"{t['Date']} - {t['Description']}: KES {t['Amount']}") 
                  for t in transactions],
            buttons=[
                MDButtonText(text="CLOSE", on_release=lambda x: dialog.dismiss())
            ]
        )
        dialog.open()