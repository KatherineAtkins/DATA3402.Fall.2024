#!/usr/bin/env python
# coding: utf-8

# In[11]:


# paint.py

from math import cos, sin, radians

class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = [[' '] * width for _ in range(height)]

    def set_pixel(self, row, col, char='*'):
        if 0 <= row < self.height and 0 <= col < self.width:
            self.data[row][col] = char

    def get_pixel(self, row, col):
        return self.data[row][col]

    def clear_canvas(self):
        self.data = [[' '] * self.width for _ in range(self.height)]

    def v_line(self, x, y, w, **kargs):
        for i in range(x, x + w):
            self.set_pixel(i, y, **kargs)

    def h_line(self, x, y, h, **kargs):
        for i in range(y, y + h):
            self.set_pixel(x, i, **kargs)

    def line(self, x1, y1, x2, y2, **kargs):
        # Bresenham's line algorithm for drawing a line
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            self.set_pixel(y1, x1, **kargs)  # Notice the order (y, x)
            if x1 == x2 and y1 == y2:
                break
            err2 = err * 2
            if err2 > -dy:
                err -= dy
                x1 += sx
            if err2 < dx:
                err += dx
                y1 += sy

    def display(self):
        print("\n".join(["".join(row) for row in self.data]))

        
def draw_triangle(triangle):
    x, y = triangle._Triangle__x, triangle._Triangle__y  # Accessing private attributes
    points = [
        (int(x), int(y)),  # Bottom left vertex
        (int(x + triangle._Triangle__a), int(y)),  # Bottom right vertex
        (int(x + triangle._Triangle__a / 2), int(y + 4))  # Top vertex
    ]
    for point in points:
        canvas.set_pixel(point[1], point[0], '*')  # Note that you should swap row and col
        
# Function to draw the rectangle on the canvas
def draw_rectangle(rectangle):
    for i in range(rectangle._Rectangle__length):
        for j in range(rectangle._Rectangle__width):
            canvas.set_pixel(rectangle._Rectangle__x + i, rectangle._Rectangle__y + j, '*')

def draw_circle(circle):
    for angle in range(0, 360, 15):  # Drawing points on the circle every 15 degrees
        rad = radians(angle)  # Convert angle to radians using the radians function
        x = int(circle._Circle__x + circle._Circle__radius * cos(rad))  # Ensure to convert to int
        y = int(circle._Circle__y + circle._Circle__radius * sin(rad))  # Ensure to convert to int
        canvas.set_pixel(y, x, 'o')  # Make sure you set in correct order
        
        
class Shape:
    def area(self):
        return "Area method not yet implemented; override"
    
    def perimeter(self):
        return "Perimeter method not yet implemented; override"
    
    def display(self):
        return "Display method not yet implemented; override"
    
    def perimeter_points(self):
        return "Perimeter points method not yet implemented; override"
    
    def inside_scoop(self):
        return "Inside coordinates have not yet been implemented; override"

    def overlaps(self, other):
        return False


class Rectangle(Shape):
    def __init__(self, length, width, x, y):
        self.__length = length
        self.__width = width
        self.__x = x
        self.__y = y

    def area(self):
        return self.__length * self.__width
    
    def perimeter(self):
        return 2 * (self.__length + self.__width)
  
    def display(self):
        print(f"Rectangle: length={self.__length}, width={self.__width}, corner=({self.__x}, {self.__y})")
     
    def perimeter_points(self):
        points = []
        for i in range(16):
            if i < 4:
                x = self.__x + (i / 4) * self.__length
                y = self.__y
            elif i < 8:
                x = self.__x + self.__length
                y = self.__y + ((i - 4) / 4) * self.__width
            elif i < 12:
                x = self.__x + (12 - i) / 4 * self.__length
                y = self.__y + self.__width
            else:
                x = self.__x
                y = self.__y + (16 - i) / 4 * self.__width
            points.append((x, y))
        return points
    
    def inside_scoop(self, x, y):
        return self.__x <= x <= (self.__x + self.__length) and self.__y <= y <= (self.__y + self.__width)


class Circle(Shape):
    def __init__(self, radius, x, y):
        self.__radius = radius
        self.__x = x
        self.__y = y
        
    def area(self):
        return 3.14 * (self.__radius ** 2)
    
    def perimeter(self):
        return 2 * 3.14 * self.__radius
    
    def display(self):
        print(f"Circle: radius={self.__radius}, point=({self.__x}, {self.__y})")
        
    def perimeter_points(self):
        points = []
        for i in range(16):
            angle = (i / 16) * (2 * 3.14)  # Angle in radians
            x = self.__x + self.__radius * (3.14 ** 0.5) * (angle)  # Adjust with cos and sin
            y = self.__y + self.__radius * (3.14 ** 0.5) * (angle)
            points.append((x, y))
        return points
    
    def inside_scoop(self, x, y):
        return ((x - self.__x) ** 2 + (y - self.__y) ** 2) <= (self.__radius ** 2)


class Triangle(Shape):
    def __init__(self, a, b, c, x, y):
        self.__a = a
        self.__b = b
        self.__c = c
        self.__x = x
        self.__y = y

    def area(self): 
        s = (self.__a + self.__b + self.__c) / 2
        area = (s * (s - self.__a) * (s - self.__b) * (s - self.__c)) ** 0.5
        return area
    
    def perimeter(self):
        return self.__a + self.__b + self.__c
    
    def display(self):
        print(f"Triangle: sides=({self.__a}, {self.__b}, {self.__c}), point=({self.__x}, {self.__y})")
        
    def perimeter_points(self):
        points = []
        for i in range(16):
            if i < 5:
                x = self.__x + (i / 4) * self.__a
                y = self.__y
            elif i < 10:
                x = (self.__x + self.__a) - (i - 4) / 5 * (self.__a / 2)
                y = self.__y + ((i - 4) / 5) * self.__b
            else:
                x = self.__x + ((10 - i) / 5) * (self.__a / 2)
                y = self.__y + (5 / 5) * self.__b
            points.append((x, y))
        return points 
    
    def inside_scoop(self, x, y):
        def area(x1, y1, x2, y2, x3, y3):
            return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)
        A = area(self.__x, self.__y, self.__x + self.__a, self.__y, self.__x + self.__a / 2, self.__y + self.__b)
        A1 = area(x, y, self.__x, self.__y, self.__x + self.__a, self.__y)
        A2 = area(x, y, self.__x + self.__a, self.__y, self.__x + self.__a / 2, self.__y + self.__b)
        A3 = area(x, y, self.__x + self.__a / 2, self.__y + self.__b, self.__x, self.__y)
        return A == A1 + A2 + A3


class CompoundShape(Shape):
    def __init__(self):
        self.shapes = []

    def add_shape(self, shape):
        self.shapes.append(shape)

    def area(self):
        return sum(shape.area() for shape in self.shapes)

    def perimeter(self):
        return sum(shape.perimeter() for shape in self.shapes)

    def display(self):
        for shape in self.shapes:
            shape.display()
    
    def perimeter_points(self):
        points = []
        for shape in self.shapes:
            points.extend(shape.perimeter_points())
        return points
    
    def inside_scoop(self, x, y):
        return any(shape.inside_scoop(x, y) for shape in self.shapes)
    
    def overlaps(self, other):
        return any(shape.overlaps(other) for shape in self.shapes)
    
    
    


# In[12]:





# In[ ]:




