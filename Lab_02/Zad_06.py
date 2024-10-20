### Zadanie 5 ###
# Proszę napisać osobne funkcje pozwalające obliczyć:
#-objętość prostopadłościanu,
#-pole powierzchni prostopadłościanu,
#-masę prostopadłościanu
#W tym celu proszę pobrać od użytkownika 3 parametry geometryczne (długości boków w metrach) oraz gęstość w kg/m^3. Wynik działania powinien wyświetlić się na ekranie również w
#jednostkach układu SI.

def CalculateSurfaceArea(lenght, width, hight):
    if lenght > 0 and width > 0 and hight > 0:
        SurfaceArea = (lenght * width)*2 + (width*hight)*2 + (lenght * hight)*2
        return SurfaceArea
    else:
        print("All parameters must be greater than 0")

def CalculateVolume(lenght, width, hight):
    Volume = lenght*width*hight
    return Volume

def CalculateMass(density):
    mass = density*CalculateVolume(lenght, width, hight)
    return mass

while True:
    lenght = float(input("Insert lenght(in meters): "))
    width = float(input("Insert width(in meters): "))
    hight = float(input("Insert hight(in meters): "))
    density = float(input("Insert mass(kg/m^3): "))

    if lenght > 0 and width > 0 and hight > 0:
        SurfaceArea = CalculateSurfaceArea(lenght, width, hight)
        Volume = CalculateVolume(lenght, width, hight)
        Mass = CalculateMass(density)

        print(f"Surface area = {SurfaceArea:.2f} m^2")
        print(f"Volume = {Volume:.2f} m^3")
        print(f"Mass = {Mass:.2f} kg")

        UserChoice = input("Do you want to calculate again(yes/no)").lower()
        if UserChoice != "yes":
            break
    else:
        print("All parameters must be greater than 0")