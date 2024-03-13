class InvalidHash(Exception):
    def __init__(self):
        self.message = "Invalid hash"

class FileNotFound(Exception):
    def __init__(self):
        self.message = "File not found"
