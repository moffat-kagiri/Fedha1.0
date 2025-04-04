# ui/screens/summaries.py
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.graph import Graph, LinePlot, BarPlot
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDRoundFlatButton
from kivy.properties import StringProperty, NumericProperty, DictProperty
from core.storage.storage import DataManager
from datetime import datetime
from ui.widgets.cards import RatioCard, TransactionCard
from ui.widgets.inputs import CurrencyInput, DateInput
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.boxlayout import MDBoxLayout
from android.storage import get_app_path
from kivymd.uix.label import MDLabel
from kivy.metrics import dp

class SummaryCard(MDCard):
    def __init__(self, title, amount="KES 0.00", **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = dp(16)
        self.spacing = dp(8)
        self.size_hint_y = None
        self.height = dp(120)
        self.md_bg_color = [0.9, 0.9, 0.9, 1]

        # Title label
        self.title_label = MDLabel(
            text=title,
            theme_text_color="Secondary",
            font_style="Body1"
        )
        
        # Amount label
        self.amount_label = MDLabel(
            text=amount,
            theme_text_color="Primary",
            font_style="H5"
        )
        
        self.add_widget(self.title_label)
        self.add_widget(self.amount_label)

    def update_amount(self, amount):
        self.amount_label.text = amount

class SummariesScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_manager = DataManager(get_storage_path=get_app_path)
        self.build_ui()

    def build_ui(self):
        # Main layout
        self.layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(16),
            spacing=dp(16)
        )

        # Title
        title = MDLabel(
            text="Financial Summary",
            halign="center",
            font_style="H5",
            size_hint_y=None,
            height=dp(48)
        )
        self.layout.add_widget(title)

        # Create summary cards
        self.income_card = SummaryCard(title="Monthly Income")
        self.expenses_card = SummaryCard(title="Monthly Expenses")
        self.savings_card = SummaryCard(title="Monthly Savings")
        
        # Add cards to layout
        self.layout.add_widget(self.income_card)
        self.layout.add_widget(self.expenses_card)
        self.layout.add_widget(self.savings_card)

        self.add_widget(self.layout)

    def on_enter(self):
        """Called when screen is entered"""
        self.update_overview()

    def update_overview(self):
        """Update financial overview"""
        try:
            overview = self.data_manager.transactions.generate_monthly_overview()
            
            # Update card amounts
            self.income_card.update_amount(f"KES {overview['income']:,.2f}")
            self.expenses_card.update_amount(f"KES {overview['expenses']:,.2f}")
            self.savings_card.update_amount(f"KES {overview['savings']:,.2f}")
            
        except Exception as e:
            Logger.error(f"Error updating summary: {str(e)}")

    def update_chart(self, chart_type="bar"):
        """Create or update financial chart"""
        if self.chart:
            self.ids.chart_container.remove_widget(self.chart)
            
        if chart_type == "bar":
            self.chart = Graph(
                xlabel='Month', ylabel='Amount',
                x_ticks_minor=1, x_ticks_major=1,
                y_ticks_major=5000,
                y_grid_label=True, x_grid_label=True,
                padding=5, xlog=False, ylog=False,
                x_grid=True, y_grid=True, xmin=-0.5, xmax=5.5, ymin=0, ymax=25000
            )
            self.bar_plot = BarPlot(color=[0, 1, 0, 1])
            self.chart.add_plot(self.bar_plot)
        else:
            self.chart = Graph(
                xlabel='Month', ylabel='Amount',
                x_ticks_minor=1, x_ticks_major=1,
                y_ticks_major=5000,
                y_grid_label=True, x_grid_label=True,
                padding=5, xlog=False, ylog=False,
                x_grid=True, y_grid=True, xmin=-0.5, xmax=5.5, ymin=0, ymax=25000
            )
            self.line_plot = LinePlot(line_width=1.5, color=[1, 0, 0, 1])
            self.chart.add_plot(self.line_plot)
            
        # Add chart data (example with 6 months history)
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        income_data = [(i, val) for i, val in enumerate([15000, 18000, 16500, 21000, 19500, 23000])]
        expenses_data = [(i, val) for i, val in enumerate([12000, 14000, 13000, 16000, 15000, 17000])]
        
        if chart_type == "bar":
            self.bar_plot.points = income_data
        else:
            self.line_plot.points = income_data
        
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
                MDFlatButton(text="CLOSE", on_release=lambda x: dialog.dismiss())
            ]
        )
        dialog.open()
    
    def refresh_summary(self, *args):
        # Refresh summary logic here
        pass