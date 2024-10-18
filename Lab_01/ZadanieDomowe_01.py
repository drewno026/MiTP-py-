### zadanie_domowe_01 ###

while True:
    LoanAmount = float(input("Podaj kwotę kredytu (w złotych): "))
    InterestRate = float(input("Podaj oprocentowanie kredytu (w procentach): ")) / 100
    LoanYears = int(input("Podaj liczbę lat kredytu: "))
    MonthlyIncome = float(input("Podaj miesięczne dochody (w złotych): "))

    months = LoanYears * 12
    MonthlyInterestRate = InterestRate / 12
    MonthlyPayment = (LoanAmount * MonthlyInterestRate * (1 + MonthlyInterestRate) ** months) / \
                      ((1 + MonthlyInterestRate) ** months - 1)

    print(f"\nMiesięczna rata wynosi: {MonthlyPayment:.2f} zł")

    if MonthlyPayment < (MonthlyIncome / 3):
        print("Kredyt jest dostępny.")
    else:
        print("Kredyt nie jest dostępny.")

    user_choice = input("\nCzy chcesz dokonać kolejnych obliczeń? (tak/nie): ").lower()
    if user_choice != "tak":
        print("Dziękuję za skorzystanie z kalkulatora kredytowego!")
        break
