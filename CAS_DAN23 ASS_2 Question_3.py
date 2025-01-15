# This program creates a visually balanced tree using recursion.
#  GROUP CAS/DAN23
# ARYAN RAYAMAJHI [s385826]
# MEENU DEVI MEENU DEVI [s383485]
# RIWAJ ADHIKARI [s385933]
# SAKAR KHADKA [s385095]


import turtle


# Instructions for creating a visually balanced tree
print("To create a visually balanced tree, follow these instructions:")
print("1. Left and right angle branches should be in the range of 15 to 45 degrees.")
print("2. The starting branch length should be at least 50.")
print("3. Recursion depth should be at least 3.")
print("4. The reduction factor should be from 0.5 to 0.8.")
print("Now you can try out as you like. Thank you!")

# Function to get a floating-point input from the user with validation
def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt))  # Try to convert user input to float
        except ValueError:
            print("Invalid input! Please enter a numeric value.")  # Handle non-numeric input
 
# Prompt user for tree parameters with appropriate messages
left_angle = get_float_input("Enter left branch angle: ")  # Get left branch angle from user
right_angle = get_float_input("Enter right branch angle: ")  # Get right branch angle from user
branch_length = get_float_input("Enter starting branch length: ")  # Get the starting branch length
recursion_depth = get_float_input("Enter recursion depth: ")  # Get the recursion depth for the tree
reduction_factor = get_float_input("Enter branch length reduction factor (e.g., 0.7): ")  # Get the reduction factor for branch length
 
# Setup the screen and turtle
screen = turtle.Screen()
screen.screensize(600, 600)
t = turtle.Turtle()
t.speed(0)  # Set to maximum speed for faster drawing

def draw(length, depth):
    """
    Recursively draws a fractal tree.
    
    Parameters:
    length (float): The length of the current branch.
    depth (int): The remaining depth of recursion.
    """
    if depth == 0:
        return  # Base case: stop recursion when depth reaches 0

    # Set the color and thickness based on the current depth
    if depth == recursion_depth:
        t.color("brown")  # Color for the main trunk
        t.pensize(8)  # Thicker main trunk
    else:
        t.color("green")  # Color for the branches
        t.pensize(max(1, 8 * (depth / recursion_depth)))  # Decreasing thickness with depth

    t.forward(length)  # Draw the current branch

    # Save the current position and heading before drawing branches
    branch_point = t.pos()
    branch_heading = t.heading()

    # Draw the left branch
    t.left(left_angle)
    draw(length * reduction_factor, depth - 1)

    # Return to the saved position and heading
    t.penup()
    t.setpos(branch_point)
    t.setheading(branch_heading)
    t.pendown()

    # Draw the right branch
    t.right(right_angle)
    draw(length * reduction_factor, depth - 1)

# Initial setup: position the turtle at the starting point
t.penup()
t.goto(0, -300)  # Start at the bottom center of the screen
t.setheading(90)  # Point upwards
t.pendown()

# Draw the tree using the recursive function
draw(branch_length, recursion_depth)

# Hide the turtle after drawing and wait for a user click to close the window
t.hideturtle()
turtle.exitonclick()
