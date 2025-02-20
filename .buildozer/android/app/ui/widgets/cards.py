# ui/widgets/cards.py
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty, NumericProperty, ColorProperty

class RatioCard(MDCard):
    """Financial ratio display card"""
    title = StringProperty("Ratio")
    value = NumericProperty(0)
    icon = StringProperty("cash")
    theme_color = StringProperty("Primary")
    text_color = ColorProperty([1, 1, 1, 1])
    bg_color = ColorProperty([0, 0, 0, 1])

class TransactionCard(MDCard):
    """Transaction history card"""
    date = StringProperty("")
    description = StringProperty("")
    amount = NumericProperty(0)
    category = StringProperty("income")
    icon = StringProperty("cash-plus")

class LoanCard(MDCard):
    """Loan information card with payment controls"""
    principal = NumericProperty(0)
    term = NumericProperty(0)
    apr = NumericProperty(0)
    payments_made = NumericProperty(0)
    description = StringProperty("")
    remaining_balance = NumericProperty(0)

class SummaryCard(MDCard):
    """Key metric summary card"""
    title = StringProperty("Metric")
    current_value = StringProperty("KES 0")
    comparison = StringProperty("+0% vs last month")
    icon = StringProperty("chart-box")
    icon_color = ColorProperty([1, 1, 1, 1])