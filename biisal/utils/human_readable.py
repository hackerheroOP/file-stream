# (c) 2023 @biisal, adarsh-goel

def humanbytes(size: float) -> str:
    """
    Convert a file size in bytes to a human-readable format.

    Args:
        size (float): The file size in bytes.

    Returns:
        str: The file size in a human-readable format.
    """
    if not isinstance(size, (int, float)):
        raise ValueError("Size must be a number")

    if not size:
        return ""

    power = 1024
    n = 0
    power_names = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}

    while size > power:
        size /= power
        n += 1

    return f"{size:.2f} {power_names[n]}B"
