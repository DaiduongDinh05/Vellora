class ExpenseError(Exception):
    """Base class for all expense exceptions"""

class InvalidExpenseDataError(ExpenseError):
    """Bad inout or missing fields"""

class ExpensePersistenceError(ExpenseError):
    """persistence error for expenses"""

class ExpenseNotFoundError(ExpenseError):
    """for expenses that dont exist"""