from core.errors import CalculationError
from core.errors import FinanceError


class LoanCalculator:
    @staticmethod
    # Calculate APR and Total Interest
    def appraise_loan(principal, monthly_instalment, term_months, max_iter=100, tol=1e-6):
        try:
            def annuity_pv(i):
                return monthly_instalment * (1 - (1 + i) ** -term_months) / i - principal
            monthly_rate = 0.05/12  # Initial guess (5% APR)
            for _ in range(max_iter):
                f = annuity_pv(monthly_rate)
                f_prime = (annuity_pv(monthly_rate + 1e-6) - f) / 1e-6  # Numerical derivative
                monthly_rate -= f / f_prime
                if abs(f) < tol:
                    apr = round(monthly_rate * 12 * 100, 2)
                    total_interest = round(monthly_instalment * term_months - principal, 2)
                    return apr, total_interest
            return None, None  # No convergence
        except ZeroDivisionError:
            raise CalculationError("APR") from None
    
    @staticmethod

    @staticmethod
    def calculate_remaining_balance(principal, apr, payments_made, term_months):
        """
        Calculate the remaining balance on a loan using amortization formula
        
        Args:
            principal (float): Original loan amount
            apr (float): Annual Percentage Rate (e.g., 5.0 for 5%)
            payments_made (int): Number of payments already made
            term_months (int): Total loan term in months
            
        Returns:
            float: Remaining balance after payments
        """
        if payments_made >= term_months:
            return 0.0
            
        try:
            # Convert APR to monthly rate
            monthly_rate = apr / 100 / 12
            
            # Amortization formula
            remaining_months = term_months - payments_made
            balance = principal * (
                (1 + monthly_rate)**term_months - (1 + monthly_rate)**payments_made
            ) / (
                (1 + monthly_rate)**term_months - 1
            )
            
            # Round to 2 decimal places for currency
            return round(balance, 2)
            
        except ZeroDivisionError:
            # Handle 0% APR case
            return max(0, principal - (principal / term_months) * payments_made)
            
        except Exception as e:
            raise FinanceError(
                user_message="Could not calculate balance",
                technical_message=str(e)
            )

class FinancialMetrics:
    @staticmethod
    # Calculate Ratios
    def calculate_ratios(income, expenses, debt):
        if income == 0:
            return {
                'expenses_ratio': 0,
                'debt_ratio': 0,
                'savings_ratio': 0
            }
        expenses_ratio = (expenses / income) * 100
        debt_ratio = (debt / income) * 100
        savings_ratio = ((income - expenses - debt) / income) * 100
        return {
            'expenses_ratio': expenses_ratio,
            'debt_ratio': debt_ratio,
            'savings_ratio': savings_ratio
        }

    
    @staticmethod
    def validate_repayment(loan_entry):
        """
        Validate against stored loan data
        """
        expected_instalment = loan_entry['Monthly Instalment']
        actual_paid = loan_entry.get('paid_amount', 0)
        return actual_paid >= expected_instalment