### Zadanie 3 ###
def przeciwprostokatna(a, b):
    wynik = (a*a + b*b)**0.5
    return wynik

def obwod(a, b):
    obw = a + b + przeciwprostokatna(a, b)
    return obw

def powierchnia(a, h):
    pole = (a*h)/2
    return pole

bok1 = int(input("Podaj dlugosc 1 boku: "))
bok2 = int(input("Podaj dlugosc 2 boku: "))
bok3 = int(input("Podaj dlugosc 3 boku: "))

if(bok1 > 0 and bok2 > 0 and bok3 > 0):
    if bok1 > bok2 and bok1 > bok3:
        if(bok1 == przeciwprostokatna(bok2, bok3)):
            print("Trojkat jest prostokatny")
        else:
            print("Trojkat jest nie prostokatny")
    elif bok2 > bok1 and bok2 > bok3:
        if(bok2 == przeciwprostokatna(bok1, bok3)):
            print("Trojkat jest prostokatny")
        else:
            print("Trojkat jest nie prostokatny")
    else:
        if(bok3 == przeciwprostokatna(bok2, bok1)):
            print("Trojkat jest prostokatny")
        else:
            print("Trojkat jest nie prostokatny")
else:
    print("Podane dlugosci musza byc wieksze od zera")

