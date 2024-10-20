### zadanie 1 ###
#Napisać program który prosi użytkownika o podanie dlugośi 2 boków trójkąta prostokątnego.
#Następnie korzystając z funkcji przeciwprostokatna() program wyświetla na ekranie komunikat
#jaka jest długość przeciwprostokątnej tego trójkąta.

def przeciwprostokatna(a, b):
    wynik = (a*a + b*b)**0.5
    return wynik

przyprostokatna1 = int(input("Podaj dlugosc 1 przyprostokatnej: "))
przyprostokatna2 = int(input("Podaj dlugosc 2 przyprostokatnej: "))

wynik = przeciwprostokatna(przyprostokatna1, przyprostokatna2)

print(f"Dlugosc przeciwprostokatnej wynosi: {wynik:.2f}")


