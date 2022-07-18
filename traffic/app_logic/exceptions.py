from enum import Enum


class TrafficApplicationException(Exception):
    class ErrorType(Enum):
        DATABASE_ERROR = 0

    def __init__(self, error_type: ErrorType, message=None):
        self.error_type = error_type
        self.message = message
        super().__init__(self.message)
