import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import pandas as pd
# validation_type[1 - float, 2 - positive float, 3 - positive int]
def get_input(prompt, validation_type):
    while True:
        try:
            value = float(input(prompt)) if validation_type in (1, 2) else int(input(prompt))

            if validation_type == 2 and value <= 0:
                print("The number must be greater than 0.")
            elif validation_type == 3 and value <= 0:
                print("The number must be a positive integer.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a number.")

amplitude = get_input("Enter the oscillation amplitude: ", 1)
frequency = get_input("Enter the oscillation frequency: ", 1)
damping_coefficient = get_input("Enter the damping coefficient: ", 2)
noise_amplitude = get_input("Enter the noise amplitude: ", 1)
time_vector = get_input("Enter the time vector: ", 3)
num_steps = get_input("Enter the number of steps: ", 3)

x = np.linspace(0, time_vector, num_steps)
y = (amplitude * np.sin(2 * np.pi * frequency * x) * np.exp(-damping_coefficient * x) +
                      noise_amplitude * np.random.rand(num_steps))

def damped_sinusoid(x, amp, freq, damp, noise):
    return amp * np.sin(2 * np.pi * freq * x) * np.exp(-damp * x) + noise

initial_guess = [1, 1, 1, 1]

fit_params, covariance_matrix = curve_fit(damped_sinusoid, x, y, p0=initial_guess)

if input("Do you want to save the generated data to a file? (y/n)\t").lower() == "y":
    file_name = input("Enter the filename: ")
    data = {"t": x, "y": y}
    dataframe = pd.DataFrame(data)
    dataframe.to_csv(file_name + ".csv", index=False, sep="\t")
    print(f"Data saved to {file_name}.csv")

plt.scatter(x, y, label="Generated data")
plt.plot(x, damped_sinusoid(x, *fit_params), 'r', label="Fitted curve")
plt.xlabel("t [s]")
plt.ylabel("y")
plt.title(f"Damped sine wave plot: y = {amplitude} * sin(2π * {frequency}t) * e^(-{damping_coefficient}t) + noise")
plt.legend()
plt.show()