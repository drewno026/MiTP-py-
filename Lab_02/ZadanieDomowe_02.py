### Zadanie domowe 2 ###
import math

def CalculateSphere(radius, density):
    SurfaceArea = 4*math.pi*radius**2
    Volume = 4*(math.pi * radius**3)/3
    Mass = density * Volume

    return SurfaceArea, Volume, Mass

def CalculateRegularTetrahedron(EgdeLenght, density):
    SurfaceArea = math.sqrt(3)*EgdeLenght**2
    Volume = EgdeLenght**3/(6*math.sqrt(2))
    Mass = density*Volume

    return SurfaceArea, Volume, Mass

def CalculateRectangularPyramid(length, width, height, density):
#    SurfaceArea =
    Volume = length*width*height/3
    Mass = density*length*width*height/3

    return Volume, Mass

def CalculateCone(radius, height, density):
    SurfaceArea = math.pi*radius(radius+(math.sqrt(radius**2 + height**2)))
    Volume = math.pi*radius**2*height/3
    Mass = density*Volume/3

    return SurfaceArea, Volume, Mass

def CalculateCylinder(radius, height, density):
    SurfaceArea = 2*math.pi*radius(radius+height)
    Volume = math.pi*radius**2*height
    Mass = density*Volume

    return SurfaceArea, Volume, Mass


