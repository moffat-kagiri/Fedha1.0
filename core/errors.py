class FinanceError(Exception):
    """Base class for financial calculation errors"""
    def __init__(self, user_message, technical_message=None):
        self.user_message = user_message
        self.technical_message = technical_message or user_message
        super().__init__(self.technical_message)

class ValidationError(FinanceError):
    """Input validation failures"""
    def __init__(self, field, message):
        super().__init__(
            user_message=f"Invalid {field}: {message}",
            technical_message=f"Validation failed for {field}: {message}"
        )

class StorageError(FinanceError):
    """Data storage/retrieval failures"""
    def __init__(self, operation, details):
        super().__init__(
            user_message=f"Could not {operation} data",
            technical_message=f"Storage operation '{operation}' failed: {details}"
        )

class SyncError(FinanceError):
    """Cloud sync failures"""
    def __init__(self, service, details):
        super().__init__(
            user_message=f"{service} sync failed",
            technical_message=f"{service} sync error: {details}"
        )

class CalculationError(FinanceError):
    """Numerical calculation failures"""
    def __init__(self, calculation_type):
        super().__init__(
            user_message=f"Could not calculate {calculation_type}",
            technical_message=f"{calculation_type} calculation failed"
        )