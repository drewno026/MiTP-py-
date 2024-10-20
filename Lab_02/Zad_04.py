### Zadanie 4 ###
#Napisz funkcję, która oblicza wszystkie kąty trójkąta zdefiniowanego przez podane 3 boki
#(niezależnie czy trójkąt jest prostokątny czy nie). Do tego celu proszę wykorzystać funkcje
#trygonometryczne dostępne w bibliotece numpy.

import math

import numpy as np
def przeciwprostokatna(a, b):
    wynik = (a*a + b*b)**0.5
    return wynik

def obwod(a, b):
    obw = a + b + przeciwprostokatna(a, b)
    return obw

def powierchnia(a, h):
    pole = (a*h)/2
    return pole

def ObliczKaty(a, b, c):
    if a+b <= c and a + c <= b and b + c <= a:
        print("Podane dlugosci nie moga tworzyc trojkata")
        return None
    else:
        cos_alfa = (b**2 + c**2 - a**2)/(2*c*b)
        cos_beta = (a**2 + c**2 - b**2)/(2*a*c)
        cos_gamma = (a**2 + b**2 - c**2)/(2*a*b)

        print(cos_alfa, cos_beta, cos_gamma)
        gamma = np.degrees(np.arccos(cos_gamma))
        beta = np.degrees(np.arccos(cos_beta))
        alfa = np.degrees(np.arccos(cos_alfa))

        print(f"Kat alfa wynosi: {alfa:.2f}")
        print(f"Kat beta wynosi: {beta:.2f}")
        print(f"Kat gamma wynosi: {gamma:.2f}")

        return alfa, beta, gamma

bok1 = int(input("Podaj dlugosc 1 boku: "))
bok2 = int(input("Podaj dlugosc 2 boku: "))
bok3 = int(input("Podaj dlugosc 3 boku: "))

ObliczKaty(bok1, bok2, bok3)
