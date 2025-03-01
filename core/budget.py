# core/budget.py
class Budget:
    def __init__(self):
        self.salary = 0.0
        self.fixed_savings = 0.0
        self.fixed_expenses = []

    def add_fixed_expense(self, amount):
        self.fixed_expenses.append(float(amount))

    def total_fixed_expenses(self):
        return sum(self.fixed_expenses)

    def surplus(self):
        return self.salary - self.fixed_savings - self.total_fixed_expenses()

    def savings_percentage(self):
        if self.salary == 0:
            return 0
        return (self.fixed_savings / self.salary) * 100

    def expenses_percentage(self):
        if self.salary == 0:
            return 0
        return (self.total_fixed_expenses() / self.salary) * 100

    def surplus_percentage(self):
        if self.salary == 0:
            return 0
        return (self.surplus() / self.salary) * 100