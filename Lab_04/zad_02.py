import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import pandas as pd

while True:
    file_name = input("Enter the file name to read the plot: ")
    try:
        data_frame = pd.read_csv(file_name + ".csv", sep="\t")
        t = np.array(data_frame['t'])
        y = np.array(data_frame['a'])
        break
    except FileNotFoundError:
        print("File with this name not found.")
        if input("Would you like to try reading the file again (y/n)? ").lower() != "y":
            print("Exiting program.")
            exit()

def damped_sinusoid(x, a, f, b, nt):
    b = max(b, 0.0001)
    return a * np.sin(2 * np.pi * f * x) * np.exp(-b * x) + nt

plt.scatter(t, y)
plt.xlabel("t [s]")
plt.ylabel("y")
plt.title("Damped Sine Wave: y=A*sin(2πft)*e^(-yt) + aN(t)")
plt.show()

if input("Would you like to fit the parameters? (y/n): ").lower() == "y":
    initial_params = [1, 1, 1, 1]
    fit_params, covariance_matrix = curve_fit(damped_sinusoid, t, y, p0=initial_params)

    print("Fitted Parameters:\nA =", fit_params[0], "\nf =", fit_params[1], "\ngamma =", fit_params[2])

    plt.plot(t, damped_sinusoid(t, *fit_params), 'r', label="Fitted Damped Sinusoid")
    plt.scatter(t, y, label="Loaded Data")
    plt.xlabel("t [s]")
    plt.ylabel("y")
    plt.title(f"Damped Sine Wave: y={round(fit_params[0], 2)}*sin(2π*{round(fit_params[1], 2)}t)*e^(-{round(fit_params[2], 2)}t) + aN(t)")
    plt.legend()
    plt.show()
