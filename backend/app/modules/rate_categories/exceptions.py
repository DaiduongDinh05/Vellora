class RateCategoryError(Exception):
    """Base class for all rate customization exceptions"""

class InvalidRateCategoryDataError(RateCategoryError):
    """Bad inout or missing fields"""

class RateCategoryPersistenceError(RateCategoryError):
    """persistence error for expenses"""

class RateCategoryNotFoundError(RateCategoryError):
    """for expenses that dont exist"""