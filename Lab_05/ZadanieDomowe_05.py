import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from scipy.io.wavfile import write
import csv

class WaveformGenerator:
    def __init__(self, sample_rate, duration):
        self.sample_rate = sample_rate
        self.duration = duration
        self.time = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    def sine_wave(self, f, A):
        return A * np.sin(2 * np.pi * f * self.time)

    def square_wave(self, f, A):
        return A * np.sign(np.sin(2 * np.pi * f * self.time))

    def sawtooth_wave(self, f, A):
        return A * (2 * (self.time * f - np.floor(0.5 + self.time * f)))

    def triangle_wave(self, f, A):
        return A * (2 * np.abs(2 * (self.time * f - np.floor(0.5 + self.time * f))) - 1)

    def white_noise(self, A):
        return A * np.random.normal(0, 1, len(self.time))

    def plot_waveform(self, signal, start=0, end=0.01):
        start_idx = int(start * self.sample_rate)
        end_idx = int(end * self.sample_rate)
        plt.plot(self.time[start_idx:end_idx], signal[start_idx:end_idx])
        plt.xlabel("Time [s]")
        plt.ylabel("Amplitude")
        plt.title("Waveform")
        plt.show()

    def calculate_fourier_transform(self, signal):
        N = len(signal)
        yf = fft(signal)
        xf = fftfreq(N, 1 / self.sample_rate)[:N // 2]
        return xf, 2.0 / N * np.abs(yf[:N // 2])

    def plot_fourier_transform(self, signal):
        xf, yf = self.calculate_fourier_transform(signal)
        plt.plot(xf, yf)
        plt.xlabel("Frequency [Hz]")
        plt.ylabel("Amplitude")
        plt.title("Fourier Transform")
        plt.show()

    def save_fourier_to_csv(self, signal, filename="fourier_transform.csv"):
        xf, yf = self.calculate_fourier_transform(signal)
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Frequency [Hz]", "Amplitude"])
            writer.writerows(zip(xf, yf))
        print(f"Fourier transform saved to {filename}")

    def save_waveform_to_wav(self, signal, filename="waveform.wav"):
        scaled_signal = np.int16(signal / np.max(np.abs(signal)) * 32767)
        write(filename, self.sample_rate, scaled_signal)
        print(f"Waveform saved to {filename}")

def main_menu():
    print("Waveform Generator Menu:")
    print("1. Generate Sine Wave")
    print("2. Generate Square Wave")
    print("3. Generate Sawtooth Wave")
    print("4. Generate Triangle Wave")
    print("5. Generate White Noise")
    print("6. Plot Waveform")
    print("7. Plot Fourier Transform")
    print("8. Save Fourier Transform to CSV")
    print("9. Save Waveform to WAV")
    print("0. Exit")

def main():
    try:
        sample_rate = int(input("Enter sample rate or press Enter for default (44100): ") or 44100)
        duration = float(input("Enter duration in seconds or press Enter for default (1.0): ") or 1.0)
    except ValueError:
        print("Invalid input. Using default values: sample_rate = 44100, duration = 1.0")
        sample_rate = 44100
        duration = 1.0

    generator = WaveformGenerator(sample_rate, duration)
    signal = None

    while True:
        main_menu()
        choice = input("Select an option: ")

        match choice:
            case "1":
                f = float(input("Enter frequency: "))
                A = float(input("Enter amplitude: "))
                signal = generator.sine_wave(f, A)
            case "2":
                f = float(input("Enter frequency: "))
                A = float(input("Enter amplitude: "))
                signal = generator.square_wave(f, A)
            case "3":
                f = float(input("Enter frequency: "))
                A = float(input("Enter amplitude: "))
                signal = generator.sawtooth_wave(f, A)
            case "4":
                f = float(input("Enter frequency: "))
                A = float(input("Enter amplitude: "))
                signal = generator.triangle_wave(f, A)
            case "5":
                A = float(input("Enter amplitude: "))
                signal = generator.white_noise(A)
            case "6":
                if signal is not None:
                    start = float(input("Enter start time (s): "))
                    end = float(input("Enter end time (s): "))
                    generator.plot_waveform(signal, start, end)
                else:
                    print("Generate a signal first!")
            case "7":
                if signal is not None:
                    generator.plot_fourier_transform(signal)
                else:
                    print("Generate a signal first!")
            case "8":
                if signal is not None:
                    filename = input("Enter filename (default: 'fourier_transform.csv'): ")
                    filename = filename if filename else "fourier_transform.csv"
                    generator.save_fourier_to_csv(signal, filename)
                else:
                    print("Generate a signal first!")
            case "9":
                if signal is not None:
                    filename = input("Enter filename (default: 'waveform.wav'): ")
                    filename = filename if filename else "waveform.wav"
                    generator.save_waveform_to_wav(signal, filename)
                else:
                    print("Generate a signal first!")
            case "0":
                break
            case _:
                print("Invalid choice. Please select again.")

if __name__ == "__main__":
    main()
