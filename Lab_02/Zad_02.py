### zadanie 1 ###
#Zmodyfikować kod z zadnia 1 tak aby dodatkowo liczony był obwód trójkąta oraz jego
#powierzchnia, do tego celu należy stworzyć nową funkcję obwód oraz nową funkcję
#powierzchnia.


def przeciwprostokatna(a, b):
    wynik = (a*a + b*b)**0.5
    return wynik

def obwod(a, b, c):
    wynik = a + b + c
    return wynik

def powierzchnia(a, h):
    wynik = (a*h)/2
    return wynik

przyprostokatna1 = int(input("Podaj dlugosc 1 przyprostokatnej: "))
przyprostokatna2 = int(input("Podaj dlugosc 2 przyprostokatnej: "))

Przeciwprostokatna = przeciwprostokatna(przyprostokatna1, przyprostokatna2)
WynikObwod = obwod(przyprostokatna1, przyprostokatna2, Przeciwprostokatna)
WynikPowierzchnia = powierzchnia(przyprostokatna1, przyprostokatna2)

print(f"Dlugosc przeciwprostokatnej wynosi: {Przeciwprostokatna:.2f}")
print(f"Dlugosc obwodu wynosi: {WynikObwod:.2f}")
print(f"Pole powierzchni wynosi: {WynikPowierzchnia:.2f}")
