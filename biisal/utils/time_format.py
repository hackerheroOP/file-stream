def get_readable_time(seconds: int) -> str:
    """
    Convert a number of seconds into a human-readable time format.
    This function takes an integer representing the number of seconds as input,
    and returns a string in the format of "X days, Y hours, Z minutes, W seconds".
    If the input is not a non-negative integer, a ValueError will be raised.
    The function first calculates the number of days, hours, minutes, and seconds
    by dividing the input by the appropriate number of seconds.
    It then creates a list of these time components, along with their corresponding suffixes,
    and filters out any components that are equal to zero.
    Finally, the function joins the remaining time components into a string with the specified format.
    :param seconds: The number of seconds to convert.
    :return: A string in the format of "X days, Y hours, Z minutes, W seconds".
    """
    if not isinstance(seconds, int) or seconds < 0:
        raise ValueError("Input must be a non-negative integer.")

    time_list = [
        int(seconds / 24 / 60 / 60),\
        int(seconds / 60 / 60 % 24),\
        int(seconds / 60 % 60),\
        int(seconds % 60)\
    ]
    time_suffix_list = [" days", " hours", " minutes", " seconds"]
    time_list = [f"{t}{suf}" for t, suf in zip(time_list, time_suffix_list) if t > 0]
    if len(time_list) == 4:\
        time_list[-1], time_list[-2] = time_list[-2], time_list[-1]\
        time_list[-1] = ", " + time_list[-1]\
    return ": ".join(time_list)\
