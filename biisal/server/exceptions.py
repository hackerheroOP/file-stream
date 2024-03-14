class InvalidHash(Exception):
    """
    This class represents an exception that is raised when an invalid hash is encountered.
    The message attribute stores the error message associated with the exception.
    """
    def __init__(self):
        """
        Initializes the InvalidHash exception with an error message.
        """
        self.message = "Invalid hash"

class FileNotFound(Exception):
    """
    This class represents an exception that is raised when a file is not found.
    The message attribute stores the error message associated with the exception.
    """
    def __init__(self):

