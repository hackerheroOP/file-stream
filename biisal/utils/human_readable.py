# (c) 2023 @biisal, adarsh-goel

def humanbytes(size: float) -> str:
    """
    Convert a file size in bytes to a human-readable format.

    This function takes a file size in bytes as input and returns a string
    representing the file size in a human-readable format, such as "10.50 KiB".

    Args:
        size (float): The file size in bytes. This argument should be a number
                     representing the file size.

    Returns:
        str: The file size in a human-readable format. This return value is a
             string that represents the file size in a human-readable format.
    """
    # Raise a ValueError if the input is not a number
    if not isinstance(size, (int, float)):
        raise ValueError("Size must be a number")
        
    # Return an empty string if the input is zero
    if not size:
        return ""
    
    # Define constants for byte conversion
    power = 
