### zadanie 5 ###
#stworzyć program pozwalający na obliczanie miejsc zerowych
#funkcji kwadratowej. W zależności od ilości miejsc zerowych wyświetlana powinna być
#ich ilość.
import math

a = int(input("Podaj parametr a: "))
b = int(input("Podaj parametr b: "))
c = int(input("Podaj parametr c: "))

delta = (b ** 2) - 4 * a * c
#delta
if (delta > 0):
    delta = math.sqrt(delta)
    x1 = (-b - delta)/(2*a)
    x2 = (-b + delta) / (2 * a)
    print("x1 = ", x1, ", x2 = ", x2)
elif ((delta == 0) and (a != 0)):
    delta = math.sqrt(delta)
    x2 = (-b + delta) / (2 * a)
    print("x1 = x2 = ", x2)
else:
    print("Równanie nie ma rozwiązań w dziedzinie liczb rzeczywistych")