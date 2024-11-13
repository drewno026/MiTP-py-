import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import pandas as pd

def get_input(prompt, validation_type):  # 1 - float, 2 - float>0, 3 int>0 4 - 0-1
    value = input(prompt)
    match validation_type:
        case 1 | 2 | 4:
            while True:
                try:
                    value = float(value)
                except:
                    value = input('Please enter a floating-point number (x.y): ')
                    continue
                if validation_type == 2:
                    if value <= 0:
                        value = input('The number must be greater than 0: ')
                        continue
                    else:
                        return float(value)
                elif validation_type == 4:
                    if value > 1 or value < 0:
                        value = input('The number must be in the range 0-1: ')
                        continue
                    else:
                        return float(value)
                else:
                    return float(value)
        case 3:
            while True:
                try:
                    value = int(value)
                except:
                    value = input('Please enter an integer: ')
                    continue
                if value <= 0:
                    value = input('The number must be greater than 0: ')
                    continue
                else:
                    return int(value)

amp_osc = get_input("Enter the oscillation amplitude: ", 1)
freq_osc = get_input("Enter the oscillation frequency: ", 1)
damping = get_input("Enter the damping coefficient: ", 2)
noise_amp = get_input("Enter the noise amplitude: ", 1)
time_vector = get_input("Enter the time vector: ", 3)
num_steps = get_input("Enter the number of steps: ", 3)

x = np.linspace(0, time_vector, num_steps)
y = amp_osc * np.sin(2 * np.pi * freq_osc * x) * np.exp(-damping * x) + noise_amp * (np.random.rand())

def damped_sinusoid(x, a, f, b, nt):
    return a * np.sin(2 * np.pi * f * x) * np.exp(-b * x) + nt

p0 = [1, 1, 1, 1]
fit_params, covariance_matrix = curve_fit(damped_sinusoid, x, y, p0=p0)

if input("Do you want to save the generated data to a file? (y/n)\t") == "y":
    filename = input("Enter the filename: ")
    data = {"t": x, "y": y}
    dataframe = pd.DataFrame(data)
    dataframe.to_csv(filename + ".csv", index=False, sep="\t")
    print(f"Data saved to {filename}.csv")

plt.scatter(x, y, label="Generated Data")
plt.plot(x, damped_sinusoid(x, *fit_params), 'r', label="Fitted Curve")
plt.xlabel("t [s]")
plt.ylabel("y")
plt.title(f"Damped Sine Wave Plot: y={amp_osc}*sin(2π*{freq_osc}t)*e^(-{damping}t)+ noise")
plt.legend()
plt.show()

mode = 1
while True:
    filename = input("Enter the filename to load the plot: ")
    try:
        df = pd.read_csv(filename + ".csv", sep="\t")
    except:
        print("File not found.")
        if input("Would you like to try reading the file again? (y/n)\t") == "y":
            continue
        else:
            mode = 0
            break
    t = np.array(df['t'])
    y = np.array(df['y'])
    break

if mode > 0:
    def damped_sinusoid(x, a, f, b, nt):
        return a * np.sin(2 * np.pi * f * x) * np.exp(-b * x) + nt

    plt.scatter(t, y)
    plt.xlabel("t [s]")
    plt.ylabel("y")
    plt.title("Damped Sine Wave Plot: y=A*sin(2πft)*e^(-yt)+ noise")
    plt.show()

    if input("Would you like to fit the parameters? (y/n)\t") == "y":
        p0 = [1, 1, 1, 1]
        fit_params, covariance_matrix = curve_fit(damped_sinusoid, t, y, p0=p0)
        print("Fitted Parameters:\nA =", fit_params[0], "\nf =", fit_params[1], "\ndamping =", fit_params[2])
        plt.plot(t, damped_sinusoid(t, *fit_params), 'r', label="Fitted Curve")
        plt.scatter(t, y, label="Loaded Data")
        plt.xlabel("t [s]")
        plt.ylabel("y")
        plt.title(f"Damped Sine Wave: y={round(fit_params[0], 2)}*sin(2π*{round(fit_params[1], 2)}t)*e^(-{round(fit_params[2], 2)}t)+ noise")
        plt.legend()
        plt.show()
    else:
        print("Goodbye")
else:
    print("Exiting the program")

#1, 2, 0.2, 0.2, 10, 1000