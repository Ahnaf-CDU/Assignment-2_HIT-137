import turtle
import math

# Question 3: Recursive Geometric Pattern Generator
# Creates fractal-like patterns using turtle graphics with inward-pointing indentations

def draw_recursive_edge(t, length, depth):
    """
    Recursively draw an edge with fractal-like indentations.
    
    Pattern: Divides edge into 3 segments, replaces middle with inward triangle
    This creates 4 segments, each 1/3 the original length
    
    Args:
        t: turtle object
        length: length of the edge
        depth: recursion depth (0 = straight line)
    """
    if depth == 0:
        # Base case: draw a straight line
        t.forward(length)
    else:
        # Recursive case: divide edge into 4 segments with indentation
        segment_length = length / 3
        
        # Draw first 1/3 segment
        draw_recursive_edge(t, segment_length, depth - 1)
        
        # Create inward-pointing triangle (indentation)
        t.right(60)  # Turn right 60° for inward triangle
        draw_recursive_edge(t, segment_length, depth - 1)  # First triangle side
        
        t.left(120)  # Turn left 120° to complete equilateral triangle
        draw_recursive_edge(t, segment_length, depth - 1)  # Second triangle side
        
        t.right(60)  # Turn back to original direction
        
        # Draw final 1/3 segment
        draw_recursive_edge(t, segment_length, depth - 1)

def draw_polygon(sides, side_length, depth):
    """
    Draw a polygon with recursive fractal edges.
    
    Args:
        sides: number of sides for the polygon
        side_length: length of each side
        depth: recursion depth for the fractal pattern
    """
    # Calculate the exterior angle for turning at each vertex
    exterior_angle = 360 / sides
    
    # Create graphics window
    screen = turtle.Screen()
    screen.title(f"Recursive Polygon - {sides} sides, depth {depth}")
    screen.bgcolor("white")
    screen.setup(width=1000, height=1000)
    
    # Create and configure turtle
    t = turtle.Turtle()
    t.speed(0)  # Fastest drawing speed
    t.color("blue")
    t.pensize(1)
    
    # Position turtle at center of screen
    t.penup()
    t.home()  # Start at center (0,0)
    # Offset for better visual centering
    start_x = -side_length // 2
    start_y = side_length // 4  # Slightly above center
    t.goto(start_x, start_y)
    t.pendown()
    
    # Draw each side of the polygon with recursive pattern
    for i in range(sides):
        draw_recursive_edge(t, side_length, depth)
        t.right(exterior_angle)  # Turn to next side
    
    # Keep window open until clicked
    screen.exitonclick()


def main():
    """Main function to get user input and draw the pattern."""
    try:
        print("Recursive Geometric Pattern Generator")
        print("=" * 40)
        
        # Get user input with validation
        sides = int(input("Enter the number of sides: "))
        if sides < 3:
            print("Number of sides must be at least 3!")
            return
            
        side_length = int(input("Enter the side length: "))
        if side_length <= 0:
            print("Side length must be positive!")
            return
            
        depth = int(input("Enter the recursion depth: "))
        if depth < 0:
            print("Recursion depth must be non-negative!")
            return
        
        print(f"\nGenerating pattern with {sides} sides, length {side_length}, depth {depth}")
        print("Click on the graphics window to close it when done.")
        
        # Generate the fractal pattern
        draw_polygon(sides, side_length, depth)
        
    except ValueError:
        print("Please enter valid integer values!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()