### Zadanie domowe 2 ###
import math

def calculate_sphere(radius, density):
    surface_area = 4*math.pi*radius**2
    volume = 4*(math.pi * radius**3)/3
    mass = density * volume
    return surface_area, volume, mass

def calculate_regular_tetrahedron(edge_length, density):
    surface_area = math.sqrt(3)*edge_length**2
    volume = edge_length**3/(6*math.sqrt(2))
    mass = density*volume
    return surface_area, volume, mass

def calculate_rectangular_pyramid(length, width, height, density):
    lateral_area = length*(math.sqrt((width/2)**2+height**2))+width*(math.sqrt((length/2)**2+height**2))
    surface_area = length*width+lateral_area
    volume = length*width*height/3
    mass = density*volume
    return surface_area, volume, mass

def calculate_cone(radius, height, density):
    surface_area = math.pi*radius*(radius+(math.sqrt(radius**2 + height**2)))
    volume = math.pi*radius**2*height/3
    mass = density*volume
    return surface_area, volume, mass

def calculate_cylinder(radius, height, density):
    surface_area = 2*math.pi*radius*(radius+height)
    volume = math.pi*radius**2*height
    mass = density*volume
    return surface_area, volume, mass

def calculate_ellipse(semi_major_axis, semi_minor_axis, density):
    epsilon = math.sqrt(1 - (semi_minor_axis**2/semi_major_axis**2))
    if epsilon != 0:
        surface_area = 2*math.pi*semi_minor_axis*(semi_minor_axis + semi_major_axis*math.acos(epsilon)/epsilon)
    else:
        surface_area = 4 * math.pi * semi_major_axis ** 2
    volume = (4*math.pi*semi_major_axis*semi_minor_axis**2)/3
    mass = density*volume
    return surface_area, volume, mass

while True:
    user_choice = input("sphere\nregular tetrahedron\nrectangular pyramid\ncone\n\
cylinder\nellipse\nWhat you want to calculate: ").lower()
    user_choice2 = input("What you want to calculate[surface area, volume, mass]: ")
    match user_choice:
        case "sphere":
            while True:
                radius = float(input("Insert radius[in meters]: "))
                if radius > 0:
                    if user_choice2 == "mass":
                        density = float(input("Insert density[kg/m^3]: "))
                        if density <= 0:
                            print("Density must be greater than 0")
                            continue
                    else:
                        density = 1
                    surface_area, volume, mass = calculate_sphere(radius, density)
                    break
                else:
                    print("All parameters must be greater than 0")
        case "regular tetrahedron":
            while True:
                edge_length = float(input("Insert edge length[in meters]: "))
                if edge_length > 0:
                    if user_choice2 == "mass":
                        density = float(input("Insert density[kg/m^3]: "))
                        if density <= 0:
                            print("Density must be greater than 0")
                            continue
                    else:
                        density = 1
                    surface_area, volume, mass = calculate_regular_tetrahedron(edge_length, density)
                    break
                else:
                    print("All parameters must be greater than 0")
        case "rectangular pyramid":
            while True:
                length = float(input("Insert length[in meters]: "))
                width = float(input("Insert width[in meters]: "))
                height = float(input("Insert height[in meters]: "))
                if length > 0 and width > 0 and height > 0:
                    if user_choice2 == "mass":
                        density = float(input("Insert density[kg/m^3]: "))
                        if density <= 0:
                            print("Density must be greater than 0")
                            continue
                    else:
                        density = 1
                    surface_area, volume, mass = calculate_rectangular_pyramid(length, width, height, density)
                    break
                else:
                    print("All parameters must be greater than 0")
        case "cone":
            while True:
                radius = float(input("Insert radius[in meters]: "))
                height = float(input("Insert height[in meters]: "))
                if radius > 0 and height > 0:
                    if user_choice2 == "mass":
                        density = float(input("Insert density[kg/m^3]: "))
                        if density <= 0:
                            print("Density must be greater than 0")
                            continue
                    else:
                        density = 1
                    surface_area, volume, mass = calculate_cone(radius, height, density)
                    break
                else:
                    print("All parameters must be greater than 0")
        case "cylinder":
            while True:
                radius = float(input("Insert radius[in meters]: "))
                height = float(input("Insert height[in meters]: "))
                if radius > 0 and height > 0:
                    if user_choice2 == "mass":
                        density = float(input("Insert density[kg/m^3]: "))
                        if density <= 0:
                            print("Density must be greater than 0")
                            continue
                    else:
                        density = 1
                    surface_area, volume, mass = calculate_cylinder(radius, height, density)
                    break
                else:
                    print("All parameters must be greater than 0")
        case "ellipse":
            while True:
                semi_major_axis = float(input("Insert semi-major axis[in meters]: "))
                semi_minor_axis = float(input("Insert semi-minor axis[in meters]: "))
                if semi_major_axis > 0 and semi_minor_axis > 0:
                    if user_choice2 == "mass":
                        density = float(input("Insert density[kg/m^3]: "))
                        if density <= 0:
                            print("Density must be greater than 0")
                            continue
                    else:
                        density = 1
                    surface_area, volume, mass = calculate_ellipse(semi_major_axis, semi_minor_axis, density)
                    break
                else:
                    print("All parameters must be greater than 0")
    match user_choice2:
        case "surface area":
            print(f"Surface area equals: {surface_area:.2f} m^2")
        case "volume":
            print(f"Volume equals: {volume:.2f} m^3")
        case "mass":
            print(f"Mass equals: {mass:.2f} kg")
    continue_choice = input("Do you want to continue(yes/no):").lower()
    if continue_choice != "yes":
        break