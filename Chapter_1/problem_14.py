import math
import sys

# From page 20:
#
# Write a program that converts complex numbers from the form x + jy to the polar form R,Theta.
# Write another that does the conversion in the opposite direction.
# Use degree as the unit of angle.

# I think the angle output for complex_to_polar is wrong, only being in the range -90 to 90 degrees
# When I'd want it to be 0 to 360. Maybe I forget the effective range of arctan, in which case
#  I'll just have to flip it around for the other half it can't do on its own.

# x is real, y is imaginary
def complex_to_polar(x, y):
    radius = math.sqrt(x*x + y*y)

    # Avoid divide-by-zero
    angle = 0
    if x == 0:
        if y < 0:
            angle = -math.pi / 2
        elif y > 0:
            angle = math.pi / 2
        else:
            angle = 0 # x=0 and y=0, angle is undefined
    else:
        angle = math.atan(y / x)

    return radius, radians_to_degrees(angle)

def polar_to_complex(radius, angle):
    angle = degrees_to_radians(angle)
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    return x, y

def degrees_to_radians(degrees):
    return 2 * math.pi * (degrees / 360)

def radians_to_degrees(radians):
    return 360 * (radians / (2 * math.pi))

def usage():
    print("Usage: python3 problem_14.py [x/radius] [y/angle]")

if len(sys.argv) != 3:
    usage()
    sys.exit(0)

try:
    x_or_radius = float(sys.argv[1])
    y_or_angle = float(sys.argv[2])
except ValueError:
    print("Not a number!")
    usage()
    sys.exit(0)

polar_form   = complex_to_polar(x_or_radius, y_or_angle)
complex_form = polar_to_complex(x_or_radius, y_or_angle)

print("Complex to Polar form   :", polar_form)
print("Polar   to Complex form :", complex_form)
