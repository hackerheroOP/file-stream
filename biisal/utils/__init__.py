# A simple program to calculate the area of a rectangle

def calculate_rectangle_area(length, width):
    """
    This function calculates the area of a rectangle using the formula: area = length * width.

    :param length: The length of the rectangle. This parameter should be a positive number.
    :param width: The width of the rectangle. This parameter should also be a positive number.
    :return: The area of the rectangle as a float. If either the length or width is not positive, the function will return None.
    """
    if length <= 0 or width <= 0:
        return None
    else:
        return length * width

# Get user input for length and width
length = float(input("Enter the length of the rectangle: "))
width = float(input("Enter the width of the rectangle: "))

# Calculate the area
area = calculate_rectangle_area(length, width)

# Display the area
if area is not None:
    print(f"The area of the rectangle is: {area}")
else:
    print("Invalid input. Please enter a positive value for length and width.")
